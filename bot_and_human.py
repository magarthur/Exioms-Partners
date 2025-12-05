def bot_and_human(train):
	train_all_access = train[train['access']=='all-access'].copy()
	agents_per_page = train_all_access.groupby(['page_name','lang'])['agent'].unique()

	valid_pairs = agents_per_page[agents_per_page.apply(lambda x: set(['all-agents', 'spider']).issubset(set(x)))].index

	train_clean = train_all_access.set_index(['page_name', 'lang']).loc[valid_pairs].reset_index()
	return train_clean

	
