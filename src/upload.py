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

def load_data():
	"""Return the MNIST data as a tuple containing the training data,
	the validation data, and the test data.

	The ``training_data`` is returned as a tuple with two entries.
	The first entry contains the actual training images.  This is a
	numpy ndarray with 50,000 entries.  Each entry is, in turn, a
	numpy ndarray with 784 values, representing the 28 * 28 = 784
	pixels in a single MNIST image.

	The second entry in the ``training_data`` tuple is a numpy ndarray
	containing 50,000 entries.  Those entries are just the digit
	values (0...9) for the corresponding images contained in the first
	entry of the tuple.

	The ``validation_data`` and ``test_data`` are similar, except
	each contains only 10,000 images.

	This is a nice data format, but for use in neural networks it's
	helpful to modify the format of the ``training_data`` a little.
	That's done in the wrapper function ``load_data_wrapper()``, see
	below.
	"""
	
	cur = db.cursor()
	cur.execute("DELETE FROM intensities")
	cur.execute("DELETE FROM num_images")
	
	f = gzip.open('../data/mnist.pkl.gz', 'rb')
	training_data, validation_data, test_data = cPickle.load(f)
	count = 0
	image_no = 0
	for i in training_data[0]:
		sql_str = "INSERT INTO num_images VALUES (%s, %s, %s)"
		args = (image_no,'training', training_data[1][image_no])
		#print sql_str
		cur.execute(sql_str, args)
		
		pixel_no = 0
		for j in i:
			count += 1
			if (count % 1e6 == 0):
				print count
			sql_str = "INSERT INTO intensities VALUES (%s, %s, %s, %s)"
			args = (0, image_no, pixel_no, "{:.9f}".format(j))
			pixel_no += 1
			cur.execute(sql_str, args)

		image_no +=1
	db.commit()
	db.close()
	f.close()
	exit()
	return (training_data, validation_data, test_data)

def load_data_wrapper():
	"""Return a tuple containing ``(training_data, validation_data,
	test_data)``. Based on ``load_data``, but the format is more
	convenient for use in our implementation of neural networks.

	In particular, ``training_data`` is a list containing 50,000
	2-tuples ``(x, y)``.  ``x`` is a 784-dimensional numpy.ndarray
	containing the input image.  ``y`` is a 10-dimensional
	numpy.ndarray representing the unit vector corresponding to the
	correct digit for ``x``.

	``validation_data`` and ``test_data`` are lists containing 10,000
	2-tuples ``(x, y)``.  In each case, ``x`` is a 784-dimensional
	numpy.ndarry containing the input image, and ``y`` is the
	corresponding classification, i.e., the digit values (integers)
	corresponding to ``x``.

	Obviously, this means we're using slightly different formats for
	the training data and the validation / test data.  These formats
	turn out to be the most convenient for use in our neural network
	code."""
	tr_d, va_d, te_d = load_data()
	training_inputs = [np.reshape(x, (784, 1)) for x in tr_d[0]]
	training_results = [vectorized_result(y) for y in tr_d[1]]
	training_data = zip(training_inputs, training_results)
	validation_inputs = [np.reshape(x, (784, 1)) for x in va_d[0]]
	validation_data = zip(validation_inputs, va_d[1])
	test_inputs = [np.reshape(x, (784, 1)) for x in te_d[0]]
	test_data = zip(test_inputs, te_d[1])
	return (training_data, validation_data, test_data)

def vectorized_result(j):
	"""Return a 10-dimensional unit vector with a 1.0 in the jth
	position and zeroes elsewhere.  This is used to convert a digit
	(0...9) into a corresponding desired output from the neural
	network."""
	e = np.zeros((10, 1))
	e[j] = 1.0
	return e

print "hello"
training_data, validation_data, test_data = load_data_wrapper()

