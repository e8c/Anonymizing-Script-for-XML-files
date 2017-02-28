'''
2/27/17
Author: Emily Chou
Description: Script to parse XML or CSV file and anonymize all names, emails, and urls.
             Solves collisions by replacing with ?FIRST? or ?LAST? + uniqNum of the collision

Arguments: sys.argv[0] => this script (nameanon1.py)
           sys.argv[1] => xml or csv file with firstname, lastname, and email of all students (the infile)
                          Note: csv file should be formatted as firstname,lastname,email on separate rows 
           sys.argv[2] => anonymized version of ^ if xml file (the outfile)
           sys.argv[3] => xml file that is to be anonymized (the infile)
           sys.argv[4] => anonymized version of ^ (the outfile)
Output: mapping.txt => mapping of anonymized names and original names
        If there are collisions, will print collision statement with corresponding anonymized name
'''

import sys
import string
import csv
import re

from xml.etree import ElementTree as ET

#firstname17 lastname17 not in names.xml

'''
Dictionary with first and last name stored as one value
script with replace these combinations first to reduce
numbers of collisions
key = anoymized name
value = original name
'''
firstAndLast_dict = dict()

'''
Dictionary with all first names and all last names
tored as separate values
key = anoymized name
value = original name
'''
firstOrLast_dict = dict()

'''
Dictionary with emails
key = original email
value = anoymizes email
'''
email_dict = dict()

'''
Parse CSV file, handle collisions, and fill dictionaries with
appropriate values
'''
def parseCSV(infile):
  f = open(infile)
  csv_f = csv.reader(f)
  
  #get information (name, email) from each row 
  for row in csv_f:
    #uniq number to associate with the name and email of this student
    emailh = hash(row[len(row) - 1])

    #add anonymized email to dictionary 
    email_dict[row[len(row) - 1]] = "EMAIL" + str(emailh)

    #add anoymized first and last name combo
    firstAndLast_dict["FIRST" + str(emailh) + " LAST" + str(emailh)] = row[0] + " " + row[0]
  
    #if there is a first name (more than 1 value in the row)
    if(len(row) > 1):
      firstTxt = row[0]
      #handle collisions if the name is already in the dictionary
      if firstTxt in firstOrLast_dict.values():
        handleCollisions(firstTxt, emailh, "?FIRST?")
      else:
        #otherwise, add first name to dictionary
        firstOrLast_dict["FIRST" + str(emailh)] = row[0]
    
    if(len(row) > 2):
      lastTxt = row[1]
      if lastTxt in firstOrLast_dict.values():
        handleCollisions(lastTxt, emailh, "?LAST?")
      else:
        #last name
        firstOrLast_dict["LAST" + str(emailh)] = row[1]    

'''
Parse XML file, handle collisions, and fill dictionaries with
appropriate values
'''
def parseXML(filein):
  with open(filein, 'rb') as f:
    tree = ET.parse(f)
    root = tree.getroot()

    for data in root.iter():
      #find email
      email = data.find('email')

      #find name 
      item = data.find('name')

      if email is not None:
        emailh = hash(email)

      #gets each name individually, replaces all
      #instances of that name in class_content
      if item is not None:
        txt = item.text
        if txt is not None:

          #emails
          email_dict[email.text] = "EMAIL" + str(emailh)

          #first and last name
          firstlast = txt[:]
          firstAndLast_dict["FIRST" + str(emailh) + " LAST" + str(emailh)] = firstlast         

          #extract first name (everything until space)
          spaceIdx = txt.find(" ")
          firstTxt = txt[:spaceIdx]

          #check for collisions
          if firstTxt in firstOrLast_dict.values():
            handleCollisions(firstTxt, emailh, "?FIRST?")
          else:
            firstOrLast_dict["FIRST" + str(emailh)] = firstTxt

          #last name 
          lastTxt = txt[spaceIdx + 1:]
   
          #check for collisions
          if lastTxt in firstOrLast_dict.values():
            handleCollisions(lastTxt, emailh, "?LAST?")
          else:
            firstOrLast_dict["LAST" + str(emailh)] = lastTxt  

'''
Go through data file and replace the original names/emails with
anoymized names/emails stored in the dictionary
'''
def findandrep(filein, fileout):
  with open(filein,'rw') as f:
    tree = ET.parse(f)
    root = tree.getroot()
    replacement = "ashdkrkejfn"
    replTxt = "asdfghjkl"
    for data in root.iter():      
      #first replace first and last name combos
      for x in firstAndLast_dict:
        try:
          data.text = data.text.replace(firstAndLast_dict[x], x)
        except:
          continue
      #replace names with just first or last name
      for x in firstOrLast_dict:
        try:
          data.text = data.text.replace(firstOrLast_dict[x], x)
        except:
          continue
      #replace emails
      for x in email_dict:
        try:
          data.text = data.text.replace(x, email_dict[x])
        except:
          continue
    tree.write(fileout)

'''
Write to mapping.txt the mapping between original and 
anonymized names so researcher can refer back and forth if needed
'''
def writeMapping():
  output = open("mapping.txt", 'w')
  #just write first and last so we still write names that would be collisions
  for x in firstAndLast_dict:
    output.write(x + " | " + firstAndLast_dict[x] + " ")
    output.write("\n")
  output.close()

'''
Handle collisions by making the anonymized name ?FIRST? plus the uniq hashed number
of the last duplicate to be parsed (this tells the researcher that the data associated
with this name should be used with caution as it is ambiguous)
'''
def handleCollisions(text, uniqNum, fOrl):
  print "Potential collision for first name " + text + ". Will be replaced with " + fOrl + str(uniqNum)
  for key in firstOrLast_dict:
    #find duplicate 
    if firstOrLast_dict.get(key, None) == text:
      #delete the duplicate value
      del firstOrLast_dict[key]
      break
  firstOrLast_dict[fOrl + str(uniqNum)] = text

#METHODS TO ANONYMIZE URL
'''
Function to replace the unique id of every url
in a file with a uniform string.
param: replaceWith - word to replace the unique
                      part of a url with
'''
def replace(filein, fileout, replaceWith):
  from xml.etree import ElementTree as ET
  with open(filein, 'rw') as f:
    tree = ET.parse(f)
    root = tree.getroot()
    replTxt = None

    #iterate through every data element in the file
    for data in root.iter():
      
      #find content tags and extract the text within
      item = data.find('content')

      if item is not None:
        txt = item.text
        if txt is not None:
  
          #find start indexes of all urls in file and store in array
          list = []             
          list = [a.start() for a in re.finditer('http', txt)]

          listOfUrls = []

          #extract the url
          i = 0
          while(i < len(list)):
            if len(list) != 0:
              urlTxt = txt[list[i] + 8:]

              #start of the unique portion (part to be
              #anonymized) of the url
              replTxt = repHelper(urlTxt)
              if replTxt != "":
                listOfUrls.append(replTxt)
            i += 1
      try:
        for i in listOfUrls:
          data.text = data.text.replace(i, replaceWith)
      except:
        continue
      
      #find subject tags and extract the text within
      item1 = data.find('subject')
      if item1 is not None:
        txt1 = item1.text
        if txt1 is not None:
          urlIdx1 = txt1.find('http')

          if urlIdx1 != -1:
            urlTxt1 = txt1[urlIdx1 + 8:]
            replTxt1 = repHelper(urlTxt1);

      #replace every occurance of the unique url tag extracted
      #with string, replaceWith
      try:
        if replTxt1 is not None:
          data.text = data.text.replace(replTxt1, replaceWith)
      except:
        continue
    tree.write(sys.argv[4])

'''
Helper method to extract the url that is to be anonymized
'''
def repHelper(urlTxt):
  replIdx = urlTxt.find('/')
  replIdx1 = replIdx2 = replIdx3 = 1000

  #all urls will have one of these ending chars
  if urlTxt.find('>') != -1:
    replIdx1 = urlTxt.find('>')
  if urlTxt.find('<') != -1:
    replIdx2 = urlTxt.find('<')
  if urlTxt.find('"') != -1:
    replIdx3 = urlTxt.find('"')

  #end of the unique portion of the url
  replIdxEnd = min(replIdx1, replIdx2, replIdx3)
  replTxt = urlTxt[replIdx + 1:replIdxEnd]
  return replTxt

def main():
  type = 0
  #ask user what type of files contain the names/emails
  fileType = raw_input("What type of file are you using to parse for names/emails? (xml or csv): ")
  if fileType=="xml":
    type = 1
  if(type == 0):
      parseCSV(sys.argv[1])
  else:
      parseXML(sys.argv[1])
      findandrep(sys.argv[1], sys.argv[2])
  
  #anonymize names/emails
  findandrep(sys.argv[3], sys.argv[4])
  writeMapping()
  
  #anonymize urls
  replace(sys.argv[4], sys.argv[4], "somelink")

main()
