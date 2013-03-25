#!/usr/bin/env python

'''
Challenge 3:
Write a script that accepts a directory as an argument as well as a container name. 
The script should upload the contents of the specified directory to the container (or create it if it doesn't exist). 
The script should handle errors appropriately. (Check for invalid paths, etc.) Worth 2 Points
'''


import pyrax
import os
import sys
import pyrax.exceptions as exc

pyrax.set_credentials("cmendoza89", "15c9d8d539ee70bf12865151fce55ee0")

pyrax.authenticate()

cf = pyrax.cloudfiles

folder = sys.argv[1]
cont = cf.create_container(sys.argv[2])

print "Creating Container..."
print "Name:", cont.name
print "# of objects:", cont.object_count

print "Uploading Web Content..."

upload_key, total_bytes = cf.upload_folder(folder, cont.name)

print "Upload Complete!"
print "Name:", cont.name
print "# of objects:", cont.object_count
print "cdn_enabled", cont.cdn_enabled
print "cdn_ttl", cont.cdn_ttl
print "cdn_log_retention", cont.cdn_log_retention
print "cdn_uri", cont.cdn_uri
print "cdn_ssl_uri", cont.cdn_ssl_uri
print "cdn_streaming_uri", cont.cdn_streaming_uri



