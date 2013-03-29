#!/usr/bin/env python

#Challenge 2:Write a script that clones a server 
#(takes an image and deploys the image as a new server). Worth 2 Point


#Import the libraries we need for this script.
import pyrax
import time
import pyrax.exceptions as exc
import os

#Authenticate via credential file
creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")

#Authenticate with our own code, because it looks ugly otherwise.
#If it cannot authenticate, it will give a custom error message.
try:
        pyrax.set_credential_file(creds_file)
except exc.AuthenticationFailed:
        print "Problem with credential file ~./rackspace_cloud_credentials"
print "Authenticated =", pyrax.identity.authenticated
print

#Connects to cloud files if authenticate goes through.
pyrax.connect_to_cloudservers()

#Call pyrax.cloudservers library, and store it in the variable 'cs' 
cs = pyrax.cloudservers

#Get user input for what they would like to name their image.
imgname = raw_input("Please provide us with an image name\n")

#Get user input for which server ID they would like to use
#in the imaging process
serverid = raw_input("Please provide us with a server ID\n")

#Query Cloud Servers for the desired server, by ID
get_server = cs.servers.get(serverid)

#Create a unique image, no other image can be created at the same time,
#so this method works pretty well using date/time stamp.
new_image = get_server.create_image(imgname+time.strftime('%Y-%m-%d %H:%M:%S'))

#Iterate through the images list, and find our new_image id.
image = [img for img in cs.images.list()
        if new_image in img.id][0]

#Wait until our image has finished being created.
pyrax.utils.wait_until(image, "status", ['ACTIVE', 'ERROR'], \
interval=30, attempts=40, verbose=True)

#Get the same flavor of the server we took an image of.
flavor = get_server.flavor['id']

#Create a unique servername that can be changed at a later time.
#This is to avoid any confusion.
server_name = str(get_server.name+time.strftime('%Y-%m-%d %H:%M:%S'))

#Create the server with the previously set variables.
new_server = cs.servers.create(server_name, image.id, flavor)

#Save the ID of our new server for future uses.
new_serverid = new_server.id

#Print out valuable data about our new server.
print "="*30, "\nName:", new_server.name, "\nID:", new_server.id, \
"\nStatus:", new_server.status, "\nAdmin Password:", new_server.adminPass

#While not loop to wait for our servers networking to populate.
#This will print out our servers IP's when it's done.
while not(new_server.networks):
        time.sleep(45)
        new_server = cs.servers.get(new_serverid)
        print "\nIPv4:", new_server.networks["public"][0], \
        "\nIPv6:", new_server.networks["public"][1], \
        "\nPrivate IP:", new_server.networks["private"][0]

#Fluff text to let you know the script is still working.
print "="*30, "\nWaiting for server to build..."
pyrax.utils.wait_until(new_server, "status", ['ACTIVE','ERROR'], interval=30, attempts=40, verbose=True)
print "Server Build Complete"
