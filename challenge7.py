#!/usr/bin/env python

'''
Challenge 7: Write a script that will create 2 Cloud Servers 
and add them as nodes to a new Cloud Load Balancer. Worth 3 Points
'''
#Import the libraries necessary for this script.
import pyrax
import time
import os

#Use our own auth code, because it is ugly otherwise
creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")

try:
        pyrax.set_credential_file(creds_file)
except exc.AuthenticationFailed:
        print "Problem with credential file ~./rackspace_cloud_credentials"
print "Authenticated =", pyrax.identity.authenticated
print

#Load Cloudservers and cloud_loadbalancers into a variable
cs = pyrax.cloudservers
clb = pyrax.cloud_loadbalancers

#Put our desired image information into a variable
image = [img for img in cs.images.list()
        if "12.10" in img.name][0]

#This finds the value for 512MB Ram and puts it into a variable
flavor = [flavor for flavor in cs.flavors.list()
        if flavor.ram == 512][0]

#Spawn Web1
web1 = cs.servers.create("web1", image, flavor)
#Store the server id for web1 in a variable
web1id = web1.id
#Print server information
print "Name:", web1.name, "\nID:", web1.id, \
"\nStatus:", web1.status, "\nAdmin Password:", web1.adminPass

#Spawn Web2
web2 = cs.servers.create("web2", image, flavor)
#Store the server id for web2 in a variable
web2id = web2.id
#Print server information
print "Name:", web2.name, "\nID:", web2.id, \
"\nStatus:", web2.status, "\nAdmin Password:", web2.adminPass

#Wait for networking to complete on both servers before moving on.
while not (web1.networks and web2.networks):
        time.sleep(10)
        print "Waiting for networks"
        web1 = cs.servers.get(web1id)
        web2 = cs.servers.get(web2id)

#Print networking for the servers
print "Web 1 Networking", \
"Public IP:", web1.networks["public"][1], \
"\nPrivate IP:", web1.networks["private"][0]

print "Web 2 Networking", \
"Public IP:", web2.networks["public"][1],\
"\nPrivate IP:", web2.networks["private"][0]

print "Server Builds Complete"

#Grab the internal IP's for the servers.
web1ip = web1.networks["private"][0]
web2ip = web2.networks["private"][0]

#Populate the data for the loadbalancer nodes and store in a variable.
node1 = clb.Node(address=web1ip, port=80, condition="ENABLED")
node2 = clb.Node(address=web2ip, port=80, condition="ENABLED")

#Spawn random load balancer name and store in a variable.
lbname = pyrax.utils.random_name(length=8)

#Populate the data vor the VIP and store in a variable.
vip = clb.VirtualIP(type="PUBLIC")

#Create the load balancer.
lb = clb.create(lbname, port=80, protocol="HTTP", virtual_ips=[vip], nodes=[node1, node2])

#Print all of the load balancer information.
print [(lb.name, lb.id) for lb in clb.list()]
