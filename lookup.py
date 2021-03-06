#!/usr/bin/env python3


import time
import fileinput
import pycurl

class Address:
  def __init__(self):
    self.contents = ""

  # callback function used by curl when it gets more data
  def callback(self, buff):
    self.contents += buff.decode("utf-8")

  # rip the email address out of the downloaded page
  def get(self):
    lines = self.contents.splitlines( )
    for line in lines:
      # search for the mailto link
      idx = line.find("mailto:")
      if idx != -1:
        # rip out the email address
        end = line[idx:].find("\"")
        return line[idx:][7:end]
    # no link found...
    return "UNKNOWN" 

def lookup(first, last):
  a = Address( )
  c = pycurl.Curl( )
  # build an URL that searches the directory for the student in question
  url = "students.umw.edu/directory/?adeq=%s+%s" % (first, last)
  c.setopt(c.URL, url)
  c.setopt(c.WRITEFUNCTION, a.callback)
  # download the page
  c.perform( )
  c.close( )
  # strip out the address
  return a.get( )

# print a friendly greeting
print("Enter a student name:")
while True:
  try:
    first, last = tuple(input('> ').split( ))
  except:
    print('\n')
    break
  email = lookup(first, last)
  print("%s %s %s" % (first, last, email))
  # wait for some time (I don't know if IT wants me hammering their server like this
  time.sleep(1)


