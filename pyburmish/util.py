from lingpy import Model
from lingpy.sequence.sound_classes import token2class
from pyburmish import burmish_path, load_burmish
from unicodedata import normalize

sca = Model('sca')
color = Model('color')
color.converter['⁵⁵'] = 'Crimson'
color.converter['³⁵'] = 'LightBlue'
color.converter['⁴'] = 'LightYellow'
color.converter['²'] = 'LightGreen'
color.converter['³'] = 'ForestGreen'
color.converter['³¹'] = 'Brown'
color.converter['¹'] = 'White'
color.converter['²¹'] = 'DarkOrange'
color.converter['³³'] = 'CornflowerBlue'
color.converter['⁵³'] = '#c86496'
color.converter['⁵¹'] = 'cyan'
_conv = {}
_conv['A'] = 'LightBlue'
_conv['E'] = 'Orange'
_conv['I'] = 'LightGreen'
_conv['O'] = 'white'
_conv['U'] = 'Crimson'
_conv['Y'] = 'LightYellow'

for sound in color.converter:
    cls = token2class(sound, 'sca')
    if cls in 'AEIOUY':
        color.converter[sound] = _conv[cls]
        


def contains(syllable, sound):
    _s = normalize('NFD', ''.join(syllable))
    if sound in _s:
        return True
    return False


def is_aspirated(syllable):
    return contains(syllable, 'ʰ')


def is_creaky(syllable):
    return contains(syllable, '\u0330')


def is_aspirated_or_unvoiced(syllable):
    if is_aspirated(syllable):
        return True
    return contains(syllable, '\u0325')
