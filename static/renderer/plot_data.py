with open("data") as f:
    data = f.read().strip().split(",")
    data = [int(x) for x in data if len(x) != 0]


import matplotlib.pyplot as plt
import numpy as np

d = np.array(data).reshape((520, 504))/2

print(d.shape)

plt.imshow(d, cmap="Greys")
plt.show()
