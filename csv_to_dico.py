def csv_to_dico(csv,theme_sets):
	for e in csv['theme'].unique():
		theme_sets[e] = csv[csv['theme'] == e].iloc[:, [i for i in range(csv.shape[1]) if i != 552]]
		
    	

