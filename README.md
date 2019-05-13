# Deliniation
This is a simple python tool to convert Deliniator Seperated Files like comma seperated files, semicolon seperated files, and so on into multidemensional json files of depth 3. It can also take Json files which were exported improperly with Deliniated strings that represent lists and convert them.
simple but frequently done things

## how to use
- place any files delinated by characters into the imports folder ensuring dsvs have the extension `.dsv`
- place any json files you wish to convert in imports as well
- edit [dsv_config] and/or [json_config] to reflect the changes you want
- run `python listafy_str.py` to convert the file(s), and then check exports for the newly created file(s)



## gotchas
- at times the OpenRefine software the library uses changes the names of the columns, ensure they match the keys in your config files.
- if you are getting a KeyError for a column you know exists, it could be because there is a unicode BOM at the beginning of the file, run `python strip.py path/to/file` to remove that before trying again.


[dsv_config]: /dsv_config.py
[json_config]: /json_config.py
