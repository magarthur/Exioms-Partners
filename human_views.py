import pandas as pd

def human_views(train, date_cols):
	df_clean = train.drop_duplicates(subset=['page_name', 'lang', 'agent']) # On s'assure ici qu'il n'y a pas de doublon
	df_clean = df_clean.set_index(['page_name', 'lang'])	# On transforme l'index en étiquette, permet d'eviter des erreurs de décalage

	df_all = df_clean.loc[df_clean['agent'] == 'all-agents', date_cols]	# on sépare ici robots et humains
	df_spider = df_clean.loc[df_clean['agent'] == 'spider', date_cols]

	df_human = df_all.sub(df_spider, fill_value=0) # on soustrait df_spider à df_all

	meta_cols = ['Page', 'project', 'access']	# Permet de rajouter les différentes infos de la page au dataset final
	df_meta = df_clean.loc[df_clean['agent'] == 'all-agents', meta_cols]

	train_human_views = pd.concat([df_meta, df_human], axis=1).reset_index()	#on concatène le tout puis on redéfinit un index.

	return train_human_views




