import matplotlib.pyplot as plt
import numpy as np

x = [0.0, 0.282, 0.482, 1.015, 1.515]
y = [0.383, 2.57, 5.51, 9.98, 14.9]


m, b = np.polyfit(np.array(x), np.array(y), 1)
print(m, b)