import pandas as pd
from behavioranalysis.utils import GOVERNMENT_ID


def compute_tables(path_to_data):
    consultation_data = pd.read_csv(path_to_data, parse_dates=["Création", "Modification"], index_col=0,
                                    dtype={"Titre": str, "Lié.à..": str, "Contenu": str, "Lien": str})
    consultation_data["Lié.à.."] = consultation_data["Lié.à.."].fillna("Unknown")
    consultation_data["Type.de.profil"] = consultation_data["Type.de.profil"].fillna("Unknown")

    consultation_data.loc[consultation_data["Id.de.l.auteur"] == GOVERNMENT_ID, "Type.de.profil"] = "Government"

    profile_types = consultation_data.groupby("Type.de.profil")

    user_counts = profile_types["Id.de.l.auteur"].unique().agg(len).to_frame()
    user_counts.rename(columns={'Id.de.l.auteur': 'Nb of contributors'}, inplace=True)

    user_activity_counts = consultation_data.groupby(["Type.de.profil", "Type.de.contenu"])["Identifiant"].agg(len).to_frame()
    user_activity_counts.rename(columns={"Identifiant": "Nb of contributions"}, inplace=True)

    return user_counts, user_activity_counts
