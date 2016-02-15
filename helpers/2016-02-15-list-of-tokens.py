from lingpyd import *

wl = Wordlist('../tsv/burmish.tsv')
langs = [line for line in csv2list('../tsv/doculects.tsv') if not
        line[0].startswith('*')]

for line in langs[1:]:
    lang = line[0]
    wl.output('tsv', filename='burmish-'+lang, subset=True,
            rows=dict(language="=='"+lang+"'"),
            ignore="all", prettify=False)
