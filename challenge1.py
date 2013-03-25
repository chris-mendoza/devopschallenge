#!/usr/bin/env python

#Challenge:  Write a script that builds three 512 MB Cloud Servers that following a similar naming convention. 
#(ie., web1, web2, web3) and returns the IP and login credentials for each server. Use any image you want. 
#Worth 1 point


import pyrax
import pyrax.exceptions as exc
import os
import time

creds_file= os.path.expanduser("~/.rackspace_cloud_credentials")

try: 
	pyrax.set_credential_file(creds_file)
except exc.AuthenticationFailed:
	print "Problem with credential file ~./rackspace_cloud_credentials"
print "Authenticated =", pyrax.identity.authenticated
print

pyrax.connect_to_cloudservers()

cs = pyrax.cloudservers

servreq = ['web1', 'web2', 'web3']
#servreq = range(1, 3+1, 1)

image = [img for img in cs.images.list()
        if "12.10" in img.name][0]

flavor = [flavor for flavor in cs.flavors.list()
        if flavor.ram == 512][0]

for server in range(len(servreq)):
        server_name = servreq[server]
        new_server = cs.servers.create(server_name, image.id, flavor.id)
        new_serverid = new_server.id
	print "Name:", new_server.name, "\nID:", new_server.id,\
"\nStatus:", new_server.status, "\nAdmin Password:", new_server.adminPass 
	while not (new_server.networks):
		time.sleep(10)
		new_server = cs.servers.get(new_serverid)
	print "Public IP", new_server.networks["public"][0], "\nPrivate IP", new_server.networks["private"][0]

