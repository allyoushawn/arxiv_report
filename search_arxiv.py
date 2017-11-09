#!/usr/bin/env python3
import requests
import time
import os
import pdb

arxiv_header = 'https://arxiv.org'
paper_info_list = []
title_key_words = ['speech recognition', 'recurrent', 'autoencoder', 'auto-encoder', 'unsupervised']
author_key_words = ['Herman Kamper', 'Aren Jansen', 'Sharon Goldwater', 'Bengio', 'Hinton']

dir_path = os.path.dirname(os.path.realpath(__file__))

target_arxiv_category = ['cs.CL', 'stat.ML', 'cs.AI', 'eess.AS']
for arxiv_category in target_arxiv_category:
    arxiv_url = arxiv_header + '/list/' + arxiv_category + '/recent'
    res = requests.get(arxiv_url)
    lines = res.text.split('\n')
    for line in lines:
        if '<a href=' in line and '>all<' in line:
            break

    tokens = line.split('<a href=')
    all_recent_paper_url = arxiv_header + tokens[-1].split('>all<')[0][1:-1]

    time.sleep(2)
    res = requests.get(all_recent_paper_url)
    lines = res.text.split('\n')

    search_author = False
    authors_list = []
    for line in lines:
        if 'Title:' in line:
            tokens = line.split('</span>')
            title = tokens[-1]
            title = title[1:]

        if 'Authors:' in line:
            search_author = True
            continue

        if search_author == True and '</div>' in line:
            search_author = False
            paper_info_list.append((title, authors_list))
            authors_list = []

        if search_author == True:
            line = line.split('</a>')
            name = line[-2]
            name = name.split('>')
            name = name[-1]
            authors_list.append(name)
    time.sleep(2)

op_file_name = time.strftime("%d/%m/%Y")
op_file_name = dir_path + '/' + op_file_name.replace('/','-')
op_f = open(op_file_name, 'w')
for paper in paper_info_list:
    retrieve = False

    #Filter with key_words in title
    for key_word in title_key_words:
        if key_word.upper() in paper[0].upper():
            retrieve = True
            break

    #Filter with key_words in authors
    for key_word in author_key_words:
        for author in paper[1]:
            if key_word.upper() in author.upper():
                retrieve = True
                break

    if retrieve == False:
        continue

    author_str = ''
    for name in paper[1]:
        author_str += name + '; '
    author_str = author_str[:-2]
    op_f.write('\'{}\' {}\n'.format(paper[0], author_str))
op_f.close()
