import matplotlib.pyplot as plt

from behavioranalysis.pagerank_builder import compute_pageranks
from behavioranalysis.utils import compute_similarity_ratio


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

    ratios = [x / 100.0 for x in range(1, 101)]

    argument_modification_similarity = []
    argument_source_similarity = []
    argument_vote_similarity = []
    modification_source_similarity = []
    modification_vote_similarity = []
    source_vote_similarity = []

    for ratio in ratios:
        argument_modification_similarity.append(compute_similarity_ratio(list(argument_pageranks.keys()),
                                                                         list(modification_pageranks.keys()), ratio))
        argument_source_similarity.append(compute_similarity_ratio(list(argument_pageranks.keys()),
                                                                   list(source_pageranks.keys()), ratio))
        argument_vote_similarity.append(compute_similarity_ratio(list(argument_pageranks.keys()),
                                                                 list(vote_pageranks.keys()), ratio))
        modification_source_similarity.append(compute_similarity_ratio(list(modification_pageranks.keys()),
                                                                       list(source_pageranks.keys()), ratio))
        modification_vote_similarity.append(compute_similarity_ratio(list(modification_pageranks.keys()),
                                                                     list(vote_pageranks.keys()), ratio))
        source_vote_similarity.append(compute_similarity_ratio(list(source_pageranks.keys()),
                                                               list(vote_pageranks.keys()), ratio))

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(ratios, argument_modification_similarity, c='b', label='Argument/Modification')
    ax.plot(ratios, argument_source_similarity, c='g', label='Argument/Source')
    ax.plot(ratios, argument_vote_similarity, c='k', label='Argument/Vote')
    ax.plot(ratios, modification_source_similarity, c='r', label='Modification/Source')
    ax.plot(ratios, modification_vote_similarity, c='m', label='Modification/Vote')
    ax.plot(ratios, source_vote_similarity, c='c', label='Source/Vote')

    plt.legend(loc=0)
    plt.xlabel("Ratio of best PageRanks", fontsize='large')
    plt.ylabel("$\it{S_{PageRank}}$", fontsize='large')
    plt.tight_layout()
    plt.show()
