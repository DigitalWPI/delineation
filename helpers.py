from copy import deepcopy
from datetime import datetime, date

def list_to_string(list,delimiter):
	""" takes a list and a delimiter and turns list into a string """
	string = ""
	for i in list:
		string += str(i) + delimiter
	string = string[:string.rfind(delimiter)]
	return string

def str_to_list(string,delimiter):
	if not string: # catches null or empty strings
		return []
	array = string.split(delimiter)
	if '' in array:
		array.remove('')
	return array

def update_str_to_list(row,keys,delimiter):
	for key in keys:
		row[key] = str_to_list(row[key],delimiter)

def numify_key(key,number):
	return str(key)+str(number)

def in_maxes(key,maxes):
	for k in maxes:
		if k == 'max_' + str(key):
			return k
	return False

def remove_key(dictionary,keys):
	""" creates new dict with out the key in it """
	new = deepcopy(dictionary)
	for i in keys:	
		try:
			del new[i]
		except Exception as e:
			print (new)
			raise e
	return new

def make_key_list(row,keys,name_map = None):
	#modifies dict to make things rows
	for key in keys:

		if isinstance(row[key],list):
			pass
		elif row[key] is None or row[key] == "":
			row[key] = []
		else:
			row[key] = [row[key]]

def change_key_names(row,name_map = None):
	if name_map is None:
		name_map = {}
	keys = list(row.keys())
	for key in keys:
		#if user wants fields renamed pass in dict {"original name": "updated name"}
		if key in name_map:
			row[name_map[key]] = row[key]
			del row[key]
		else:
			result = row[key]	#
			del row[key]		# for stupid sorting
			row[key] = result	#

def lambda_value_map(row,proc):
	keys = list(row.keys())
	for key in keys:
		proc(row,key)

def delete_keys(row,keys):
	for key in keys:
		del row[key]
def create_embargo_col(row):
	"""
	takes in a record and modifies the record to now have embargo fields instead of
	rdate type stuff. 
	{...,'rdate' : '2015-01-01','availability': 'restricted'} will become:
	
	{...,
	'embargo' : true,
	'embargo_release_date' : '2015-01-01',
	'embargo_visibility': [
		'authenticated',
		'public'
		]
	} 
	goes from auth to pub, and from pub to pub, and from private to auth. unless specified.
	"""
	restrictions = ['public','authenticated','private']
	release_day = row['rdate']

	current_restriction = row['availability']
	if current_restriction == "unrestricted":
		current_restriction = 0
	elif current_restriction == "restricted":
		current_restriction = 1
	else:
		current_restriction = 2

	post_restriction = 0

	if current_restriction == 0:
		if release_day == '0000-00-00' or datetime.strptime(row['rdate'],"%Y-%m-%d") < datetime.today():
			#perfect we dont need any restrictive stuff
			row['embargo'] = False
			row['embargo_release_date'] = None
			del row['rdate']
			del row['availability']
			return row
		else: # edge case given by Aaron Neslin Tuesday May 28th 2019
			# case: future rdate, but says 'unrestricted' : keep restricted for ever.
			row['embargo'] = True
			row['embargo_visibility'] = ['private','authenticated'] #make current state its final state
			row['embargo_release_date'] = '1776-07-04' # release date in the past (it wont show up)
			print(f"WARNING: restricting previously unrestricted work: {row['identifier']}",\
				f"\n{release_day}{row['availability']}",\
				"\nSend Email to Aaron Neslin / Emily O'Brien about this")
			del row['rdate']
			del row['availability']
			return row
	row['embargo'] = True
	row['embargo_visibility'] = [restrictions[current_restriction], restrictions[post_restriction]]
	row['embargo_release_date'] = release_day
	if release_day == '0000-00-00': # needs to be restricted
		# edge case, restrict for ever if this date is used.
		row['embargo_visibility'] = ['private',restrictions[current_restriction]] #make current state its final state
		row['embargo_release_date'] = '1776-07-04' # release date in the past (it wont show up)

	del row['rdate']
	del row['availability']
	return row
