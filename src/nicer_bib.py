#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 12:00:54 2022

@author: brainkz
"""
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

def run():
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
