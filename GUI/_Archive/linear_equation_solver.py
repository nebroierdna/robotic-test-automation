import numpy as np

# Define the coefficient matrix A and the constant vector b
A = np.array([[800, 700, 1, 0, 0, 0],
              [0, 0, 0, 800, 700, 1],
              [520, 500, 1, 0, 0, 0],
              [0, 0, 0, 520, 500, 1],
              [523, 398, 1, 0, 0, 0],
              [0, 0, 0, 523, 398, 1]])

b = np.array([1920, 980, 885, 464, 958, 429])

# Solve the system of equations
x = np.linalg.solve(A, b)

print(x)