
# fonction permettant de sélectionner toutes les lignes qui possèdent all-access, spider et all-agents
def bot_and_human(train):
	train_all_access = train[train['access']=='all-access'].copy()
	agents_per_page = train_all_access.groupby(['page_name','lang'])['agent'].unique()

	valid_pairs = agents_per_page[agents_per_page.apply(lambda x: set(['all-agents', 'spider']).issubset(set(x)))].index
	# On sélectionne les couples (page_name, lang) qui possèdent à la fois :
	#- 'all-agents'
	#- 'spider' que fait cette fonction ?

	train_clean = train_all_access.set_index(['page_name', 'lang']).loc[valid_pairs].reset_index()
	# on filtre le dataset pour ne garder que les lignes correspondant aux couples (page_name, lang) identifiées comme complets
	return train_clean

	

