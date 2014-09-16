# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-09-11 12:57
# modified : 2014-09-11 12:57
"""
Basic script for handling unicode data.
"""

__author__="Johann-Mattis List"
__date__="2014-09-11"

import os
import json
import lingpyd
from .settings import *


udat = lingpyd.csv2list(
        os.path.join(
            burmish_path,
            'data',
            'UnicodeData.brackets.txt'
            ),
        sep = ";"
        )


unames = dict()
rcParams['brackets'] = '([{『（₍⁽«'
for line in udat:
    
    if len(line[0]) == 4:
        char = eval("'"+r"\u"+line[0]+"'")

        unames[char] = line[1]
        unames[line[1]] = char
        


def get_pendant(char):

    name = unames[char]
    try:
        if "RIGHT" in name:
            return unames[name.replace("RIGHT","LEFT")]
        if "LEFT" in name:
            return unames[name.replace("LEFT","RIGHT")]
    except:
        return ''


# set up some basic normalization paramters
rcParams['normalizations'] = json.load(
        open(
            os.path.join(
                burmish_path,
                'data',
                'normalizations.json'
                )
            )
        )
