import sys

from crossword import *

from collections import deque

class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains:
            for word in list(self.domains[var]):
                if len(word) != var.length:
                    self.domains[var].remove(word)
        # raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        is_revised = False
        overlaps = self.crossword.overlaps[x,y]
        if overlaps is not None:
            for word in list(self.domains[x]):
                x_overlaps = word[overlaps[0]]
                y_overlaps = [val[overlaps[1]] for val in list(self.domains[y])]
                if x_overlaps not in y_overlaps:
                    self.domains[x].remove(word)
                    is_revised = True
        return is_revised
        # raise NotImplementedError

    def get_all_arcs(self):
        dup_arcs = [{x,neighbor} for x in self.crossword.variables for neighbor in self.crossword.neighbors(x)]
        arcs = []
        # remove any duplicates
        for arc in dup_arcs:
            if arc not in arcs:
                arcs.append(arc)
        # convert every set of arc to tuple of arc
        arcs = [tuple(arc) for arc in arcs]
        return arcs

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # generate arcs if they are neighbors
        if arcs is None:
            arcs = self.get_all_arcs()
        queue = deque(arcs)
        while queue:
            x,y = queue.pop()
            if self.revise(x,y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x) - {y}:
                    queue.appendleft((z,x))
        return True
        # raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return len(assignment) == len(self.crossword.variables)
        # raise NotImplementedError

    def is_unique(self, assignment):
        # check if assignment values are distinct
        seen = set()
        return not any(i in seen or seen.add(i) for i in assignment.values())

    def is_unary_satisfied(self, assignment):
        # check var's length and value's length
        for var in assignment:
            if var.length != len(assignment[var]):
                return False
        return True

    def is_binary_satisfied(self, assignment):
        # check if all overlaps is satisfied
        for var in assignment:
            neighbors = (self.crossword.neighbors(var)).intersection(assignment.keys())
            for neighbor in neighbors:
                var_overlaps_pos, n_overlaps_pos = self.crossword.overlaps[var, neighbor]
                # if assignment[var][var_overlaps_pos] != assignment[neighbor][n_overlaps_pos]:
                if assignment[var][var_overlaps_pos] != assignment[neighbor][n_overlaps_pos]:
                    return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        return self.is_unique(assignment) and self.is_unary_satisfied(assignment) and self.is_binary_satisfied(assignment)
        # raise NotImplementedError

    def sort_dom(self, dic):
        # sort a dictionary
        return {val:occur for val, occur in sorted(dic.items(), key=lambda item: item[1])}

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # get all unassigned_neighbors
        neighbors = self.crossword.neighbors(var) - assignment.keys()
        count_ruleout = {val:0 for val in self.domains[var]}
        for neighbor in neighbors:
            for var_val in count_ruleout:
                if var_val in self.domains[neighbor]:
                    count_ruleout[var_val] += 1
        counts = self.sort_dom(count_ruleout)
        return list(counts.keys())
        # raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # get the sorted domains
        unassigned = self.crossword.variables - assignment.keys()

        counts = {var:len(self.domains[var]) for var in unassigned}
        sorted_dom = self.sort_dom(counts)
        
        min_MRV = list(sorted_dom.values())[0]

        # check MRV heuristic
        tied_vars = [var for var in sorted_dom if sorted_dom[var] == min_MRV]
        if len(tied_vars) == 1:
            return tied_vars[0]
        
        # get the sorted degrees
        for var in counts:
            counts[var] = len(self.crossword.neighbors(var))
        sorted_degrees = self.sort_dom(counts)

        min_degrees = list(sorted_degrees.values())[0]
        # check degree heuristic
        tied_vars = [var for var in sorted_degrees if sorted_degrees[var] == min_degrees]
        return tied_vars[0]
        
        # raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for val in self.domains[var]:
            assignment[var] = val
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result != None:
                    return result
                assignment.pop(var,None)
            assignment.pop(var,None)
        return None
        # raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
