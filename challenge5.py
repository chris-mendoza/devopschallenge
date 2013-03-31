#!/usr/bin/env python

'''
Challenge 5: Write a script that creates a Cloud Database instance. 
This instance should contain at least one database, and the database 
should have at least one user that can connect to it. Worth 1 Point.
'''

#Import the libraries needed for our script.
import pyrax
import os
import pyrax.exceptions as exc

#Use our own exception for auth, because it's ugly otherwise
creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")

try:
        pyrax.set_credential_file(creds_file)
except exc.AuthenticationFailed:
        print "Problem with credential file ~./rackspace_cloud_credentials"
print "Authenticated =", pyrax.identity.authenticated
print

#Set the cloud database library to a variable
cdb = pyrax.cloud_databases

db_name = raw_input("Name your database")
user_name = raw_input("Database username?")
passwd = raw_input("Password?")
#Create a new object when we create out database.
inst = cdb.create("first_instance", flavor=1, volume=2)

print inst

#Wait until our instance has created.
pyrax.utils.wait_until(inst, "status", ['ACTIVE', 'ERROR'], interval=30, attempts=40, verbose=True)

#Create database inside of our instance.
db = inst.create_database(db_name)
print "DB:", db

#Create a user in our database
user = inst.create_user(name=user_name, password=passwd, database_names=[db])
print "User:", user
