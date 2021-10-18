import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # initialize distribution
    prob_distribution = {p:0 for p in corpus}
    # all pages have the same (1-d) probability
    for p in prob_distribution:
        prob_distribution[p] += (1-damping_factor)/len(corpus)
    linked_pages = corpus[page]
    # update prob for pages linked by current page
    for p in linked_pages:
        num_links = len(corpus) if len(linked_pages) == 0 else len(linked_pages)
        prob_distribution[p] += damping_factor/num_links
    return prob_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # create initial sample
    current_page = random.choice(list(corpus.keys()))
    PR_chain = [current_page]
    
    # Loop for n-1 remaining samples
    for i in range(n-1):
        distribution = transition_model(corpus,current_page,damping_factor)
        # pick a page randomly based on their weight
        current_page = random.choices(population=list(distribution.keys()),weights=list(distribution.values()),k=1).pop()
        # add chosen page to the chain
        PR_chain.append(current_page)
    
    # normalize results
    page_ranks = {page : PR_chain.count(page)/n for page in corpus}
    
    print(sum(page_ranks.values()))
    return page_ranks

def get_incoming_pages(corpus, current_page):
    """
    Return list of pages in corpus that link to current_page.
    """
    return [page for page in corpus if current_page in corpus[page]]

def calculate_i_sum_part(corpus, page_ranks, incoming_pages):
    """
    Return i sum part in formula.
    """
    result = 0
    for page in incoming_pages:
        num_links = len(corpus) if len(corpus[page]) == 0 else len(corpus[page])
        result += page_ranks[page] / num_links
    return result

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # STOPPING_CONDITION used to compare current changes with new changes
    STOPPING_CONDITION = 0.001
    # flag cont to check if STOPPING_CONDITION is satisfied
    cont = True
    # initialize page_ranks
    INITIAL_POS = 1 / len(corpus)
    page_ranks = {page : INITIAL_POS for page in corpus}
    # loop until STOPPING_CONDITION is satisfied
    while cont:
        prev_PR = page_ranks.copy()
        cont = False
        for page in page_ranks:
            # get incoming pages
            incoming = get_incoming_pages(corpus, page)
            # calculate PR(p) using given formula
            i_sum_part = calculate_i_sum_part(corpus, prev_PR, incoming)
            page_ranks[page] = (1-damping_factor)/len(corpus) + i_sum_part * damping_factor
            # check STOPPING_CONDITION
            if abs(page_ranks[page] - prev_PR[page]) > STOPPING_CONDITION:
                cont = True
    sum_pos = sum(page_ranks.values())
    # normalize results
    page_ranks = {page : pos/sum_pos for page,pos in page_ranks.items()}
    print(sum(page_ranks.values()))
    return page_ranks


if __name__ == "__main__":
    main()
