import h5py
import numpy as np
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Path to input numpy file", required=True)
parser.add_argument("-o", "--output", help="Path to output HDF file", required=True)

args = parser.parse_args()
file = np.load(args.input + str(0) + "_processed.npz")
X_cat = file['X_cat']
X_int = file['X_int']
y = file['y']
print(X_cat.shape)
print(X_cat[0])
for i in range(2):
  A = np.load(args.input + str(i+4) + "_processed.npz")
  X_cat = np.concatenate([A['X_cat'], X_cat])
  X_int = np.concatenate([A['X_int'], X_int])
  y = np.concatenate([A['y'], y])
  print(X_cat.shape)
  #file = np.concatenate([file,A])
hdf = h5py.File(args.output, 'w')

X_cat = X_cat.astype(np.long)
hdf.create_dataset("X_cat", data=X_cat)

X_int = np.log(X_int.astype(np.float32) + 1)
hdf.create_dataset("X_int", data=X_int)

y = y.astype(np.float32)
hdf.create_dataset("y", data=y)
