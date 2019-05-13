#this is a comment, config for tweak
import helpers

new_line = "⛷"
delimiter='⛸'
list_delimiter="⛄"

#these things should always be made into a list, even if they have no delimiter
list_keys = [
	"urn",
	"committee",
	"creator",
	"dtype", # i.e. resource_type
	"title",
	"abstract",
	"department",
	"sdate",
	"advisor",
	"contributor",
	"resources"
]

new_key_names = { #left is original name, right is desired name
	"urn":"identifier",
	"dtype":"resource_type",
	"abstract":"description",
	"sdate":"date_created",
	"ddate":"defense_date",
	"keywords":"keyword"
}

del_keys = [ #things to remove
	'adate',
	'cdate',
	'url',
	'notices'
]
lambdas = [ #inline fuction definitions, applied to all keys in row
	lambda row,key : row.update({"year":row[key][0][0:4]} if key == "date_created" else {}), #create year
	lambda row,key : helpers.create_embargo_col(row) if key == 'rdate' else {},#add embargo stuff
	lambda row,key : row.update({"description":[item.strip('"') for item in row[key]]} if key == 'description' else {}), # remove extra quotes
	lambda row,key : row.update({"resource_type": [item.title() for item in row[key]]} if key == 'resource_type' else {}) #title case for res type

]
update = { #new things to add
	"license":[]
}
