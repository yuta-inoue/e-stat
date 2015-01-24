# -*- coding:utf-8 -*-
import csv
import math
def export_csv_dict(objects,path):
	u"""
	objectを指定したpathにエクスポートする
	"""
	with open(path,'w') as f:
		w = csv.DictWriter(f,objects.keys())
		w.writeheader()
		w.writerow(objects)
def export_csv_list(objects,folder_path,fname):
	i = 0
	#title_row = []
	row = []
	for val in objects:
		if i%1000==0:
			suffix = math.floor(i / 1000)
			writer = csv.writer(open(folder_path+fname+'%d.csv'%suffix, 'w'),quoting=csv.QUOTE_ALL)
		for key in val:
			#if i == 0:
			#	title = key
			#	title_row.append(title)
			row.append(val[key])
		#title_row.append('VALUES')
		#if i == 0:
		#	writer.writerow(title_row)
		writer.writerow(row)
		row = []
		i += 1
