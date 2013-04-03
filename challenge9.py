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

a = 1
while a:
        inputid = raw_input("Type in Image Name:\n")
        new_input = inputid.strip("use: ")

        search_image = [img for img in cs.images.list()
         if inputid in img.name]

        print search_image

        if "use:" in inputid: 
                saved_img = [img for img in cs.images.list()
                             if new_input in img.name]
                print "Using image: ", saved_img
                a = 0


#Create an interactive interface to easily choose your flavor.

i = 1
while i:
        flavorid = raw_input("Insert Flavor ID:\n")
        new_flv = flavorid.strip("use:")

        flavor = [flv for flv in cs.flavors.list()
                   if flavorid in flv.name]

        print flavor

        if "use:" in flavorid:
                save_flv = [flv for flv in cs.flavors.list()
                           if new_flv in flv.name]

                print "Using flavor: ", new_flv
                i = 0

#Create the server 
new_server = cs.servers.create(domain_name, saved_img, save_flv)
