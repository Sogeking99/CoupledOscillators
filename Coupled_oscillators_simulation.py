from vpython import *
import numpy as np
import matplotlib.pyplot as plt
import sys


# Parameters

m = np.array([0.2, 0.15, 0.7, 0.15])        # Masses of bodies
k = np.array([10, 5, 5, 20, 7])             # Strength of springs       
n = len(m)                                  # Number of bodies

if n+1 != len(k):
    sys.exit()

x = np.zeros(n)     # Initial positions, set to 0 from equilibrium
x[0] = 0.03         # Setting one intial position sligtly away from equilibrium
xdot = np.zeros(n)  # Inital velocities of bodies set to 0

L = (n+1)*0.1       # Total length from wall 1 to wall 2
dL = 0.1            # Distance between objects

# Setting x cooridinate for bodies (needed for graph drawing and animation drawing)
# We are setting each body 0.1m away from previous.
x_positions = np.zeros(n)
for i in range(0, n):
    x_positions[i] = i*dL + dL

# Time init
t = 0
t_max = 10
dt = 0.01
t_array = np.arange(0, t_max, dt)

# Matrix to store positions and analytical solutions for plotting
solution_matrix = []
for i in range(n):    
    a = []
    solution_matrix.append(a)


# Animation settings

# Static spheres to represent wall 1 and wall 2
left = sphere(pos=vector(-L/2,0,0),radius=0.01, color=color.red)
right = sphere(pos=vector(L/2,0,0),radius=0.01, color=color.red)

# Bodies as blue objects
cars = []
for i in range(n):    
    a = box(pos=vector(left.pos.x + (i+1)*dL + x[i],0,0),size=vector(0.03,0.02,0.02), color=color.blue)
    cars.append(a)

# Springs
springs = []
for i in range(n+1):
    if i == 0:
        a = helix(pos=left.pos, axis = cars[0].pos-left.pos, radius=0.005, thickness=0.003)
        springs.append(a)
    elif i == n:
        a = helix(pos=cars[i-1].pos, axis = right.pos - cars[i-1].pos, radius = 0.005, thickness=0.003)
        springs.append(a)
    else:
        a = helix(pos=cars[i-1].pos, axis = cars[i].pos - cars[i-1].pos, radius = 0.005, thickness=0.003)
        springs.append(a)

t += dt
while t<t_max:
    rate(100)

    for  i in range(0,n):

        # Using Hooke's law to calculate force on each body (F = -k*x)
        F = 0.0

        if i == 0:
            F = -k[0]*x[0]-k[1]*(x[0]-x[1])                 # First body in a row, having wall on left and body on right side

        elif i == n-1:
            F = -k[n-1]*(x[n-1]-x[n-2])-k[n]*x[n-1]         # Last body in a row, having body on left and wall on the right side

        else: 
            F = -k[i+1]*(x[i]-x[i+1]) - k[i]*(x[i]-x[i-1])  # Body between two other bodies

        xddot = 0.0
        xddot = F / m[i]        # Newton's second law F = m*a  => a = F/m
        xdot[i] += xddot * dt
        x[i] += xdot[i]*dt

        solution_matrix[i].append(x[i] + x_positions[i])
  
  
    # Iscrtavanje animacije
    for i in range(n):
        cars[i].pos = vector(left.pos.x + (i+1)*dL + x[i], 0, 0)
  
    
    for i in range(0,n+1):
        if i == 0:
            springs[0].axis = cars[0].pos - left.pos
        elif i == n:
            springs[i].pos = cars[i-1].pos
            springs[i].axis = right.pos - cars[i-1].pos
        else:
            springs[i].pos = cars[i-1].pos
            springs[i].axis = cars[i].pos - cars[i-1].pos

    # Loop constraint
    t = t + dt

# Plotting the results
plt.figure(figsize=(10, 6))

for i in range(n-1, -1, -1):
    s = "x" + str(i+1)
    if i%2  == 0:
        plt.plot(t_array, solution_matrix[i], label=s, color='purple')
    else:
        plt.plot(t_array, solution_matrix[i], label=s, color='blue')

plt.xlabel('Time (seconds)')
plt.ylabel('Position (meters)')
plt.title('Oscilating motion')
plt.legend()
plt.grid(True)
plt.show()
