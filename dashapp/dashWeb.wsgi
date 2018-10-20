#!/usr/bin/python3.5
import sys
sys.path.insert(0, '/var/www/dashapp')
#from dashWeb import app as application
from dashWeb import server as application
print(application)
