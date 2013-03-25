#!/usr/bin/env python

'''
Challenge 5: Write a script that creates a Cloud Database instance. 
This instance should contain at least one database, and the database 
should have at least one user that can connect to it. Worth 1 Point.
'''


#!/usr/bin/env python

import pyrax
import os
import pyrax.exceptions as exc

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")

try:
        pyrax.set_credential_file(creds_file)
except exc.AuthenticationFailed:
        print "Problem with credential file ~./rackspace_cloud_credentials"
print "Authenticated =", pyrax.identity.authenticated
print

cdb = pyrax.cloud_databases

inst = cdb.create("first_instance", flavor=1, volume=2)

print inst

pyrax.utils.wait_until(inst, "status", ['ACTIVE', 'ERROR'], interval=30, attempts=40, verbose=True)

db = inst.create_database("db_name")
print "DB:", db

user = inst.create_user(name="chris", password="pizza", database_names=[db])
print "User:", user
