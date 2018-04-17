import numpy as np

def movingaverage(data, window_size):
    """
    compute moving average with window
    np.ones returns a vector with 1's

    """

    window= np.ones(int(window_size))/float(window_size)

    return np.convolve(data, window, 'same')
