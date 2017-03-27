import sys
import operator
import string
import csv
import re

from xml.etree import ElementTree as ET

def getStats(firstname, lastname, usersfile, contentfile):
  userid = None

  #get the user's id from the usersfile so we can match posts to the user
  with open(usersfile, 'rb') as f:
    tree = ET.parse(f)
    root = tree.getroot()

    flag = False
    for data in root.iter():
      #find name
      item = data.find('name')

      if item is not None:
        txt = item.text
        if txt.find(firstname) != -1:
          if txt.find(lastname) != -1:
            flag = True

      if flag:
        useridIdx = data.find("user_id")
        if useridIdx is not None:
          userid = useridIdx.text
          break

  f.close()
  print "\nACTIVITY LOG FOR " + firstname + " " + lastname + " (" + userid + ")\n"

  createCount = 0
  followCount = 0
  updateCount = 0
  findDate = False
  with open(contentfile, 'rb') as f:
    tree = ET.parse(f)
    root = tree.getroot()
    for data in root.iter():
      #search through change logs (next 5 datas look for userid and date and post id
      #first find change log
      # in change log find uid
      # if found uid then find 'type' and 'when' and 'to' and increment count of followups and count of created
      item = data.find('change-log')
      if item is not None:
        txt = item.text
        for item in data.findall('change-log'):
        #NEED FOR LOOP TO GO THROUGH ALL CHANGE LOG IN CHANGE LOG
          uidItem = item.find('uid')
          if uidItem is not None:
            #print txt[uidItem:uidItem+15]
            if uidItem.text == userid:
              typeItem = item.find('type')
              if typeItem is not None:
                postType = typeItem.text
                print "TYPE: " + postType
                if postType == "followup":
                  followCount += 1
                elif postType == "create":
                  createCount += 1
                elif postType == "update":
                  updateCount += 1

              whenItem = item.find('when')
              if whenItem is not None:
                postWhen = whenItem.text
                print "DATE: " + postWhen

              #log will have either data or to element for post id
              dataItem = item.find('data')
              if dataItem is not None:
                postData = dataItem.text
                print "POST ID: " + postData + "\n"

              toItem = item.find('to')
                         if toItem is not None:
                postTo = toItem.text
                print "POST ID: " + postTo + "\n"

  print "# of posts created: ", createCount
  print "# of posts followup: ", followCount
  print "# of posts updated: ", updateCount

def main():
  #takes in First and last name (argv[1], argc[2]), users file, and content file
  firstname = sys.argv[1]
  lastname = sys.argv[2]
  usersfile = sys.argv[3]
  contentfile = sys.argv[4]
  getStats(firstname, lastname, usersfile, contentfile)

main()

