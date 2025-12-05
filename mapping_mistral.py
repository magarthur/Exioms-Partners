import logging
from mistralai.client import MistralClient
import wikipediaapi
import sys
import os

def get_theme_mistral(page_name, lang, themes, wiki_objects, clean_page_title,theme_cache):
    key = f"{lang}_{page_name}"
    if key in theme_cache:
        return theme_cache[key]

    wiki = wiki_objects.get(lang)
    if not wiki:
        theme_cache[key] = "Other"
        return "Other"

    title_clean = clean_page_title(page_name)
    page = wiki.page(title_clean)
    if not page.exists():
        theme_cache[key] = "Other"
        return "Other"

    summary_text = page.summary[:2000]  # Tronquer pour éviter prompts trop longs

    prompt = f"""
### CONTEXTE
Tu es un classificateur de pages Wikipedia. Ta tâche est d'assigner **UN SEUL thème** à la page suivante, parmi cette liste :
{', '.join(themes)}.

### RÈGLES STRICTES
1. **Que le thème principal** :
   - Ne choisis que le thème principal, mais aide toi des sous-catégories pour choisir le bon thème.

3. **Format de réponse** :
   - Réponds **uniquement par le mot du thème**, sans explication.
   - Si aucun thème ne correspond, utilise "Other".

---
### DONNÉES À CLASSIFIER
Titre : {title_clean}
Résumé : {summary_text[:1500]}
---
Thème :
"""

    try:
        # -------------------------------
        # Redirection de stderr pour cacher les warnings
        # -------------------------------
        stderr_fileno = sys.stderr
        sys.stderr = open(os.devnull, 'w')

        response = client.chat(
            model="mistral-small",  # modèle déprécié
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=10
        )

        sys.stderr.close()
        sys.stderr = stderr_fileno
        # -------------------------------

        theme = response.choices[0].message.content.strip()
        if theme not in themes:
            logging.warning(f"Thème invalide '{theme}' pour {page_name}. Remplacé par 'Other'.")
            theme = "Other"

    except Exception as e:
        sys.stderr = stderr_fileno  # restaurer stderr en cas d'erreur
        logging.error(f"Erreur pour {page_name} ({lang}): {str(e)[:200]}")
        theme = "Other"

    theme_cache[key] = theme
    return theme