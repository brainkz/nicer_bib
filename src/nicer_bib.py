#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 12:00:54 2022

@author: brainkz
"""

bib_str = '''
@article{10.1145/3177877,
author = {Sadat, Sayed Abdullah and Canbolat, Mustafa and K\"{o}se, Sel\c{c}uk},
title = {Optimal Allocation of LDOs and Decoupling Capacitors within a Distributed On-Chip Power Grid},
year = {2018},
issue_date = {July 2018},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
volume = {23},
number = {4},
issn = {1084-4309},
url = {https://doi.org/10.1145/3177877},
doi = {10.1145/3177877},
abstract = {Parallel on-chip voltage regulation, where multiple regulators are connected to the same power grid, has recently attracted significant attention with the proliferation of small on-chip voltage regulators. In this article, the number, size, and location of parallel low-dropout (LDO) regulators and intentional decoupling capacitors are optimized using mixed integer non-linear programming formulation. The proposed optimization function concurrently considers multiple objectives such as area, power noise, and overall power consumption. Certain objectives are optimized by putting constraints on the other objectives with the proposed technique. Additional constraints have been added to avoid the overlap of LDOs and decoupling capacitors in the optimization process. The results of an optimized LDO allocation in the POWER8 chip is compared with the recent LDO allocation in the same IBM chip in a case study where a 20% reduction in the noise is achieved. The results of the proposed multi-criteria objective function under a different area, power, and noise constraints are also evaluated with a sample ISPD’11 benchmark circuits in another case study.},
journal = {ACM Trans. Des. Autom. Electron. Syst.},
month = {may},
articleno = {49},
numpages = {15},
keywords = {Power delivery network (PDN), decoupling capacitors, current sharing, physical design, distributed on-chip voltage regulator}
}
'''
bib_str = '''
@inproceedings{10.1145/2897937.2898008,
author = {Zhan, Xin and Li, Peng-Hsiang Chung and S\'{a}nchez-Sinencio, Edgar},
title = {Distributed On-Chip Regulation: Theoretical Stability Foundation, over-Design Reduction and Performance Optimization},
year = {2016},
isbn = {9781450342360},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/2897937.2898008},
doi = {10.1145/2897937.2898008},
abstract = {While distributed on-chip voltage regulation offers an appealing solution to power delivery, designing power delivery networks (PDNs) with distributed on-chip voltage regulators with guaranteed stability is challenging because of the complex interactions between active regulators and the bulky passive network. The recently developed hybrid stability theory provides an efficient stability checking and design approach, giving rise to highly desirable localized design of PDNs. However, the inherent conservativeness of the hybrid stability criteria can lead to pessimism in stability evaluation and hence large over-design. We address this challenge by proposing an optimal frequency-dependent system partitioning technique to significantly reduce the amount of pessimism in stability analysis. With theoretical rigor, we show how to partition a PDN system by employing optimal frequency-dependent impedance splitting between the passive network and voltage regulators while maintaining the desired theoretical properties of the partitioned system blocks upon which the hybrid stability principle is anchored. We demonstrate a new stability-ensuring PDN design approach with the proposed over-design reduction technique using an automated optimization flow which significantly boosts regulation performance and power efficiency.},
booktitle = {Proceedings of the 53rd Annual Design Automation Conference},
articleno = {54},
numpages = {6},
location = {Austin, Texas},
series = {DAC '16}
}
'''



import re
import os
from pybtex.database import parse_string, Person
from clipboard import copy, paste
#
# pybtex.database.parse_string(value, bib_format, **kwargs)¶


SEP = re.compile(r'([\s\-]+)')
ORDINAL = re.compile(r'\d*((1st)|(2nd)|(3rd)|([4567890]{1}th))\s*', re.IGNORECASE)
WORDS = re.compile(r'(annual)\s*', re.IGNORECASE)


NON_CAP = {'a', 'an', 'the', 'for', 'and', 'nor', 'but', 'or', 'yet', 'so', 'aboard', 'about', 'above', 'across', 'after', 'against', 'along', 'amid', 'among', 'around', 'as', 'at', 'before', 'behind', 'below', 'beneath', 'beside', 'between', 'beyond', 'but', 'by', 'concerning', 'considering', 'despite', 'down', 'during', 'except', 'following', 'for', 'from', 'in', 'inside', 'into', 'like', 'minus', 'near', 'next', 'of', 'off', 'on', 'onto', 'opposite', 'out', 'outside', 'over', 'past', 'per', 'plus', 'regarding', 'round', 'save', 'since', 'than', 'through', 'till', 'to', 'toward', 'under', 'underneath', 'unlike', 'until', 'up', 'upon', 'versus', 'via', 'with', 'within', 'without'}

FIELDS = {
'inproceedings' : {'author', 'title', 'booktitle', 'volume', 'number', 'pages', 'month', 'year', 'doi'},
      'article' : {'author', 'title',   'journal', 'volume', 'number', 'pages', 'month', 'year', 'doi'},
         'book' : {'author', 'title',      'year', 'publisher'}
}

JOURNAL_ABBR = {
'ACM Trans. Des. Autom. Electron. Syst.' : 'ACM Transactions on Design Automation of Electronic Systems',
}

MONTH_ABBR = {
'jan' : 'January',
}

KEYS = {'inproceedings': 'booktitle', 'article': 'journal'}

def by2(it, fillval = ''):
    it = iter(it)
    for a in it:
        yield a, next(it, fillval)

def cap_title(title, sep = SEP):
    out = []
    for word, sep in by2(sep.split(title)):
        # print(word, sep, word.islower())
        if word not in NON_CAP and word.islower():
            word = word.capitalize()
        # print(word + sep)
        out.append(word + sep)
    return ''.join(out)

def initials(name, sep = SEP):
    out = []
    for name, sep in by2(sep.split(name)):
        out.append(name[0] + '.' + sep)
    return ''.join(out)

def author_initials(person_entries):
    for person in person_entries:
        person.first_names = [initials(name) for name in person.first_names]
        person.middle_names = [initials(name) for name in person.middle_names]

def filter_booktitle_journal(entry, keys = KEYS, abbr = JOURNAL_ABBR):
    key = keys[entry.type]
    if entry.fields[key] in abbr:
        entry.fields[key] = abbr[entry.fields[key]]
    else:
        entry.fields[key] = ORDINAL.sub('', entry.fields[key])
        entry.fields[key] = WORDS.sub('', entry.fields[key])
    entry.fields[key] = cap_title(entry.fields[key])
if __name__ == '__main__':
    os.system('afplay /System/Library/Sounds/Morse.aiff')
    try:
        db = parse_string(paste(), 'bibtex').lower()
        # db = parse_string(bib_str, 'bibtex').lower()
        for entry_key, entry in db.entries.items():
            entry.fields = {k:v for k,v in entry.fields.items() if k in FIELDS[entry.type]}
            entry.fields['title'] = cap_title(entry.fields['title'])
            author_initials(entry.persons['author'])
            if entry.type in ('inproceedings', 'article'):
                filter_booktitle_journal(entry)
        print(db.to_string('bibtex'))
        copy(db.to_string('bibtex'))
        os.system('afplay /System/Library/Sounds/Glass.aiff')
    except:
        os.system('afplay /System/Library/Sounds/Sosumi.aiff')
