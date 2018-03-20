# Copyright (c) 2018 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================


"""home of easyopen - to easily open an idf file"""

# ideally this should be in idf_helper
# pytest kept failing since the other routines set the IDD file
# pytest works here in a seperate file, like eppy/runner.py

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
from six import StringIO
import eppy
import eppy.modeleditor
import eppy.EPlusInterfaceFunctions.parse_idd
import eppy.runner.run_functions


def easyopen(fname):
    """automatically set idd and open idf file. uses version from idf to set correct idd"""
    if isinstance(fname, (file, StringIO)):
        fhandle = fname
    else:
        fhandle = open(fname, 'r')

    # - get the version number from the idf file
    txt = fhandle.read()
    try:
        txt = txt.decode('latin-1') # latin-1 seems to read most things
    except AttributeError:  
        pass
    ntxt = eppy.EPlusInterfaceFunctions.parse_idd.nocomment(txt, '!')
    blocks = ntxt.split(';')
    blocks = [block.strip()for block in blocks]
    bblocks = [block.split(',') for block in blocks]
    bblocks1 = [[item.strip() for item in block] for block in bblocks]
    ver_blocks = [block for block in bblocks1 
                    if block[0].upper() == 'VERSION']
    ver_block = ver_blocks[0]
    versionid = ver_block[1]
    
    # - get the E+ folde based on version number
    vlist = versionid.split('.')
    if len(vlist) == 1:
        vlist = vlist + ['0', '0']
    elif len(vlist) == 2:
        vlist = vlist + ['0']
    ver_str =  '-'.join(vlist)
    eplus_exe, _  = eppy.runner.run_functions.install_paths(ver_str)
    eplusfolder = os.path.dirname(eplus_exe)
    iddfile = '{}/Energy+.idd'.format(eplusfolder, )
    
    # - set IDD and open IDF.
    eppy.modeleditor.IDF.setiddname(iddfile)
    if isinstance(fname, (file, StringIO)):
        fhandle.seek(0)
        idf = eppy.modeleditor.IDF(fhandle)
    else:
        idf = eppy.modeleditor.IDF(fname)
    return idf

