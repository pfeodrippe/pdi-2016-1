import numpy as np
import cv2
import math
import subprocess
import os

def mse(imageA, imageB):
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	return err

def psnr(imageA, imageB):
	m = mse(imageA, imageB)
	return 10 * math.log(255/m, 10)

def test_for_image(n, k):
	number = str(n).zfill(2)
	with open(os.devnull, 'w') as devnull:
		output = subprocess.check_output(('./../binarizewolfjolion-cpp/binarize -k ' + str(k) + ' ../original_images/H' + number + '.png ../processed_images/P' + number + '.png').split(), stderr=devnull)

def load_image(n): 
	number = str(n).zfill(2)
	original = cv2.imread("./../GT/H" + number + "_estGT.tiff")
	contrast = cv2.imread("./../processed_images/P" + number + ".png")
	original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
	contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
	return (original, contrast)

def search_for_best_in_image(n):
	offset = 0.1
	k = 0.5
	flag = True
	processed_numbers = []

	while flag == True:
		test_for_image(n, k)
		original, contrast = load_image(n)
		now = psnr(original, contrast)

		test_for_image(n, k - offset)
		original, contrast = load_image(n)
		before = psnr(original, contrast)

		test_for_image(n, k + offset)
		original, contrast = load_image(n)
		after = psnr(original, contrast)

		if now >= before and now >= after:
			print "BEST"
			print k
			print now
			flag = False
			return now
		elif before > after:
			k = k - offset
		else:
			k = k + offset

		if k in processed_numbers:
			offset *= 0.8
		else:
			processed_numbers.append(k)

		print k

psnr_arr = []
for i in xrange(1, 11):
	print "Image " + str(i).zfill(2)
	p = search_for_best_in_image(i)
	psnr_arr.append(p)
	print ""

print reduce(lambda x, y: x + y, psnr_arr) / len(psnr_arr)


