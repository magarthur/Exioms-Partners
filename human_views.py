import pandas as pd

def human_views(train, date_cols):
	df_clean = train.drop_duplicates(subset=['page_name', 'lang', 'agent']) # On s'assure ici qu'il n'y a pas de doublon
	df_clean = df_clean.set_index(['page_name', 'lang'])	# On transforme l'index en étiquette, permet d'eviter des erreurs de décalage

	df_all = df_clean.loc[df_clean['agent'] == 'all-agents', date_cols]	# on sépare ici robots et humains
	df_spider = df_clean.loc[df_clean['agent'] == 'spider', date_cols]

	df_human = df_all.sub(df_spider, fill_value=0).reset_index() # on soustrait df_spider à df_all

	return df_human






