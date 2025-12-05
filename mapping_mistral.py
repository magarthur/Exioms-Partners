import logging
from mistralai.client import MistralClient
import wikipediaapi
import sys
import os

def get_theme_mistral(page_name, lang, themes, wiki_objects, clean_page_title, theme_cache, client):
    # 1. Vérification du cache
    key = f"{lang}_{page_name}"
    if key in theme_cache:
        return theme_cache[key]

    # 2. Vérification objets Wiki
    wiki = wiki_objects.get(lang)
    if not wiki:
        theme_cache[key] = "Other"
        return "Other"

    # 3. Récupération Page
    title_clean = clean_page_title(page_name)
    page = wiki.page(title_clean)
    if not page.exists():
        theme_cache[key] = "Other"
        return "Other"

    summary_text = page.summary[:2000]

    # 4. Prompt
    prompt = f"""
### CONTEXTE
Tu es un classificateur de pages Wikipedia. Ta tâche est d'assigner **UN SEUL thème** à la page suivante, parmi cette liste :
{', '.join(themes)}.

### RÈGLES STRICTES
1. **Que le thème principal** :
   - Ne choisis que le thème principal.
2. **Format de réponse** :
   - Réponds **uniquement par le mot du thème**, sans explication.
   - Si aucun thème ne correspond, utilise "Other".

---
### DONNÉES À CLASSIFIER
Titre : {title_clean}
Résumé : {summary_text[:1500]}
---
Thème :
"""

    theme = "Other" # Valeur par défaut
    
    # On sauvegarde la sortie d'erreur standard actuelle
    original_stderr = sys.stderr 
    null_file = None

    try:
        # -------------------------------
        # Redirection sécurisée de stderr
        # -------------------------------
        try:
            null_file = open(os.devnull, 'w')
            sys.stderr = null_file
            
            # Appel API
            response = client.chat(
                model="mistral-small-latest", # "mistral-small" est souvent obsolète, utilise latest
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=10
            )
            
            theme = response.choices[0].message.content.strip()

        finally:
            # Ce bloc s'exécute TOUJOURS, même si client.chat plante.
            # On restaure la sortie d'erreur AVANT de gérer les exceptions
            sys.stderr = original_stderr
            if null_file:
                null_file.close()
        # -------------------------------

        # Validation (Maintenant que stderr est restauré, on peut logger si besoin)
        if theme not in themes:
            logging.warning(f"Thème invalide '{theme}' pour {page_name}. Remplacé par 'Other'.")
            theme = "Other"

    except Exception as e:
        # Ici stderr est rétabli, donc on verra bien l'erreur dans la console
        logging.error(f"Erreur pour {page_name} ({lang}): {str(e)[:200]}")
        theme = "Other"

    theme_cache[key] = theme
    return theme
