import numpy as np

A = [[[1, 5], [6, 2], [6, 1]],
     [[4, 2], [5, 7], [5, 2]]]

b = np.max([row[1][1] for row in A])

hh = 5