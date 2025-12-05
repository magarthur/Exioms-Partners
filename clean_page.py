import re

def clean_page_title(raw_title):
    """
    Transforme un nom de page brut en titre valide pour Wikipedia API
    - remplace les underscores par des espaces
    - supprime les apostrophes et caractères problématiques
    - gère les guillemets échappés
    """
    title = raw_title.replace("_", " ")        # underscore -> espace
    title = title.replace('\\"', '"')          # guillemets échappés
    title = title.replace("'", "")             # supprimer les apostrophes
    return title