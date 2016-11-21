# -*- coding: utf-8 -*-
# File get_sample.py
"""
Projet: Vocal controlled synthL
date: octobre 2016
UPMC, Master SdI, acoustique
@authors: lauraparra & victorwetzel
"""


import numpy as np
### FUNCTION: record
# This function get samples from
# the computer's microphone.

def record(stream,chunk):
	# Read raw microphone data
    rawsamples = stream.read(chunk)#, exception_on_overflow = False)
    # Convert raw data to NumPy array
    samples = np.fromstring(rawsamples, dtype=np.int16)
     
    return samples
    