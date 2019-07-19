import numpy as np
import devfx.data_containers as dc

"""----------------------------------------------------------------
"""
v = [np.arange(0, 10, 1), 2*np.arange(0, 10, 1)]
v = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [ 0,  2,  4,  6,  8, 10, 12, 14, 16, 18]]
print(v)

print('\n')

"""----------------------------------------------------------------
"""
ds = dc.Dataset(v)

x = ds[:, :]
print(x)

print('\n')

"""----------------------------------------------------------------
"""
x = ds[0, :]
print(x)

x = ds[0:1, :]
print(x)

x = ds[0:2, :]
print(x)

print('\n')

"""----------------------------------------------------------------
"""
x = ds[:, 0]
print(x)

x = ds[:, 0:1]
print(x)

x = ds[:, 0:2]
print(x)

print('\n')

"""----------------------------------------------------------------
"""
x = ds[0, 0]
print(x)

x = ds[0:1, 0:1]
print(x)

x = ds[0:2, 0:2]
print(x)


