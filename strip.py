#usr/bin/python
#this file strips BOM from the begining of files with BOM windows -> *nix issues
# if you get "json.decoder.JSONDecodeError: Unexpected UTF-8 BOM (decode using utf-8-sig): line 1 column 1 (char 0)"
# on some file run `strip.py path/to/file` then try again.
import os, sys, codecs
def strip(path):
    BUFSIZE = 4096
    BOMLEN = len(codecs.BOM_UTF8)

    with open(path, "r+b") as fp:
        chunk = fp.read(BUFSIZE)
        if chunk.startswith(codecs.BOM_UTF8):
            i = 0
            chunk = chunk[BOMLEN:]
            while chunk:
                fp.seek(i)
                fp.write(chunk)
                i += len(chunk)
                fp.seek(BOMLEN, os.SEEK_CUR)
                chunk = fp.read(BUFSIZE)
            fp.seek(-BOMLEN, os.SEEK_CUR)
            fp.truncate()

if __name__ == '__main__':
    strip(sys.argv[1])