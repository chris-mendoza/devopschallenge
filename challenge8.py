#!/usr/bin/env python

'''
Challenge 8: Write a script that will create a static webpage 
served out of Cloud Files. The script must create a new container,
cdn enable it, enable it to serve an index file, create an index 
file object, upload the object to the container, and create a CNAME 
record pointing to the CDN URL of the container. Worth 3 Points
'''

#Import the necessary libraries for our script.
import pyrax
import os
import sys
import pyrax.exceptions as exc
import fnmatch

#Use our own auth code, because it looks ugly otherwise.
creds_file= os.path.expanduser("~/.rackspace_cloud_credentials")

try:
	pyrax.set_credential_file(creds_file)
except exc.AuthenticationFailed:
	print "Problem with credential file ~./rackspace_cloud_credentials"
print "Authenticated =", pyrax.identity.authenticated
print

#Store Cloud Files and DNS into variables
cf = pyrax.cloudfiles
dns = pyrax.cloud_dns

#Get User input for the container name and domain
domain_name = raw_input("What Domain will we be using?\n")
cname_pre = raw_input("What is the CNAME prefix?")
contname = raw_input("Container Name? \n")
sitedata = raw_input("What is the site going to say?\n ")

#List all of the containers, and dump them into a variable.
obj_list = [obj for obj in cf.list_containers()
        if fnmatch.fnmatch(contname, obj)]

objs = str(obj_list)[3:-2]
print objs

#Test if the container exists, if not, create it.

if contname == objs:
        print "*"*30, "\nThese containers are the same!"
        answer = raw_input("Would you like to continue anyway? This may overwrite some data![y/n]")
        if not answer.lower().startswith("y"):
                sys.exit()
        else:
                cont = cf.create_container(contname)

else:
        print "Container does not exist, creating it now!"
        cont = cf.create_container(contname)

#Make Container Public (CDN Enable)
cont.make_public(ttl=900)
print "Content is now Public"


print "*"*30, "\nName:", cont.name, \
"\n# of objects:", cont.object_count, \
"\ncdn_enabled", cont.cdn_enabled, "\ncdn_ttl", cont.cdn_ttl, \
"\ncdn_log_retention", cont.cdn_log_retention, \
"\ncdn_uri", cont.cdn_uri, "\ncdn_ssl_uri", cont.cdn_ssl_uri, \
"\ncdn_streaming_uri", cont.cdn_streaming_uri

#Set web index page.
print "We have uploaded your site input as the file: index.html"

cont.set_web_index_page("index.html")

#Create the index.html
site = '''<HTML>
<TITLE>Temporary Site</TITLE>
<MARQUEE>%s</MARQUEE>
</HTML>''' %(sitedata)

#Store the site
siteobj = cf.store_object(contname, "index.html", site)

#If the domain does not exist, ask if it should be created.
try:
        dom = dns.find(name=domain_name)
except exc.NotFound:
        answer = raw_input("The domain '%s' was not found. Do you want to create it? [y/n]" % domain_name)
        if not answer.lower().startswith("y"):
                sys.exit()
        else:
                try:
                        dom = dns.create(name=domain_name, emailAddress="sample@example.com", ttl=900, comment="sampledomain")
                except exc.DomainCreationFailed as e:
                        print "Domain creation failed:", e
        print "Domain created:", dom
        print

cname_total = (cname_pre+"."+domain_name)

cname = {"type": "CNAME",
        "name": cname_total,
        "data": cont.cdn_uri,
        "ttl": 900}

try:
       subdom = dns.create(name=cname_total, emailAddress="meh@wiki-zone.info", ttl=600, comment="meh") 
except exc.DomainCreationFailed as e:
       print "Could not create '%s': %s" % (cname_total, e)
       print
       sys.exit()
    
print "We have successfully created the CNAME '%s'." % cname_total
print subdom
print
