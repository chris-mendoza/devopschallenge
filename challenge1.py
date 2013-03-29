#!/usr/bin/env python

#Challenge:  Write a script that builds three 512 MB Cloud Servers that following a similar naming convention. 
#(ie., web1, web2, web3) and returns the IP and login credentials for each server. Use any image you want. 
#Worth 1 point


import pyrax
import pyrax.exceptions as exc
import os
import time
import sys

#Set the credential directory, and assign it to the variable "creds_file"
creds_file= os.path.expanduser("~/.rackspace_cloud_credentials")

#Let's handle the credential failure ourself, because it looks ugly otherwise.
try:
        pyrax.set_credential_file(creds_file)
except exc.AuthenticationFailed:
        print "Problem with credential file ~./rackspace_cloud_credentials"
print "Authenticated =", pyrax.identity.authenticated
print

#Pass the credential variable to pyrax
pyrax.set_credential_file(creds_file)

#Connect to Cloud Servers with Pyrax
pyrax.connect_to_cloudservers()

#Storing the cloudservers library to a variable "cs"
cs = pyrax.cloudservers

#Search for Ubuntu 12.10 image, and store it in the variable named "image"
image = [img for img in cs.images.list()
        if "12.10" in img.name][0]

#Searches for the flavor 512, and stores it to the variable named "flavor"
flavor = [flavor for flavor in cs.flavors.list()
        if flavor.ram == 512][0]

#Store data from the user in a variable for the amount of servers.
#this one needs to be printed first, because we're trying to grab an integer.
print "How many servers would you like to create? "
servernum = int(raw_input())

#Store data from the user for the server prefix in a variable.
prefix = raw_input('What prefix would you like to use in your server name?\n')

#Show user input to assist in later deciding what they would like to do.
print "You are now creating ", servernum, " server(s)"
print "Your prefix is:"+prefix

#Confirm that this is what you would like to do
answer = raw_input("Would you like to proceed? [y/n] ")
if not answer.lower().startswith("y"):
	sys.exit()

#Server name list variable
names = []
print "Creating Server...Sit back this may take a while.."

#A loop to create the desired amount of servers, with the desired prefix,
#and a different name...
for i in xrange(1, servernum+1, 1):
        
        #append the prefix to a number so all the names aren't the same
	name = prefix + str(i)
	
        #add the name to the list ever iteration.
        names.extend([name])

        #grab the last server on the list, always. 
        server_name = (max(names))
	
        #Create the server, using the user specified data
        new_server = cs.servers.create(server_name, image.id, flavor.id)        

        #print out server information.
        print "-"*30, "\nName:", new_server.name, "\nID:", new_server.id,\
        "\nStatus:", new_server.status, "\nAdmin Password:", new_server.adminPass
        
        #used in the while loop to refresh the variable every iteration.       
        new_serverid = new_server.id

	#Wait for networking to populate before moving on.
        while not (new_server.networks):
                #wait 30 seconds before moving on
		time.sleep(50)
        #refreshes the new_server value to be tested again on next iteration
                new_server = cs.servers.get(new_serverid)
                #Print out networking information
                print "IPv4:", new_server.networks["public"][1], \
                "\nIPv6:", new_server.networks["public"][0], \
                "\nPrivate IP", new_server.networks["private"][0]

