#!/usr/bin/env python

'''
Challenge 6: Write a script that creates a CDN-enabled container in Cloud Files. Worth 1 Point
'''

import pyrax
import os

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")

try:
        pyrax.set_credential_file(creds_file)
except exc.AuthenticationFailed:
        print "Problem with credential file ~./rackspace_cloud_credentials"
print "Authenticated =", pyrax.identity.authenticated
print

cf = pyrax.cloudfiles

cont = cf.create_container("challenge6")
print "Name:", cont.name
print "# of objects:", cont.object_count

cont.make_public(ttl=900)

print "cdn_enabled", cont.cdn_enabled
print "cdn_ttl", cont.cdn_ttl
print "cdn_log_retention", cont.cdn_log_retention
print "cdn_uri", cont.cdn_uri
print "cdn_ssl_uri", cont.cdn_ssl_uri
print "cdn_streaming_uri", cont.cdn_streaming_uri
