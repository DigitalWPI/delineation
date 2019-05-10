import os
import json
import sys
import csv
from copy import deepcopy
from helpers import list_to_string, numify_key, in_maxes, remove_key,\
	make_key_list, change_key_names, lambda_value_map, delete_keys, create_embargo_col
from listafy_str import fix_items


def convert_and_call_dsv(file_path,config):
	new_line		= config.new_line
	delimiter		= config.delimiter
	list_delimiter	= config.list_delimiter
	list_keys		= config.list_keys
	new_key_names	= config.new_key_names
	del_keys 		= config.del_keys
	lambdas			= config.lambdas
	update			= config.update
	with open(file_path,'r') as f:
		etd_string = f.read()
	all_records = read_deliniated_string(etd_string,new_line = new_line,delimiter=delimiter,list_delimiter=list_delimiter)
	for row in all_records:
		fix_items(row,list_keys,{},new_key_names,del_keys,lambdas,update)

	filename = os.path.basename(file_path)
	file_only, extension = os.path.splitext(filename)
	filename = file_only+'_converted.json'
	with open(f"exports/{filename}",'w') as outfile:
		outfile.write(json.dumps(all_records,indent=4))


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
				item = remove_blanks(item)
			new_row.append(item)
		if new_row != ['']:
			new.append(new_row)
	headings = new[0]
	final_list = []
	for row in new[1:]:
		name_val = {}
		for index,col in enumerate(row):
			name_val[headings[index]] = col
		final_list.append(name_val)
	return final_list

def remove_blanks(list_):
	for n,item in enumerate(list_):
		#list_[n] = item.strip()
		if not item.strip():
			list_[n] = ""
	if "" in list_:
		list_.remove("")
	return list_

if __name__ == '__main__':
	main(sys.argv[1])
