#!/usr/bin/env python

'''
Challenge 4: Write a script that uses Cloud DNS to create 
a new A record when passed a FQDN and IP address as arguments. Worth 1 Point
'''

#Import the libraries we need for the script
import pyrax
import os
import sys
import pyrax.exceptions as exc

#Use our own auth exception, because it looks ugly otherwise.
creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")

try:
        pyrax.set_credential_file(creds_file)
except exc.AuthenticationFailed:
        print "Problem with credential file ~./rackspace_cloud_credentials"
print "Authenticated =", pyrax.identity.authenticated
print

#Import cloud_dns library 
dns = pyrax.cloud_dns

#Receive user input for the Domain Name and IP address for the A record.
domain_name = raw_input("Enter your A record name:")
ip_address = raw_input("Enter the IP Address:")

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

