import re

import pandas as pd
import matplotlib.pyplot as plt

from behavioranalysis.utils import sort_dict_by_value, compute_similarity_ratio


def display(path_to_data):
    consultation_data = pd.read_csv(path_to_data, parse_dates=["Création", "Modification"], index_col=0,
                                    dtype={"Identifiant": str, "Titre": str, "Lié.à..": str, "Contenu": str, "Lien": str})
    consultation_data["Lié.à.."] = consultation_data["Lié.à.."].fillna("Unknown")

    argument_replies = {key: 0 for key in consultation_data.loc[consultation_data["Type.de.contenu"] == "Proposition"]["Identifiant"]}
    modification_replies = {key: 0 for key in consultation_data.loc[consultation_data["Type.de.contenu"] == "Proposition"]["Identifiant"]}
    source_replies = {key: 0 for key in consultation_data.loc[consultation_data["Type.de.contenu"] == "Proposition"]["Identifiant"]}
    vote_replies = {key: 0 for key in consultation_data.loc[consultation_data["Type.de.contenu"] == "Proposition"]["Identifiant"]}

    for index, activity in consultation_data.loc[(~consultation_data["Lié.à.."].str.contains("Proposition")) &
                                                 (consultation_data["Lié.à.."] != "Unknown")].iterrows():
        while "Proposition" not in activity.loc["Lié.à.."]:
            parent_post_identifier = re.search('\d+', activity.loc["Lié.à.."]).group()
            parent_content_type = re.search('Proposition|Modification|Source|Argument', activity.loc["Lié.à.."]).group()

            activity.loc["Lié.à.."] = consultation_data.loc[(consultation_data["Identifiant"] == parent_post_identifier) &
                                                            (consultation_data["Type.de.contenu"] == parent_content_type)
                                                            ].iloc[0]["Lié.à.."]

    propositions = consultation_data.loc[consultation_data["Type.de.contenu"] == "Proposition"]

    for index, prop in propositions.iterrows():
        post_identifier = prop.loc["Identifiant"]
        replies = consultation_data.loc[consultation_data["Lié.à.."] == f'Proposition "{post_identifier}"']

        argument_replies[post_identifier] = len(replies.loc[replies["Type.de.contenu"] == "Argument"].index)
        modification_replies[post_identifier] = len(replies.loc[replies["Type.de.contenu"] == "Modification"].index)
        source_replies[post_identifier] = len(replies.loc[replies["Type.de.contenu"] == "Source"].index)
        vote_replies[post_identifier] = len(replies.loc[replies["Type.de.contenu"] == "Vote"].index)


    argument_replies = sort_dict_by_value(argument_replies)
    modification_replies = sort_dict_by_value(modification_replies)
    source_replies = sort_dict_by_value(source_replies)
    vote_replies = sort_dict_by_value(vote_replies)

    argument_modification_similarity = []
    argument_source_similarity = []
    argument_vote_similarity = []
    modification_source_similarity = []
    modification_vote_similarity = []
    source_vote_similarity = []

    ratios = [x / 100.0 for x in range(1, 101)]

    for ratio in ratios:
        argument_modification_similarity.append(compute_similarity_ratio(list(argument_replies.keys()),
                                                                         list(modification_replies.keys()), ratio))
        argument_source_similarity.append(compute_similarity_ratio(list(argument_replies.keys()),
                                                                   list(source_replies.keys()), ratio))
        argument_vote_similarity.append(compute_similarity_ratio(list(argument_replies.keys()),
                                                                 list(vote_replies.keys()), ratio))
        modification_source_similarity.append(compute_similarity_ratio(list(modification_replies.keys()),
                                                                       list(source_replies.keys()), ratio))
        modification_vote_similarity.append(compute_similarity_ratio(list(modification_replies.keys()),
                                                                     list(vote_replies.keys()), ratio))
        source_vote_similarity.append(compute_similarity_ratio(list(source_replies.keys()),
                                                               list(vote_replies.keys()), ratio))

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(ratios, argument_modification_similarity, c='b', label='Argument/Modification')
    ax.plot(ratios, argument_source_similarity, c='g', label='Argument/Source')
    ax.plot(ratios, argument_vote_similarity, c='k', label='Argument/Vote')
    ax.plot(ratios, modification_source_similarity, c='r', label='Modification/Source')
    ax.plot(ratios, modification_vote_similarity, c='m', label='Modification/Vote')
    ax.plot(ratios, source_vote_similarity, c='c', label='Source/Vote')

    plt.legend(loc=0)
    plt.xlabel("Ratio of most replied proposals", fontsize='large')
    plt.ylabel("$\it{S_{reply}}$", fontsize='large')
    plt.tight_layout()
    plt.show()
