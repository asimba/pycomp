#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import exit,argv
from os import access,R_OK,remove
from os.path import isfile
from tempfile import NamedTemporaryFile
import py_compile
import zlib,base64

def err(msg): print msg;exit()

if __name__=='__main__':
    if len(argv)!=3:
        err('PyComp is a simple script to compress python files.\n'+\
        'Usage: pycomp.py <source.py> <destination.py>')

    if isfile(argv[1]) and access(argv[0],R_OK):
        if isfile(argv[2]): err('The file "%s" is already exists!' % argv[2])
        try:
            tf=NamedTemporaryFile(delete=True)
            tn=tf.name
            tf.close()
        except: err('Unable to create temporary file!')
        try:
            py_compile.compile(argv[1],tn,doraise=True)
            try: remove(tn)
            except: pass
        except: err('File check failed: "%s" !' % argv[1])
        try: o=open(argv[2],'wb')
        except: err('Unable to open file "%s"!' % argv[2])
        i=open(argv[1],'rb')
        o.write('#!/usr/bin/env python\n# -*- coding: utf-8 -*-\nimport'+\
        ' base64,zlib;exec compile(zlib.decompress(base64.decodestring(\"\\\n')
        o.write(base64.encodestring(zlib.compress(i.read(),9)).replace('\n',\
            '\\\n'))
        o.write('\")),"","exec")\n')
        i.close()
        o.close()
    else: err('The file "%s" is inaccessible!' % argv[1])
