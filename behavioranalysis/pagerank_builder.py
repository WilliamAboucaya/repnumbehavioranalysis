import pandas as pd
import networkx as nx
import re
import logging

from behavioranalysis import utils


def argument(graph, post_author, original_post_author):
    edge_weight = 1 / graph.nodes[post_author]['arguments']

    if graph.has_edge(post_author, original_post_author):
        graph[post_author][original_post_author]["weight"] += edge_weight
    else:
        graph.add_edge(post_author, original_post_author, weight=edge_weight)


def modification(graph, post_author, original_post_author):
    edge_weight = 1 / graph.nodes[post_author]['modifications']

    if graph.has_edge(post_author, original_post_author):
        graph[post_author][original_post_author]["weight"] += edge_weight
    else:
        graph.add_edge(post_author, original_post_author, weight=edge_weight)


def proposition(graph, post_author, original_post_author):
    edge_weight = 0
    # graph.add_edge(post_author, original_post_author, weight=edge_weight, label="argument")


def source(graph, post_author, original_post_author):
    edge_weight = 1 / graph.nodes[post_author]['sources']

    if graph.has_edge(post_author, original_post_author):
        edge_weight = 1
        graph[post_author][original_post_author]["weight"] += edge_weight
    else:
        edge_weight = 1
        graph.add_edge(post_author, original_post_author, weight=edge_weight)


def vote(graph, post_author, original_post_author):
    edge_weight = 1 / graph.nodes[post_author]['votes']

    if graph.has_edge(post_author, original_post_author):
        graph[post_author][original_post_author]["weight"] += edge_weight
    else:
        graph.add_edge(post_author, original_post_author, weight=edge_weight)


def compute_pageranks(path_to_data):
    logging.basicConfig(level=logging.DEBUG)

    consultation_data = pd.read_csv(path_to_data,
                                    parse_dates=["Création", "Modification"],
                                    index_col=0, dtype={"Titre": str, "Lié.à..": str, "Contenu": str, "Lien": str})
    consultation_data["Lié.à.."] = consultation_data["Lié.à.."].fillna("Unknown")

    users = consultation_data["Id.de.l.auteur"].unique()

    argument_graph = nx.DiGraph()
    argument_graph.add_nodes_from(users)

    modification_graph = nx.DiGraph()
    modification_graph.add_nodes_from(users)

    proposition_graph = nx.DiGraph()
    proposition_graph.add_nodes_from(users)

    source_graph = nx.DiGraph()
    source_graph.add_nodes_from(users)

    vote_graph = nx.DiGraph()
    vote_graph.add_nodes_from(users)

    for user in users:
        activity_count = consultation_data.loc[consultation_data["Id.de.l.auteur"] == user][
            "Type.de.contenu"].value_counts()

        argument_graph.nodes[user]["arguments"] = activity_count.get("Argument", 0)
        modification_graph.nodes[user]["modifications"] = activity_count.get("Modification", 0)
        proposition_graph.nodes[user]["propositions"] = activity_count.get("Proposition", 0)
        source_graph.nodes[user]["sources"] = activity_count.get("Source", 0)
        vote_graph.nodes[user]["votes"] = activity_count.get("Vote", 0)

    switch_content_type = {
        "Argument": [argument, argument_graph],
        "Modification": [modification, modification_graph],
        "Proposition": [proposition, proposition_graph],
        "Source": [source, source_graph],
        "Vote": [vote, vote_graph]
    }

    pattern = re.compile('^(Proposition|Modification|Source|Argument) "\d+"$')

    logging.debug("Starting construction of the graph...")

    for index, activity in consultation_data.iterrows():
        related_to = activity.loc["Lié.à.."]
        content_type = activity.loc["Type.de.contenu"]
        post_author = activity.loc["Id.de.l.auteur"]

        if content_type == "Proposition":
            switch_content_type[content_type][0](switch_content_type[content_type][1], post_author, 0)
        elif pattern.match(related_to):
            original_post_identifier = int(re.search('\d+', related_to).group())
            original_content_type = re.search('Proposition|Modification|Source|Argument', related_to).group()
            original_post_author = consultation_data.loc[(consultation_data["Identifiant"] == original_post_identifier) &
                                                         (consultation_data[
                                                              "Type.de.contenu"] == original_content_type)].iloc[0][
                "Id.de.l.auteur"]

            switch_content_type[content_type][0](switch_content_type[content_type][1], post_author, original_post_author)
        else:
            logging.warning('The "Related to" field of %s %d is invalid.', content_type, activity.index)

        if index == 30000:
            logging.debug("20% done")
        elif index == 60000:
            logging.debug("40% done")
        elif index == 90000:
            logging.debug("60% done")
        elif index == 120000:
            logging.debug("80% done")

    logging.debug("The graph has successfully been constructed")

    argument_pageranks = utils.sort_dict_by_value(nx.pagerank(argument_graph))
    modification_pageranks = utils.sort_dict_by_value(nx.pagerank(modification_graph))
    source_pageranks = utils.sort_dict_by_value(nx.pagerank(source_graph))
    vote_pageranks = utils.sort_dict_by_value(nx.pagerank(vote_graph))

    argument_pageranks_filtered = argument_pageranks.copy()
    modification_pageranks_filtered = modification_pageranks.copy()
    source_pageranks_filtered = source_pageranks.copy()
    vote_pageranks_filtered = vote_pageranks.copy()

    for author in argument_pageranks:
        if (modification_graph.nodes[author]["modifications"] == 0) & (proposition_graph.nodes[author]["propositions"] == 0):
            del argument_pageranks_filtered[author]
            del source_pageranks_filtered[author]
        if proposition_graph.nodes[author]["propositions"] == 0:
            del modification_pageranks_filtered[author]
        if ((argument_graph.nodes[author]["arguments"] == 0) &
                (modification_graph.nodes[author]["modifications"] == 0) &
                (proposition_graph.nodes[author]["propositions"] == 0) &
                (source_graph.nodes[author]["sources"] == 0)):
            del vote_pageranks_filtered[author]

    return argument_pageranks_filtered, modification_pageranks_filtered, source_pageranks_filtered, vote_pageranks_filtered
