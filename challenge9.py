#!/usr/bin/env python

import pyrax
import pyrax.exceptions as exc
import os
import sys
import time

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
new_serverid = new_server.id
server_pass = new_server.adminPass

#Wait for networking to populate before moving on.
while not (new_server.networks):
        #wait 30 seconds before moving on
        time.sleep(50)
        print "Waiting for networking"
        #refreshes the new_server value to be tested again on next iteration
        new_server = cs.servers.get(new_serverid)
        #Print out networking information
       
      
print "-"*30, "\nName:", new_server.name, "\nID:", new_server.id,\
"\nStatus:", new_server.status, "\nAdmin Password:", server_pass
print "IPv4:", new_server.networks, \
"\nIPv6:", new_server.networks["public"][0], \
"\nPrivate IP", new_server.networks["private"][0]

ip_address = new_server.networks["public"][1]

#Raise an exception if the domain nam does not exist.
try:
        dom = dns.find(name=domain_name)
except exc.NotFound:
        answer = raw_input("The domain '%s' was not found. Do you want to create it? [y/n]" % domain_name)
        if not answer.lower().startswith("y"):
                sys.exit()
        try:
                dom = dns.create(name=domain_name, emailAddress="sample@example.com", ttl=900, comment="sampledomain")
        except exc.DomainCreationFailed as e:
                print "Domain creation failed:", e
        print "Domain created:", dom
        print

#Construct a list for your A record data, and insert it into a variable.
a_rec = {"type": "A",
        "name": domain_name,
        "data": ip_address,
        "ttl": 6000}

#Add the domain record with the dom variable used earlier.
recs = dom.add_records([a_rec])

print recs
print

