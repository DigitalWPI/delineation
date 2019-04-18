import sys
import json
import csv
import os
import collections
import config
import strip
from helpers import update_str_to_list, remove_key, make_key_list, change_key_names, lambda_value_map, delete_keys

def main(list_keys,deliated_strs,new_key_names,del_keys,lambdas,update):
	files =  os.listdir('imports')
	if '.keep' in files:
		files.remove('.keep')
	for path in files:
		path = 'imports/'+path

		print("Converting", path)

		try:
			change_file(path,list_keys,deliated_strs,new_key_names,del_keys,lambdas,update)
		except json.decoder.JSONDecodeError as e:
			if "Unexpected UTF-8 BOM" in str(e):
				print("\nStripping UTF-8 BOM from begining of file...\n")
				strip.strip(path)
				try:
					change_file(path,list_keys,deliated_strs,new_key_names,del_keys,lambdas,update)
				except Exception as e:
					print(f"Unable to do anything worth while to {path}. Riased {e}")


def change_file(path,list_keys,deliated_strs,new_key_names,del_keys,lambdas,update):
	with open (path,'r') as f:
		all_records = json.load(f)
	for row in all_records:
		fix_items(row,list_keys,deliated_strs,new_key_names,del_keys,lambdas,update)

	filename = os.path.basename(path)
	with open(f"exports/{filename}",'w') as outfile:
		outfile.write(json.dumps(all_records,indent=4))

def fix_items(row,str_lst,delstr_list,name_changes,to_delete_keys,lambdas,update):
	# print(json.dumps(row,indent=4),'\n\nmake_key_list')
	make_key_list(row,str_lst)
	# print(json.dumps(row,indent=4),'\n\nupdate_str_to_list')
	for delimiter,keys in delstr_list.items():
		update_str_to_list(row,keys,delimiter)
	# print(json.dumps(row,indent=4),'\n\nchange_key_names')
	change_key_names(row,name_changes)
	# print(json.dumps(row,indent=4),'\n\nlambdas')
	for lmbd in lambdas:
		lambda_value_map(row,lmbd)
	# print(json.dumps(row,indent=4),'\n\ndelete_keys')
	delete_keys(row,to_delete_keys)
	# print(json.dumps(row,indent=4),'\n\n')
	#final update
	row.update(update)

if __name__ == '__main__':
	#config.list_keys
	#config.deliated_strs
	#config.new_key_names
	#config.del_keys
	#config.lambdas
	#config.update
	main(config.list_keys,config.deliated_strs,config.new_key_names,config.del_keys,config.lambdas,config.update)
