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
        img_in = raw_input("Type in Image Name:\n")

        search_image = [img for img in cs.images.list()
         if img_in in img.name]

        print search_image


        if "use:" in img_in: 
             img_out = img_in.strip("use:")
             saved_img = [img for img in cs.images.list()
                             if img_out in img.name][0]
             print "Using image: ", saved_img
             i = 0


#Create an interactive interface to easily choose your flavor.

i = 1
while i:
        flv_in = raw_input("Insert Flavor ID:\n")
        
        search_flavor = [flv for flv in cs.flavors.list()
                   if flv_in in flv.name]

        print search_flavor

        if "use:" in flv_in:
                flv_out = flv_in.strip("use:")
                saved_flv = [flv for flv in cs.flavors.list()
                           if flv_out in flv.name][0]

                print "Using flavor: ", saved_flv 
                i = 0

#Create the server 
new_server = cs.servers.create(domain_name, saved_img, saved_flv)
