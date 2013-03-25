#!/usr/bin/env python

import pyrax
import os
import sys
import pyrax.exceptions as exc


creds_file= os.path.expanduser("~/.rackspace_cloud_credentials")

try:
	pyrax.set_credential_file(creds_file)
except exc.AuthenticationFailed:
	print "Problem with credential file ~./rackspace_cloud_credentials"
print "Authenticated =", pyrax.identity.authenticated
print

cf = pyrax.cloudfiles
dns = pyrax.cloud_dns

cont = cf.create_container("challenge8")
print "Creating Container..."
print "Name:", cont.name
print "# of objects:", cont.object_count

cont.make_public(ttl=900)
print "Content is now Public"

print "Uploading Web Content..."
folder = "/var/www/"

upload_key, total_bytes = cf.upload_folder(folder, cont.name)

print "Upload Complete!"
print "cdn_enabled", cont.cdn_enabled
print "cdn_ttl", cont.cdn_ttl
print "cdn_log_retention", cont.cdn_log_retention
print "cdn_uri", cont.cdn_uri
print "cdn_ssl_uri", cont.cdn_ssl_uri
print "cdn_streaming_uri", cont.cdn_streaming_uri

domain_name="wiki-zone.info"

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


cname = {"type": "CNAME",
	"name": "test."+domain_name,
	"data": cont.cdn_uri,
	"ttl": 900}

recs = dom.add_records([cname])
print recs
print "DONE!"
