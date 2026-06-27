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
    distribution = dict()
    n = len(corpus)
    links = corpus[page]

    # If page has no outgoing links, pretend it links to all pages
    if not links:
        links = set(corpus.keys())

    # Start every page with its share of the random-jump probability
    for p in corpus:
        distribution[p] = (1 - damping_factor) / n

    # Add the damped probability of following a link from `page`
    for link in links:
        distribution[link] += damping_factor / len(links)

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    counts = {page: 0 for page in corpus}

    # First sample: chosen uniformly at random
    page = random.choice(list(corpus.keys()))
    counts[page] += 1

    # Remaining samples: chosen based on previous sample's transition model
    for _ in range(n - 1):
        model = transition_model(corpus, page, damping_factor)
        pages = list(model.keys())
        weights = list(model.values())
        page = random.choices(pages, weights=weights, k=1)[0]
        counts[page] += 1

    # Convert counts into proportions
    return {page: count / n for page, count in counts.items()}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    n = len(corpus)
    ranks = {page: 1 / n for page in corpus}

    # A page with no links is treated as linking to every page (incl. itself)
    links = {
        page: (corpus[page] if corpus[page] else set(corpus.keys()))
        for page in corpus
    }

    # Precompute, for each page, the set of pages that link to it
    incoming = {page: set() for page in corpus}
    for page, outs in links.items():
        for out in outs:
            incoming[out].add(page)

    while True:
        new_ranks = {}
        for page in corpus:
            total = sum(ranks[i] / len(links[i]) for i in incoming[page])
            new_ranks[page] = (1 - damping_factor) / n + damping_factor * total

        max_diff = max(abs(new_ranks[p] - ranks[p]) for p in corpus)
        ranks = new_ranks

        if max_diff < 0.001:
            break

    return ranks


if __name__ == "__main__":
    main()
    