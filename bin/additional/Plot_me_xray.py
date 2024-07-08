# Author: M. Reichert
import numpy as np
import matplotlib.pyplot as plt


fig, ax = plt.subplots(1, 1)
plt.title('X-ray burst')

def sum_over(A,X):
    """
     Sum mass fractions over equal mass numbers
    """
    max_A = max(A)
    X_new = np.zeros([max_A+1,])
    for i in range(len(A)):
        X_new[int(A[i])] += X[i]
    return np.array(range(max_A+1)),X_new

# Load the final abundances of Euler
A,Z,N,Y,X = np.loadtxt("runs/Example_xrayburst_schatz_euler/finab.dat",unpack=True)

# Sum over equal A's
A_summed, X_summed = sum_over(A.astype(int),X)

# Plot Euler
ax.plot(A_summed,X_summed,label="Backward Euler")

# Load WinNet
A,Z,N,Y,X = np.loadtxt("runs/Example_xrayburst_schatz_x-tfc/finab.dat",unpack=True)

# Sum over equal A's
A_summed, X_summed = sum_over(A.astype(int),X)

# Plot WinNet
ax.plot(A_summed,X_summed,label="X-TFC",linestyle='dashed')

# Show the legend
plt.legend()
plt.xlabel("Mass number A")
plt.ylabel("Mass fraction X")
plt.ylim(1e-10,1)
plt.yscale("log")
plt.grid()
plt.savefig("runs/xrayburst.pdf",bbox_inches="tight")
plt.show()

