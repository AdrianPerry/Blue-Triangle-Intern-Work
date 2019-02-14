#!/usr/bin/env python
# -*- coding: utf-8 -*-

# htmlToPlainText.py
import unicodecsv as csv
import re
# import codecs


from bs4 import BeautifulSoup


with open('issues.csv', 'r') as csv_file_in:
    csv_reader = csv.reader(csv_file_in)
    rows = []
    for row in csv_reader:
        rows.append(row)

    csv_file_in.close()


headerList = rows[0]
headerList[0] = "Issue Id"
descriptionIndex = 0
tagIndex=2
for headerName in headerList:
    if headerName == 'Description':
        # Got the index for the description column, break out of loop
        break
    descriptionIndex = descriptionIndex + 1


descriptions = []
tags = []
for i in range(1, len(rows)):
    oldHtmlDescription = rows[i][descriptionIndex]
    try:
        newPlainTextDescription = oldHtmlDescription.split('{html class=mailbox}')[1].split('{html}')[0]
        soup = BeautifulSoup(newPlainTextDescription, features="html.parser")
        newPlainTextDescription = soup.get_text()
    except Exception as e:
        # print(e)
        newPlainTextDescription = oldHtmlDescription
    newPlainTextDescription = re.sub("(<!--.*?-->)", "", newPlainTextDescription, flags=re.DOTALL)
    descriptions.append(newPlainTextDescription)

    oldTag = rows[i][tagIndex]
    newTag = oldTag.replace(' ','_')
    tags.append(newTag)

print headerList[2]

newRows = []
for i in range(1, len(rows)):
    newRows.append(rows[i])
    newRows[i-1][descriptionIndex] = descriptions[i-1]
    newRows[i-1][tagIndex] = tags[i-1]

with open('issues-modified.csv', 'w') as csv_file_out:
    writer = csv.writer(csv_file_out, delimiter=",", encoding='utf-8')
    writer.writerow(headerList)
    for row in newRows:
        writer.writerow(row)

    csv_file_out.close()