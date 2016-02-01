#!/usr/bin/env python3

import time
import os
import email
import imaplib
import getpass

file_dates = {}

IMAP_SERVER = 'imap.umw.edu'

# connect to the email server
def connect( ):
  mail = imaplib.IMAP4_SSL(IMAP_SERVER)
  try:
    mail.login('finlayson', getpass.getpass( ))
  except:
    print('Could not log in!')
    sys.exit(0)
  return mail

# show available folders, and choose one of them
def choose_folder(mail):
  folders = mail.list( )[1]
  i = 0
  for f in folders:
    name = str(f, encoding='utf8')
    print(i, '- ' + name[name.find('/') + 3:])
    i = i + 1
  number = int(input('Which folder to download from: '))
  name = str(folders[number], encoding='utf8')
  folder = name[name.find('/') + 3:]
  mail.select(folder)

# get all mail messages from the given folder
def get_mail(mail):
  result, data = mail.search(None, 'ALL')
  ids = data[0].split( )
  mesgs = []
  for mail_id in ids:
    result, data = mail.fetch(mail_id, '(RFC822)')
    if data != None and data[0] != None:
      mesgs.append(data[0][1])
  return mesgs

# create a directory if it doesn't exist
def ensure_dir(name):
  if not os.path.exists(name):
    try:
      os.makedirs(name)
      return True
    except:
      print('Could not make directory \'%s, skipping!\'' % (name))
      return False
  return True

# return the number of a month
def month_number(m):
  if m == 'Jan': return 0
  if m == 'Feb': return 1
  if m == 'Mar': return 2
  if m == 'Apr': return 3
  if m == 'May': return 4
  if m == 'Jun': return 5
  if m == 'July': return 6
  if m == 'Aug': return 7
  if m == 'Sep': return 8
  if m == 'Oct': return 9
  if m == 'Nov': return 10
  if m == 'Dec': return 11
  else:
    print('Noo!, there is no month called \'%s\'!!!' % (m))
    assert(False)

# return whether a is OLDER than b
def date_older(a, b, fname):
  a = a.split( )
  b = b.split( )
  # compare year first (unlikely to happen!)
  if int(a[3]) < int(b[3]):
    return True
  elif int(a[3]) > int(b[3]):
    return False
  # compare the month next
  if month_number(a[2]) < month_number(b[2]):
    return True
  elif month_number(a[2]) > month_number(b[2]):
    return False
  # compare the day next
  if int(a[1]) < int(b[1]):
    return True
  elif int(a[1]) > int(b[1]):
    return False
  # compare times last
  atime = a[4].split(':')
  btime = b[4].split(':')
  # compare hours
  if int(atime[0]) < int(btime[0]):
    return True
  elif int(atime[0]) > int(btime[0]):
    return False
  # compare minutes
  if int(atime[1]) < int(btime[1]):
    return True
  elif int(atime[1]) > int(btime[1]):
    return False
  # compare seconds
  if int(atime[2]) < int(btime[2]):
    return True
  elif int(atime[2]) > int(btime[2]):
    return False
  # in cases where someone attaches the same file twice (ugh) it has
  # the same time stamp, and we don't care which one we take!
  return True

# return whether the file with the given name is older than the date given
def file_older(fname, date):
  # if the file does not exist, it should be replaced
  if not os.path.exists(fname):
    # add it in!
    file_dates[fname] = date
    return True
  # get the last date from the mapping
  last_date = file_dates[fname]
  # if the existing one is older
  if date_older(last_date, date, fname):
    # update the time
    print('Found a newer version of', fname)
    print('\t\t(%s older than %s)\n\n' % (last_date, date))
    file_dates[fname] = date
    return True
  else:
    # file is not older, don't over-write
    print('This version of %s is older, skipping!' % (fname))
    return False


# create a file from the sender and dump the contents into it
def create_file(sender, fname, text, date):
  if fname == None:
    fname = 'mesg.txt'
  # only over-write a file if it's older than the given one!
  if file_older(sender + '/' + fname, date):
    f = open(sender + '/' + fname, 'wb')
    f.write(text)
    f.close( )

# process one email message
def process(raw_mesg):
  mesg = email.message_from_string(str(raw_mesg, encoding='utf8'))
  sender = mesg['From']
  date = mesg['Date']
  sender = sender[sender.find('<') + 1 : sender.find('@')]
  if not ensure_dir(sender):
    return
  else:
    for part in mesg.walk( ):
      if part.get_content_maintype() == 'multipart':
        continue
      create_file(sender, part.get_filename( ), part.get_payload(decode=True), date)

# chain it all together
mail = connect( )
choose_folder(mail)
mesgs = get_mail(mail)
for mesg in mesgs:
  process(mesg)



