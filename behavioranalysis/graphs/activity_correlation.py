import pandas as pd
import matplotlib.pyplot as plt
from behavioranalysis import utils


def display(path_to_data):
    consultation_data = pd.read_csv(path_to_data, parse_dates=["Création", "Modification"], index_col=0,
                                    dtype={"Titre": str, "Lié.à..": str, "Contenu": str, "Lien": str})
    consultation_data["Lié.à.."] = consultation_data["Lié.à.."].fillna("Unknown")

    arguments = consultation_data.loc[consultation_data["Type.de.contenu"] == "Argument"]
    modifications = consultation_data.loc[consultation_data["Type.de.contenu"] == "Modification"]
    propositions = consultation_data.loc[consultation_data["Type.de.contenu"] == "Proposition"]
    sources = consultation_data.loc[consultation_data["Type.de.contenu"] == "Source"]
    votes = consultation_data.loc[consultation_data["Type.de.contenu"] == "Vote"]

    argument_count = arguments["Id.de.l.auteur"].value_counts().rename("Number.of.arguments")
    modification_count = modifications["Id.de.l.auteur"].value_counts().rename("Number.of.modifications")
    proposition_count = propositions["Id.de.l.auteur"].value_counts().rename("Number.of.propositions")
    source_count = sources["Id.de.l.auteur"].value_counts().rename("Number.of.sources")
    vote_count = votes["Id.de.l.auteur"].value_counts().rename("Number.of.votes")

    counts = pd.concat([argument_count, modification_count, proposition_count, source_count, vote_count], axis=1).fillna(0)

    argument_count_dict_ordered = utils.sort_dict_by_value(counts["Number.of.arguments"].to_dict())
    modification_count_dict_ordered = utils.sort_dict_by_value(counts["Number.of.modifications"].to_dict())
    proposition_count_dict_ordered = utils.sort_dict_by_value(counts["Number.of.propositions"].to_dict())
    source_count_dict_ordered = utils.sort_dict_by_value(counts["Number.of.sources"].to_dict())
    vote_count_dict_ordered = utils.sort_dict_by_value(counts["Number.of.votes"].to_dict())

    ratios = [x / 100.0 for x in range(1, 101)]

    argument_modification_similarity = []
    argument_proposition_similarity = []
    argument_source_similarity = []
    argument_vote_similarity = []
    modification_proposition_similarity = []
    modification_source_similarity = []
    modification_vote_similarity = []
    proposition_source_similarity = []
    proposition_vote_similarity = []
    source_vote_similarity = []

    for ratio in ratios:
        argument_modification_similarity.append(utils.compute_similarity_ratio(list(argument_count_dict_ordered.keys()),
                                                                               list(modification_count_dict_ordered.keys()), ratio))
        argument_proposition_similarity.append(utils.compute_similarity_ratio(list(argument_count_dict_ordered.keys()),
                                                                              list(proposition_count_dict_ordered.keys()), ratio))
        argument_source_similarity.append(utils.compute_similarity_ratio(list(argument_count_dict_ordered.keys()),
                                                                         list(source_count_dict_ordered.keys()), ratio))
        argument_vote_similarity.append(utils.compute_similarity_ratio(list(argument_count_dict_ordered.keys()),
                                                                       list(vote_count_dict_ordered.keys()), ratio))
        modification_proposition_similarity.append(utils.compute_similarity_ratio(list(modification_count_dict_ordered.keys()),
                                                                                  list(proposition_count_dict_ordered.keys()), ratio))
        modification_source_similarity.append(utils.compute_similarity_ratio(list(modification_count_dict_ordered.keys()),
                                                                             list(source_count_dict_ordered.keys()), ratio))
        modification_vote_similarity.append(utils.compute_similarity_ratio(list(modification_count_dict_ordered.keys()),
                                                                           list(vote_count_dict_ordered.keys()), ratio))
        proposition_source_similarity.append(utils.compute_similarity_ratio(list(proposition_count_dict_ordered.keys()),
                                                                            list(source_count_dict_ordered.keys()), ratio))
        proposition_vote_similarity.append(utils.compute_similarity_ratio(list(proposition_count_dict_ordered.keys()),
                                                                          list(vote_count_dict_ordered.keys()), ratio))
        source_vote_similarity.append(utils.compute_similarity_ratio(list(source_count_dict_ordered.keys()),
                                                                     list(vote_count_dict_ordered.keys()), ratio))

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(ratios, argument_modification_similarity, c='b', label='Argument/Modification')
    ax.plot(ratios, argument_proposition_similarity, c='gold', label='Argument/Proposal')
    ax.plot(ratios, argument_source_similarity, c='g', label='Argument/Source')
    ax.plot(ratios, argument_vote_similarity, c='k', label='Argument/Vote')
    ax.plot(ratios, modification_proposition_similarity, c='darkorange', label='Modification/Proposal')
    ax.plot(ratios, modification_source_similarity, c='r', label='Modification/Source')
    ax.plot(ratios, modification_vote_similarity, c='m', label='Modification/Vote')
    ax.plot(ratios, proposition_source_similarity, c='grey', label='Proposal/Source')
    ax.plot(ratios, proposition_vote_similarity, c='olive', label='Proposal/Vote')
    ax.plot(ratios, source_vote_similarity, c='c', label='Source/Vote')

    plt.legend(loc=0)
    plt.xlabel("Ratio $\it{r}$ of most active contributors", fontsize='large')
    plt.ylabel("$\it{S_{activity}}$", fontsize='large')
    plt.tight_layout()
    plt.show()
