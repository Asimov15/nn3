#!/usr/bin/python

"""
mnist_loader
~~~~~~~~~~~~

A library to load the MNIST image data.  For details of the data
structures that are returned, see the doc strings for ``load_data``
and ``load_data_wrapper``.  In practice, ``load_data_wrapper`` is the
function usually called by our neural network code.
"""

#### Libraries
# Standard library
import cPickle
import gzip
import random
import MySQLdb
db = MySQLdb.connect(host="localhost",	# your host, usually localhost
					 user="julius",		# your username
					 passwd="happy1",	# your password
					 db="cicero")		# name of the data base

# Third-party libraries
import numpy as np

cur = db.cursor()
cur.execute("DELETE FROM intensities")
cur.execute("DELETE FROM num_images")
db.commit()
db.close()

