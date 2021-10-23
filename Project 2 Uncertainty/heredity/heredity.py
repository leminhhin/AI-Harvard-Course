import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]

def get_n_genes(person, one_gene, two_genes):
    """
    Return number of genes of that person
    """
    if person in one_gene:
        return 1
    elif person in two_genes:
        return 2
    return 0

def get_parents(people, person):
    """
    Return parents (mother and father) of the person
    """
    return people[person]['mother'], people[person]['father']

def get_passing_genes_probs(person, one_gene, two_genes):
    """
    Return possibility of passing gene from that person
    """
    if person in one_gene:
        return (1-PROBS["mutation"]) * 0.5
    elif person in two_genes:
        return 1-PROBS["mutation"]
    return PROBS["mutation"]

def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    joint_probs = 1
    # parents dictionary keeps track of the possibility of passing genes to their child
    parents_probs = dict()
    for person in people:
        # get person genes
        n_genes = get_n_genes(person, one_gene, two_genes)
        mother, father = get_parents(people, person)
        # calculate probability of having n_genes for parent
        if mother is None and father is None:
            # calculate probability of having n_genes (number of genes)
            gene_probs = PROBS["gene"][n_genes]
        # calculate probability for child
        else:
            # calculate probability of parents passing genes to child
            parents_probs[mother] = get_passing_genes_probs(mother, one_gene, two_genes)
            parents_probs[father] = get_passing_genes_probs(father, one_gene, two_genes)
            # calculate probability of having n_genes passed by parents
            if person in one_gene:
                # EITHER get gene from mother and not from father OR not get gene from mother but father
                gene_probs = parents_probs[mother] * (1-parents_probs[father]) + (1-parents_probs[mother]) * parents_probs[father]
            elif person in two_genes:
                # get each gene from both parents
                gene_probs = parents_probs[mother] * parents_probs[father]
            else:
                # not get get genes from both parents
                gene_probs = (1-parents_probs[mother]) * (1- parents_probs[father])

        # calculate probability of having trait (based on n_genes)
        trait_probs = PROBS["trait"][n_genes][person in have_trait]
        joint_probs *= gene_probs * trait_probs
    return joint_probs
    # raise NotImplementedError


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        n_genes = get_n_genes(person, one_gene, two_genes)
        probabilities[person]["gene"][n_genes] += p
        probabilities[person]["trait"][person in have_trait] += p        
    # raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        # normalize gene
        sum_probs = sum(probabilities[person]["gene"].values())
        for n_gene in probabilities[person]["gene"]:
            probabilities[person]["gene"][n_gene] /= sum_probs
        
        # normalize trait
        sum_probs = sum(probabilities[person]["trait"].values())
        for trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait] /= sum_probs
    # raise NotImplementedError


if __name__ == "__main__":
    main()
