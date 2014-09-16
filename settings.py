# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-09-11 12:54
# modified : 2014-09-11 12:54
"""
Basic settings for burmish plugin.
"""

__author__="Johann-Mattis List"
__date__="2014-09-11"

import lingpyd
from lingpyd.settings import rcParams
from lingpyd.data.model import *
from lingpyd.data.derive import *

burmish_path = os.path.split(
        os.path.abspath(
            __file__
            )
        )[0]

try:
    rcParams['sca'] = Model(os.path.join(burmish_path,'models', 'burmish'))
    rcParams['art'] = Model(os.path.join(burmish_path, 'models', 'art'))
except:
    compile_model(os.path.join(burmish_path,'models','burmish'))
    compile_model(os.path.join(burmish_path,'models','art'))
    rcParams['sca'] = Model(os.path.join(burmish_path,'models', 'burmish'))
    rcParams['art'] = Model(os.path.join(burmish_path, 'models', 'art'))

# refine specific settings for burmish
diacritics,vowels,tones = lingpyd.data.model.load_dvt(path='')
rcParams['asjp'] = Model('asjp')
rcParams['dolgo'] = Model('dolgo')

rcParams['diacritics'] = diacritics
rcParams['vowels'] = [v for v in vowels if v != 'y']
rcParams['tones'] = tones
rcParams['_color'] = Model('color')
rcParams['combiners']    = '\u0361\u035c'
rcParams['morpheme_separator'] = "◦"
rcParams['nasal_placeholder'] = "∼"

