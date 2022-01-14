import re
import pandas as pd
import matplotlib.pyplot as plt

from behavioranalysis.utils import GOVERNMENT_ID


def generate_quartiles(df):
    result_df = pd.DataFrame()

    result_df["Q1.argument"] = df["Nb.Arguments"].quantile(q=0.25, interpolation='lower')
    result_df["MED.argument"] = df["Nb.Arguments"].quantile(q=0.5, interpolation='lower')
    result_df["Q3.argument"] = df["Nb.Arguments"].quantile(q=0.75, interpolation='lower')

    result_df["Q1.modification"] = df["Nb.Modifications"].quantile(q=0.25, interpolation='lower')
    result_df["MED.modification"] = df["Nb.Modifications"].quantile(q=0.5, interpolation='lower')
    result_df["Q3.modification"] = df["Nb.Modifications"].quantile(q=0.75, interpolation='lower')

    result_df["Q1.source"] = df["Nb.Sources"].quantile(q=0.25, interpolation='lower')
    result_df["MED.source"] = df["Nb.Sources"].quantile(q=0.5, interpolation='lower')
    result_df["Q3.source"] = df["Nb.Sources"].quantile(q=0.75, interpolation='lower')

    result_df["Q1.vote"] = df["Nb.Votes"].quantile(q=0.25, interpolation='lower')
    result_df["MED.vote"] = df["Nb.Votes"].quantile(q=0.5, interpolation='lower')
    result_df["Q3.vote"] = df["Nb.Votes"].quantile(q=0.75, interpolation='lower')

    return result_df


def display(path_to_data):
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 200)

    consultation_data = pd.read_csv(path_to_data, parse_dates=["Création", "Modification"], index_col=0,
                                    dtype={"Identifiant": str, "Titre": str, "Lié.à..": str, "Contenu": str, "Lien": str})
    consultation_data["Lié.à.."] = consultation_data["Lié.à.."].fillna("Unknown")

    argument_replies = {key: 0 for key in
                        consultation_data.loc[consultation_data["Type.de.contenu"] == "Proposition"]["Identifiant"]}
    modification_replies = {key: 0 for key in
                            consultation_data.loc[consultation_data["Type.de.contenu"] == "Proposition"]["Identifiant"]}
    source_replies = {key: 0 for key in
                      consultation_data.loc[consultation_data["Type.de.contenu"] == "Proposition"]["Identifiant"]}
    vote_replies = {key: 0 for key in
                    consultation_data.loc[consultation_data["Type.de.contenu"] == "Proposition"]["Identifiant"]}

    for index, activity in consultation_data.loc[(~consultation_data["Lié.à.."].str.contains("Proposition")) &
                                                 (consultation_data["Lié.à.."] != "Unknown")].iterrows():
        while "Proposition" not in activity.loc["Lié.à.."]:
            parent_post_identifier = re.search('\d+', activity.loc["Lié.à.."]).group()
            parent_content_type = re.search('Proposition|Modification|Source|Argument', activity.loc["Lié.à.."]).group()

            activity.loc["Lié.à.."] = consultation_data.loc[
                (consultation_data["Identifiant"] == parent_post_identifier) &
                (consultation_data["Type.de.contenu"] == parent_content_type)].iloc[0]["Lié.à.."]

    propositions = consultation_data.loc[consultation_data["Type.de.contenu"] == "Proposition"]

    for index, prop in propositions.iterrows():
        post_identifier = prop.loc["Identifiant"]
        replies = consultation_data.loc[consultation_data["Lié.à.."] == f'Proposition "{post_identifier}"']

        argument_replies[post_identifier] = len(replies.loc[replies["Type.de.contenu"] == "Argument"].index)
        modification_replies[post_identifier] = len(replies.loc[replies["Type.de.contenu"] == "Modification"].index)
        source_replies[post_identifier] = len(replies.loc[replies["Type.de.contenu"] == "Source"].index)
        vote_replies[post_identifier] = len(replies.loc[replies["Type.de.contenu"] == "Vote"].index)

    propositions.loc[:, ("Nb.Arguments",)] = propositions.apply(lambda row: argument_replies[row["Identifiant"]], axis=1)
    propositions.loc[:, ("Nb.Modifications",)] = propositions.apply(lambda row: modification_replies[row["Identifiant"]], axis=1)
    propositions.loc[:, ("Nb.Sources",)] = propositions.apply(lambda row: source_replies[row["Identifiant"]], axis=1)
    propositions.loc[:, ("Nb.Votes",)] = propositions.apply(lambda row: vote_replies[row["Identifiant"]], axis=1)

    propositions.loc[:, ("Part",)] = propositions.apply(lambda row: row["Catégorie"].split(" - ")[0].rstrip("er"), axis=1)
    propositions.loc[:, ("Chapter",)] = propositions.apply(lambda row: row["Catégorie"].split(" - ")[1].rstrip("er"), axis=1)
    propositions.loc[:, ("Section",)] = propositions.apply(lambda row: row["Catégorie"].split(" - ")[2].rstrip("er"), axis=1)
    propositions.loc[:, ("GOV",)] = propositions.apply(lambda row: True if (row["Id.de.l.auteur"] == GOVERNMENT_ID) else False, axis=1)

    propositions_by_part = propositions.loc[:, ["Part",
                                                "Nb.Arguments",
                                                "Nb.Modifications",
                                                "Nb.Sources",
                                                "Nb.Votes",
                                                "GOV"]].groupby(["Part"])
    propositions_by_chapter = propositions.loc[:, ["Part",
                                                   "Chapter",
                                                   "Nb.Arguments",
                                                   "Nb.Modifications",
                                                   "Nb.Sources",
                                                   "Nb.Votes",
                                                   "GOV"]].groupby(["Part", "Chapter"])
    propositions_by_section = propositions.loc[:, ["Part",
                                                   "Chapter",
                                                   "Section",
                                                   "Nb.Arguments",
                                                   "Nb.Modifications",
                                                   "Nb.Sources",
                                                   "Nb.Votes",
                                                   "GOV"]].groupby(["Part", "Chapter", "Section"])

    result_by_part = generate_quartiles(propositions_by_part)
    result_by_chapter = generate_quartiles(propositions_by_chapter)
    result_by_section = generate_quartiles(propositions_by_section)

    gov_propositions = propositions.loc[propositions["GOV"]]

    gov_propositions_by_part = gov_propositions.loc[:, ["Part",
                                                        "Nb.Arguments",
                                                        "Nb.Modifications",
                                                        "Nb.Sources",
                                                        "Nb.Votes"]].groupby(["Part"])
    gov_propositions_by_chapter = gov_propositions.loc[:, ["Part",
                                                           "Chapter",
                                                           "Nb.Arguments",
                                                           "Nb.Modifications",
                                                           "Nb.Sources",
                                                           "Nb.Votes"]].groupby(["Part", "Chapter"])
    gov_propositions_by_section = gov_propositions.loc[:, ["Part",
                                                           "Chapter",
                                                           "Section",
                                                           "Nb.Arguments",
                                                           "Nb.Modifications",
                                                           "Nb.Sources",
                                                           "Nb.Votes"]].groupby(["Part", "Chapter", "Section"])

    gov_result_by_part = gov_propositions_by_part.quantile(q=0.5, interpolation='lower')
    gov_result_by_chapter = gov_propositions_by_chapter.quantile(q=0.5, interpolation='lower')
    gov_result_by_section = gov_propositions_by_section.quantile(q=0.5, interpolation='lower')

    return result_by_part, result_by_chapter, result_by_section, gov_result_by_part, gov_result_by_chapter, gov_result_by_section
