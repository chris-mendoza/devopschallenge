#!/usr/bin/env python

'''
Challenge 4: Write a script that uses Cloud DNS to create 
a new A record when passed a FQDN and IP address as arguments. Worth 1 Point
'''

import pyrax
import os
import sys
import pyrax.exceptions as exc

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")

try:
        pyrax.set_credential_file(creds_file)
except exc.AuthenticationFailed:
        print "Problem with credential file ~./rackspace_cloud_credentials"
print "Authenticated =", pyrax.identity.authenticated
print

dns = pyrax.cloud_dns

domain_name = sys.argv[1]
ip_address = sys.argv[2]

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

a_rec = {"type": "A",
	"name": domain_name,
	"data": ip_address,
	"ttl": 6000}

recs = dom.add_records([a_rec])
print recs
print

