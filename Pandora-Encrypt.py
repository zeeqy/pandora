
# coding: utf-8

# In[1]:

from Crypto.Cipher import AES
import hashlib
import getpass
import random
import base64
from Crypto.PublicKey import RSA



# In[2]:

f = open('pandora_public_key.pem','r')
public = f.read()
f.close()
f = open('pandora.data','r')
pw_list = [x.split('\t') for x in f.read().splitlines()]
f.close()
account = raw_input('account info: ').encode('utf-8')
username = raw_input('username: ').encode('utf-8')
password = getpass.getpass('password: ').encode('utf-8')
aes_key = getpass.getpass('AES Key: ').encode('utf-8')
init_string = [account.encode('utf-8'),'|'.join([username,password]).encode('utf-8')]

# In[7]:

def encode(public,aes_key,init_string):
    public_key = RSA.importKey(public)
    md = hashlib.md5()
    md.update(aes_key)
    aes_string = md.digest()
    account_rsa = public_key.encrypt(init_string[0],random.randint(0,1990))[0]
    login_rsa = public_key.encrypt(init_string[1],random.randint(0,1990))[0]
    obj = AES.new(aes_string)
    return [obj.encrypt(account_rsa),obj.encrypt(login_rsa)]


# In[8]:

encoded = [base64.b64encode(encode(public,aes_key,init_string)[0]),base64.b64encode(encode(public,aes_key,init_string)[1])]
if encoded[0] in [x[0] for x in pw_list]:
	updated_list = [encoded if x[0] == encoded[0] else x for x in pw_list]
else:
	pw_list.append(encoded)
	updated_list = pw_list
f = open('pandora.data','w')

for i in updated_list:
	f.write("""%s"""%i[0])
	f.write("\t")
	f.write("""%s"""%i[1])
	f.write("\n")
f.close()
print 'Encrypt into Pandora!'

