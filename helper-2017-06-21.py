from pyburmish import load_burmish, burmish_path
from lingpy import *
from collections import defaultdict

db = load_burmish(remote=True, sqlite=True)
wl = Wordlist(burmish_path('dumps', 'proto-burmish.tsv'),
        conf=burmish_path('conf', 'wordlist.rc'))



D = {0: ['doculect', 'concept', 'tokens', 'structure', 'cogids', 'alignment']}
S = defaultdict(str)
for idx, d, tks, alm, cogs, structure, in iter_rows(wl, 'doculect', 'tokens',
        'alignment', 'cogids', 'structure'):
    if d != 'Proto-Burmish':
        db[idx, 'tokens'] = tks
        db[idx, 'alignment'] = alm
        db[idx, 'cogids'] = cogs
        S[idx] = structure
    else:
        D[idx] = [wl[idx, h] for h in D[0]]


db.add_entries('structure', S, lambda x: x)
db.add_data(Wordlist(D))
db.update('burmish')
    


