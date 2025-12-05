
#Cette fonction prend en paramètre un dictionnaire dont les clés sont les thèmes et les valeurs sont les noms des pages accompagnés de leurs vues journalières.
#Elle retourne un dictionnaire dont les clefs sont les thèmes et les valeurs correspondent à la moyenne des vues par jour (par thème).
def sum_views(theme_sets):
	sums_themes = {}
	for key in theme_sets:
		sums_themes[key] = theme_sets[key][date_cols].sum(axis=0)/theme_sets[key].shape[0]
	return sums_themes

