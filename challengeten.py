#!/usr/bin/env python

'''
Challenge 10: Write an application that will:
- Create 2 servers, supplying a ssh key to be installed at /root/.ssh/authorized_keys.
- Create a load balancer
- Add the 2 new servers to the LB
- Set up LB monitor and custom error page.
- Create a DNS record based on a FQDN for the LB VIP.
- Write the error page html to a file in cloud files for backup.
'''

import pyrax
import pyrax.exceptions as exc
import time
import os
import sys
from M2Crypto import RSA 
import base64


#Tell the program where to find our login credentials.
creds_file= os.path.expanduser("~/.rackspace_cloud_credentials")

#Use our own authentication script, because it looks ugly otherwise
try:
        pyrax.set_credential_file(creds_file)
except exc.AuthenticationFailed:
        print "Problem with credential file ~./rackspace_cloud_credentials"
print "Authenticated =", pyrax.identity.authenticated
print

#Grab each library and put it into a variable for easier reference.
cs = pyrax.cloudservers
dns = pyrax.cloud_dns
clb = pyrax.cloud_loadbalancers
cf = pyrax.cloudfiles

#Create a function to generate an RSA key pair if needed


#Take some input from the user, and store it in variables.
serv_pre = raw_input("Server Prefix:\n")
ssh_usr = raw_input("Which user's key are we going to export?(Press enter to use your current users key)")

usr_home = "~"+ssh_usr

srv_host = os.uname()[1]

if ssh_usr == "":
        ssh_usr = os.getlogin()

pub_path = os.path.expanduser("~/.ssh")+"/id_rsa.pub"
priv_path = os.path.expanduser("~/.ssh")+"/id_rsa"

if os.path.isfile(pub_path) is False:
                print "The keys to the user: "+ssh_usr+" does not exist"
                print "Creating a key pair now..."
                rsa_key = RSA.gen_key(2048, 65537)
                pub_key = 'ssh-rsa %s %s@%s' % (base64.b64encode('\0\0\0\7ssh-rsa%s%s ' % (rsa_key.pub()[0], rsa_key.pub()[1])), ssh_usr, srv_host) 


                print pub_key

                f = open(pub_path, "a")
                f.write(pub_key)
                f.close()

                rsa_key.save_key(priv_path, cipher=None)
                os.chmod(priv_path, 600)

		print "Saved SSH Key To local System: \n", pub_path
                              
ssh_key = open(pub_path).read()                 

files = {"/root/.ssh/authorized_keys": ssh_key}

print "Creating Server"

image = [img for img in cs.images.list()
         if "6.3 in img.name"][0]

flavor = [flv for flv in cs.flavors.list()
         if flv.ram == 512][0]

new_server = cs.servers.create(serv_pre, image, flavor, files=files)

new_serverid = new_server.id
server_pass = new_server.adminPass

while not (new_server.networks):
	time.sleep(50)
	print "Waiting for networking"
	new_server = cs.servers.get(new_serverid)

print "-"*30, "\nName:", new_server.name, "\nID:", new_server.id,\
"\nStatus:", new_server.status, "\nAdmin Password:", server_pass
print "IPv4:", new_server.networks, \
"\nIPv6:", new_server.networks["public"][0], \
"\nPrivate IP", new_server.networks["private"][0]

