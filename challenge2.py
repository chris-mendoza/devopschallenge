#!/usr/bin/env python

#Challenge 2:Write a script that clones a server 
#(takes an image and deploys the image as a new server). Worth 2 Point

import pyrax
import time
import pyrax.exceptions as exc
import os

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")

try:
        pyrax.set_credential_file(creds_file)
except exc.AuthenticationFailed:
        print "Problem with credential file ~./rackspace_cloud_credentials"
print "Authenticated =", pyrax.identity.authenticated
print

pyrax.connect_to_cloudservers()

cs = pyrax.cloudservers
server = cs.servers.get("4d7abee9-5124-44dc-9c33-346db9a22a7e")
server.create_image("python")
print "Image process starting..."

server_name = server.name + "-clone"

image = [img for img in cs.images.list()
        if "python" in img.name][0]

pyrax.utils.wait_until(image, "status", ['ACTIVE', 'ERROR'], interval=30, attempts=40, verbose=True)

flavor = server.flavor['id']

new_server = cs.servers.create(server_name, image.id, flavor)
new_serverid = new_server.id
print "Name:", new_server.name, "\nID:", new_server.id, \
"\nStatus:", new_server.status, "\nAdmin Password:", new_server.adminPass

while not(new_server.networks):
        time.sleep(10)
        new_server = cs.servers.get(new_serverid)

print "\nPublic IP:", new_server.networks["public"][0], \
"\nPrivate IP:", new_server.networks["private"][0]

print "Waiting for server to build..."

pyrax.utils.wait_until(new_server, "status", ['ACTIVE','ERROR'], interval=30, attempts=40, verbose=True)

print "Server Build Complete"
