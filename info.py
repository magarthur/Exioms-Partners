def info(train):
	# On découpe la colonne Page en 4 parties en partant de la fin
	split_col = train['Page'].str.rsplit('_', n=3, expand=True)

	train['page_name'] = split_col[0]      # ex : "3C"
	train['project']   = split_col[1]      # ex : "zh.wikipedia.org"
	train['access']    = split_col[2]      # ex : "all-access"
	train['agent']     = split_col[3]      # ex : "spider"

#Ces 5 nouvelles informations sont ajoutées à la fin du dataset