'''
Cisco Clean Access (CCA) login script if you do not want to lose your tabs when you open a browser

Developed only for Ubuntu (which does not require NAC Agent) and tested only at UCI

Usage: python cca-agent.py <UCInetID>

This script is for educational purposes only, use it on your own risk.
PS: for more info about CCA: http://en.wikipedia.org/wiki/Cisco_NAC_Appliance
'''

import urllib, urllib2
import collections
import socket
import sys, getpass

# in order to convert headers to dictionary
def convert(data):
    if isinstance(data, unicode):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

# website where request will be sent
target = 'https://resnet-cca3-arc.reshsg.uci.edu/auth/perfigo_cm_validate.jsp'

# get arguments from command line
arg_size = len(sys.argv)
if (arg_size == 2):
    UCInetID = sys.argv[1]
else:
    print 'Usage: python cca-agent.py <UCInetID>'
    sys.exit()

# get password
password = getpass.getpass('Enter password (hidden):')

# get computer's ip address
ip_address = socket.gethostbyname(socket.gethostname())

# headers data
headers = { u'Accept':u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            u'Accept-Charset':u'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            u'Accept-Encoding':u'gzip,deflate,sdch',
            u'Accept-Language':u'en-US,en;q=0.8',
            u'Cache-Control':u'max-age=0',
            u'Connection':u'keep-alive',
            u'Content-Length':u'326',
            u'Content-Type':u'application/x-www-form-urlencoded',
            u'Cookie':u'set-cookie',
            u'Host':u'resnet-cca3-arc.reshsg.uci.edu',
            u'Origin':u'https://resnet-cca3-arc.reshsg.uci.edu',
            u'Referer':u'https://resnet-cca3-arc.reshsg.uci.edu/auth/perfigo_weblogin.jsp?cm=1111111&uri=http%3A%2F%2Fwww.google.com%2F',
            u'User-Agent':u'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4'
          }

# form data
values = dict( eqFrom='perfigo_login.jsp',
               uri='http://www.google.com/',
               cm='1111111', # dunno what this is?
               userip=ip_address,
               session='',
               pm='Linux i686', #MacIntel
               index='0',
               pageid='-1',
               compact='false',
               registerGuest='NO',
               userNameLabel='UCInetID',
               passwordLabel='password',  
               guestUserNameLabel='Guest ID',
               guestPasswordLabel='Password',
               username=UCInetID,
               password=password,
               provider='UCInetID Login'
              )

headers = convert(headers)
data = urllib.urlencode(values)
req = urllib2.Request(target,data, headers)
rsp = urllib2.urlopen(req)
html_rsp = rsp.read()

if ('Invalid' in html_rsp):
    print 'no connection, invalid username or password'
else:
    print 'You probably connected to UCI ResNet'