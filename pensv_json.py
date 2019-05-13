# this file was used for testing when the problem was first presented
import json
import sys
import csv
from copy import deepcopy
from helpers import list_to_string, numify_key, in_maxes, remove_key,\
	make_key_list, change_key_names, lambda_value_map, delete_keys, create_embargo_col

def example():
	with open('/Users/awscott/samveraStuff/notes/ETD_JSON_indented_no_res_some.json') as jsonfile:
		lists = json.load(jsonfile)
	# lists=lists[6:7]

	etd_string = prepare_csv(lists,new_line = "😊",delimiter='🍑',list_delimiter="☕")
	deep = read_deliniated_string(etd_string,new_line = "😊",delimiter='🍑',list_delimiter="☕")

	list_keys = ["urn","resources","committee","contributor","advisor","creator","dtype","title","abstract","department",'sdate']
	new_key_names = {"urn":"identifier","dtype":"resource_type","abstract":"description","sdate":"date_created","keywords":"keyword"}
	del_keys = ['adate','cdate','ddate','rdate','url','notices','availability']
	create_year = lambda row,key : row.update({"year":row[key][0][0:4]} if key == "date_created" else {})
	for row in deep:
		make_key_list(row,list_keys)
		change_key_names(row,new_key_names)
		lambda_value_map(row,create_year)
		delete_keys(row,del_keys)
		row["license"]=["https://creativecommons.org/licenses/by/4.0/"]

		# row["description"][0].replace('\\n','\n')
	print(f"{json.dumps(lists,indent=4)} \n\n{etd_string}\n\n{json.dumps(deep,indent=4)}")
	with open('exports/dirty50.json','w') as f:
		f.write(json.dumps(deep,indent=4))

def main(file_path):
	with open(file_path,'r') as f:
		etd_string = f.read()
	deep = read_deliniated_string(etd_string,new_line = "⛷",delimiter='⛸',list_delimiter="⛄")
	list_keys = ["urn","resources","committee","contributor","advisor","creator","dtype","title","abstract","department",'sdate']
	new_key_names = {"urn":"identifier","dtype":"resource_type","abstract":"description","sdate":"date_created","keywords":"keyword"}
	del_keys = ['adate','cdate','ddate','url','notices']
	create_year = lambda row,key : row.update({"year":row[key][0][0:4]} if key == "date_created" else {})
	create_embargo = lambda row,key : create_embargo_col(row) if key == 'rdate' else {}#add embargo stuff
	for row in deep:
		make_key_list(row,list_keys)
		change_key_names(row,new_key_names)
		lambda_value_map(row,create_year)
		lambda_value_map(row,create_embargo)
		delete_keys(row,del_keys)
		row["license"]=["https://creativecommons.org/licenses/by/4.0/"]

		# row["description"][0].replace('\\n','\n')
	#print(f"{etd_string}\n\n{json.dumps(deep,indent=4)}")
	with open(file_path+'_converted.json','w') as f:
		f.write(json.dumps(deep,indent=4))

def read_deliniated_string(entire_file_as_string,new_line = "💩",delimiter='👙',list_delimiter="{|,|}"):
	etds = entire_file_as_string
	etds = etds.split(new_line)
	new = []
	for item in etds:
		list_  = item.split(delimiter)
		new_row = []
		for item in list_:
			if list_delimiter in item:
				item = item.split(list_delimiter)
			new_row.append(item)
		new.append(new_row)
	headings = new[0]
	final_list = []
	for row in new[1:]:
		name_val = {}
		for index,col in enumerate(row):
			name_val[headings[index]] = col
		final_list.append(name_val)
	return final_list

def prepare_csv(list_of_dict,new_line = None,delimiter = None,list_delimiter = None,maxes = None,truncate = True):
	""" this dumps the dict into a file with given delimiters, it does not encapsulate in quotes. it isnt smart"""
	
	#kwarg defaults, dont want pointer errors
	if new_line is None:
		new_line = '\n'
	if delimiter is None:
		delimiter = ','
	if list_delimiter is None:
		list_delimiter = ';'
	if maxes is None:
		maxes = {}
	etd_string = ""

	#remove_key
	list_of_flattened_dicts = []
	for row in list_of_dict:
		mega_dict = {}
		for key in row:
			max_key =  in_maxes(key,maxes)
			if max_key:
				flat_dict = flatten_list_of_dict(row[key],maxes[max_key],row[str(key)+'_keys']) #author1,author2,author3
				mega_dict.update(flat_dict)
			else:
				if isinstance(row[key],list):
					mega_dict.update({key:list_to_string(row[key],list_delimiter)}) #keywords : [sceince,math,physics]
				else:
					mega_dict.update({key:row[key]}) #normal case ie title: 'the title'
		list_of_flattened_dicts.append(mega_dict)
	all_keys = list(mega_dict.keys()) #hopefully still in scope


	if truncate:
		pass#file.write(list_to_string(all_keys,delimiter)+new_line)
		etd_string += list_to_string(all_keys,delimiter) + new_line
	for flat in list_of_flattened_dicts:
		big_list = []
		for key in all_keys:
			value = ""
			if key in flat:
				value = flat[key]
			big_list.append(value) # ensure its in order, and always has correct amount of items.
		etd_string += list_to_string(big_list,delimiter) + new_line
	etd_string = etd_string[:etd_string.rfind(new_line)] #get rid of final newline
	return etd_string

def flatten_list_of_dict(lod,max_lod,keys):
	#lod stands for like of dict, ie: [{name:joe,age:12},{name:banjoe,age:20},{name:jim,age:None}]
	#max_lod would be 2 if this was the most name/age dicts we had in this case cause its the max index of the list

	new_flat = {}
	n = 0
	for item in lod:
		n +=1
		for key in keys:
			try:
				new_flat.update({numify_key(key,n):item[key]})
			except:
				print(new_flat,item,lod)
				raise
	if n < max_lod+1:
		n = n + 1
		for key in keys:
			new_flat.update({numify_key(key,n):''})
			if n >= max_lod+1:
				break
	return new_flat


if __name__ == '__main__':
	main(sys.argv[1])
