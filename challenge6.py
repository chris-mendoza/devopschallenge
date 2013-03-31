#!/usr/bin/env python

'''
Challenge 6: Write a script that creates a CDN-enabled container in Cloud Files. Worth 1 Point
'''
#Import the necessary libraries for this script.
import pyrax
import os

#Use our own Auth code, because it is ugly otherwise
creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")

try:
        pyrax.set_credential_file(creds_file)
except exc.AuthenticationFailed:
        print "Problem with credential file ~./rackspace_cloud_credentials"
print "Authenticated =", pyrax.identity.authenticated
print

#Connect to CloudFiles
cf = pyrax.cloudfiles

#Get user input for our container name.

cont_name = raw_input("What is your container named?\n")

#Create the container, and create an object for it.
cont = cf.create_container(cont_name)

#Use the cont object to print our new containers data.
print "Name:", cont.name
print "# of objects:", cont.object_count

#CDN Enable the container by passing the cont object through
#its built in object "make_public" and set the ttl for 900(seconds).
cont.make_public(ttl=900)

#Pass the cont object through more attributes and print out 
#the data about our CDN enabled object.
print "cdn_enabled", cont.cdn_enabled
print "cdn_ttl", cont.cdn_ttl
print "cdn_log_retention", cont.cdn_log_retention
print "cdn_uri", cont.cdn_uri
print "cdn_ssl_uri", cont.cdn_ssl_uri
print "cdn_streaming_uri", cont.cdn_streaming_uri
