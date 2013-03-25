#!/usr/bin/env python

'''
Challenge 7: Write a script that will create 2 Cloud Servers 
and add them as nodes to a new Cloud Load Balancer. Worth 3 Points
'''

import pyrax
import time
import os

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")

try:
        pyrax.set_credential_file(creds_file)
except exc.AuthenticationFailed:
        print "Problem with credential file ~./rackspace_cloud_credentials"
print "Authenticated =", pyrax.identity.authenticated
print


cs = pyrax.cloudservers
clb = pyrax.cloud_loadbalancers

image = [img for img in cs.images.list()
        if "12.10" in img.name][0]

flavor = [flavor for flavor in cs.flavors.list()
        if flavor.ram == 512][0]


web1 = cs.servers.create("web1", image, flavor)
web1id = web1.id
print "Name:", web1.name, "\nID:", web1.id, \
"\nStatus:", web1.status, "\nAdmin Password:", web1.adminPass
web2 = cs.servers.create("web2", image, flavor)
web2id = web2.id
print "Name:", web2.name, "\nID:", web2.id, \
"\nStatus:", web2.status, "\nAdmin Password:", web2.adminPass

while not (web1.networks and web2.networks):
        time.sleep(10)
        print "Waiting for networks"
        web1 = cs.servers.get(web1id)
        web2 = cs.servers.get(web2id)

print "Web 1 Networking", \
"Public IP:", web1.networks["public"][1], \
"\nPrivate IP:", web1.networks["private"][0]

print "Web 2 Networking", \
"Public IP:", web2.networks["public"][1],\
"\nPrivate IP:", web2.networks["private"][0]

print "Server Builds Complete"
web1ip = web1.networks["private"][0]
web2ip = web2.networks["private"][0]

node1 = clb.Node(address=web1ip, port=80, condition="ENABLED")
node2 = clb.Node(address=web2ip, port=80, condition="ENABLED")

lbname = pyrax.utils.random_name(length=8)
vip = clb.VirtualIP(type="PUBLIC")
lb = clb.create(lbname, port=80, protocol="HTTP", virtual_ips=[vip], nodes=[node1, node2])

print [(lb.name, lb.id) for lb in clb.list()]
