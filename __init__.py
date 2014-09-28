# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-09-10 19:48
# modified : 2014-09-10 19:48
"""
Basic module for Burmish plugin for LingPy.
"""

__author__="Johann-Mattis List"
__date__="2014-09-10"

import os
from lingpyd import *
from lingpyd.basic.ops import *
from .settings import *
from .basics import *


#burmish_path = os.path.split(
#        os.path.abspath(
#            __file__
#            )
#        )[0]
#
#try:
#    rcParams['sca'] = Model(os.path.join(burmish_path,'models', 'burmish'))
#    rcParams['art'] = Model(os.path.join(burmish_path, 'models', 'art'))
#except:
#    compile_model(os.path.join(burmish_path,'models','burmish'))
#    compile_model(os.path.join(burmish_path,'models','art'))
#    rcParams['sca'] = Model(os.path.join(burmish_path,'models', 'burmish'))
#    rcParams['art'] = Model(os.path.join(burmish_path, 'models', 'art'))
#
## refine specific settings for burmish
#diacritics,vowels,tones = lingpyd.data.model.load_dvt(path='')
#rcParams['asjp'] = Model('asjp')
#rcParams['dolgo'] = Model('dolgo')
#
#rcParams['diacritics'] = diacritics
#rcParams['vowels'] = [v for v in vowels if v != 'y']
#rcParams['tones'] = tones
#rcParams['_color'] = Model('color')
#rcParams['combiners']    = '\u0361\u035c'
#rcParams['breaks']       = '.-'
#rcParams['stress']       = "ˈˌ'"
#rcParams['merge_vowels'] = True 
#rcParams['basic_orthography'] = 'fuzzy'
#rcParams['burmish_path'] = burmish_path
#
#rcParams['morpheme_separator'] = "◦"
#rcParams['nasal_placeholder'] = "∼"
