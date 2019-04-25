#this is a comment, config for tweak
import helpers
list_keys = [
	"urn",
	"committee",
	"creator",
	"dtype",
	"title",
	"abstract",
	"department",
	"sdate"
]

deliated_strs = {
	# the char at the begining is the seperator for the list so "Scott, Alfred☕O'Brien, Emily" in this case
	# the items in [] are the keys to convert into lists
	'☕' : [ "contributor", "advisor", "keywords", "resources" ]
	#more could be added here like so, but ensure each list ends with a comman except the last
	#'👍' : ["some metadata field","some other metadata field"],
	#'🙂' : ["metadata field three","some fourth metadata field"]
	}
new_key_names = { #left is original name, right is desired name
	"urn":"identifier",
	"dtype":"resource_type",
	"abstract":"description",
	"sdate":"date_created",
	"keywords":"keyword"
}

del_keys = [ #things to remove
	'adate',
	'cdate',
	'ddate',
	'url',
	'notices'
]
lambdas = [ #ignore these inline fuction definitions
	lambda row,key : row.update({"year":row[key][0][0:4]} if key == "date_created" else {}),
	lambda row,key : helpers.create_embargo_col(row) if key == 'rdate' else {}#add embargo stuff
]
update = { #new things to add
	"license":["https://creativecommons.org/licenses/by/4.0/"]
}