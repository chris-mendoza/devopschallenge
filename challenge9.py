#!/usr/bin/env python

import pyrax
import pyrax.exceptions as exc
import os
import sys

#Tell the program where to find our login credentials.
creds_file= os.path.expanduser("~/.rackspace_cloud_credentials")

#Use our own authentication script, because it looks ugly otherwise
try:
        pyrax.set_credential_file(creds_file)
except exc.AuthenticationFailed:
        print "Problem with credential file ~./rackspace_cloud_credentials"
print "Authenticated =", pyrax.identity.authenticated
print

#Store Cloud Servers and Cloud DNS in a variable.
cs = pyrax.cloudservers
dns = pyrax.cloud_dns

#Get user input for the domain/server name.
domain_name = raw_input("What is the FQDN we are going to use? \n")

#Create an interactive interface to easily choose your image.

i = 1
while i:
        inputid = raw_input("Type in Image Name:\n")

        image = [img for img in cs.images.list()
         if inputid in img.name]

        print image

        if "use:" in inputid:
                output = inputid.lstrip('use:')
                print "Using image: ", image 
                i = 0


#Create an interactive interface to easily choose your flavor.
i = 1
while i:
        flavorid = raw_input("Insert Flavor ID:\n")

        flavor = [flv for flv in cs.flavors.list()
                   if flavorid in flv.name][0]

        print flavor

        if "use:" in flavorid:
                flv_out = flavorid.lstrip('use:')
                print "Using flavor: ", flavor
                i = 0

#Create the server 
new_server = cs.servers.create(domain_name, image.id, flavor.id)
