#!/usr/bin/env python

'''
Challenge 3:
Write a script that accepts a directory as an argument as well as a container name. 
The script should upload the contents of the specified directory to the container (or create it if it doesn't exist). 
The script should handle errors appropriately. (Check for invalid paths, etc.) Worth 2 Points
'''

#import the libraries needed for this script
import pyrax
import os
import sys
import pyrax.exceptions as exc
import fnmatch


#Begin authentication script
creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")

#Handle incorrect credentials ourselves, because it's ugly otherwise
try:
        pyrax.set_credential_file(creds_file)
except exc.AuthenticationFailed:
        print "Problem with credential file ~./rackspace_cloud_credentials"
print "Authenticated =", pyrax.identity.authenticated
print

#Specify that we're going to be using the Cloudfiles library
#and set it to the variable 'cf'.
cf = pyrax.cloudfiles

#Take user input for a directory, and set it to the variable 'folder'
folder = raw_input("Which directory would you like to upload?\n")

#Here's some error checking for the directory. If it does not exist,
#it is created automatically.
if not os.path.exists(folder):
	print "Oh no! Folder does not exist. Creating it now!"
	os.makedirs(folder)


#Take user input for the container we want to upload the folder to.
#We will put this in the variable named 'contname'
contname = raw_input("Which container would you like to upload this to?\n")
print "Contname:", contname

#List all of the cloudfiles container, and dump them into a variable.
obj_list = [obj for obj in cf.list_containers()
	if fnmatch.fnmatch(contname, obj)]

objs = str(obj_list)[3:-2] 
print objs 

#If the container does not exist, it is created automatically,
#otherwise it asks if you would like to overwrite any files that 
#have the same name.

if contname == objs:
        print "These containers are the same!"
        answer = raw_input("Would you like to continue anyway? This may overwrite some data![y/n]")
        if not answer.lower().startswith("y"):
                sys.exit()
        else:
                cont = cf.create_container(contname)
   
else:
        print "Container does not exist, create it now!"
        cont = cf.create_container(contname) 

#Return all the valuable data about our container.
print "Name:", cont.name, \
"\n# of objects:", cont.object_count

#Upload all files in the specified folder to the container.
print "\nUploading Web Content..."

upload_key, total_bytes = cf.upload_folder(folder, container=contname)

print "\n Upload Complete!"
#Ask if you want CDN enabled every time it syncs.
if cont.cdn_enabled == True:
        print "-"*30, "\nName:", cont.name, \
        "\n# of objects:", cont.object_count, \
        "\ncdn_enabled", cont.cdn_enabled, \
        "\ncdn_ttl", cont.cdn_ttl, \
        "\ncdn_log_retention", cont.cdn_log_retention, \
        "\ncdn_uri", cont.cdn_uri, \
        "\ncdn_ssl_uri", cont.cdn_ssl_uri, \
        "\ncdn_streaming_uri", cont.cdn_streaming_uri
        sys.exit()

elif cont.cdn_enabled == False:
        answer2 = raw_input("Would you like to CDN Enable this container?[y/n]")
	if answer2.lower().startswith("y"):
                cont.make_public(ttl=900)
                print "-"*30, "\nName:", cont.name, \
                "\n# of objects:", cont.object_count,\
                "\ncdn_enabled", cont.cdn_enabled, \
                "\ncdn_ttl", cont.cdn_ttl, \
                "\ncdn_log_retention", cont.cdn_log_retention, \
                "\ncdn_uri", cont.cdn_uri, \
                "\ncdn_ssl_uri", cont.cdn_ssl_uri, \
                "\ncdn_streaming_uri", cont.cdn_streaming_uri        
        
        elif not answer2.lower().startswith("y"):
                print "-"*30, "\nName:", cont.name, \
                "\n# of objects:", cont.object_count, \
                "\ncdn_enabled", cont.cdn_enabled, \
                sys.exit()
