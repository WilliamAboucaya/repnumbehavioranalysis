import matplotlib.pyplot as plt
import numpy as np

from behavioranalysis.utils import GOVERNMENT_ID
from behavioranalysis.pagerank_builder import compute_pageranks


def pageranks_graph(pageranks):
    colors = ['r' if index == GOVERNMENT_ID else 'b' for index in list(pageranks.keys())]

    plt.bar(range(len(pageranks)), list(pageranks.values()), align='center')
    plt.xticks(range(len(pageranks)), list(pageranks.keys()))
    plt.xlabel("Users (sorted in ascending PageRank)", fontsize='large')
    plt.ylabel("PageRank", fontsize='large')
    plt.yscale("log")
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.tight_layout()
    plt.show()

def all_pageranks_graph(**kwargs):
    max_number_pageranks = max([len(pr) for pr in kwargs.values()])

    for activity, pageranks in kwargs.items():
        x = np.arange(0, max_number_pageranks, max_number_pageranks / len(pageranks))
        x = x[x < max_number_pageranks]
        plt.plot(x, list(pageranks.values()), label=activity)
    plt.xlabel("Users (sorted in ascending PageRank)", fontsize='large')
    plt.ylabel("PageRank", fontsize='large')
    plt.yscale("log")
    plt.legend()
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.tight_layout()
    plt.show()


def display(path_to_data, load_existing_pageranks: bool = False):
    if load_existing_pageranks:
        with open('./behavioranalysis/data/pageranks/argument_pageranks_filtered', 'r') as file:
            argument_pageranks = eval(file.read())

        with open('./behavioranalysis/data/pageranks/modification_pageranks_filtered', 'r') as file:
            modification_pageranks = eval(file.read())

        with open('./behavioranalysis/data/pageranks/source_pageranks_filtered', 'r') as file:
            source_pageranks = eval(file.read())

        with open('./behavioranalysis/data/pageranks/vote_pageranks_filtered', 'r') as file:
            vote_pageranks = eval(file.read())
    else:
        argument_pageranks, modification_pageranks, source_pageranks, vote_pageranks = compute_pageranks(path_to_data)

    all_pageranks_graph(Arguments=argument_pageranks, Modifications=modification_pageranks,
                        Sources=source_pageranks, Votes=vote_pageranks)
