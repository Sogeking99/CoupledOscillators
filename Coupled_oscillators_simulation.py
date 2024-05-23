from vpython import *
import numpy as np
import matplotlib.pyplot as plt
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


# Parameters

def submit():
    if deviation_var.get() > 0.07:
        messagebox.showinfo("Obaveštenje", "Udaljenost od ekvilibrijuma ne može biti veća od 0.7.")
    else:
        mass_list = [var.get() for var in mass_variables.values()]
        m = np.array(mass_list)        # Masses of bodies

        k_list = [var.get() for var in k_variables.values()]
        k = np.array(k_list)             # Strength of springs
        n = len(m)                                  # Number of bodies

        if n+1 != len(k):
            messagebox.showinfo("Obaveštenje", "Neispravan broj tela i opruga.")
            sys.exit()

        x = np.zeros(n)     # Initial positions, set to 0 from equilibrium
        x[deviation_body.get()-1] = deviation_var.get()        # Setting one intial position sligtly away from equilibrium
        xdot = np.zeros(n)  # Inital velocities of bodies set to 0

        L = (n+1)*0.1       # Total length from wall 1 to wall 2
        dL = 0.1            # Distance between objects

        # Setting x coordinate for bodies (needed for graph drawing and animation drawing)
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
            # rate(100)

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


def create_text_fields(*args):
    # Clear any existing text fields
    for widget in mass_frame.winfo_children():
        widget.destroy()

    for widget in k_frame.winfo_children():
        widget.destroy()

    for widget in deviation_frame.winfo_children():
        widget.destroy()

    try:
        for i in range(num_of_bodies.get()):
            mass_variables[f'mass_var{i}'] = tk.DoubleVar()
            tk.Entry(mass_frame, textvariable=f'mass_var{i}').grid(row=1, column=i + 1, padx=10, pady=5)

        for i in range(num_of_bodies.get() + 1):
            k_variables[f'k_var{i}'] = tk.DoubleVar()
            tk.Entry(k_frame, textvariable=f'k_var{i}').grid(row=2, column=i + 1, padx=10, pady=5)

        options = [i for i in range(1, num_of_bodies.get() + 1)]
        dropdown = ttk.Combobox(deviation_frame, textvariable=deviation_body, values=options)
        dropdown.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        dropdown.current(0)
    except tk.TclError:
        # If the input is not a valid number, clear the text fields frame
        for widget in mass_frame.winfo_children():
            widget.destroy()

        for widget in k_frame.winfo_children():
            widget.destroy()

        for widget in deviation_frame.winfo_children():
            widget.destroy()


# GUI

root = tk.Tk()
root.title("Unos promenljivih")

tk.Label(root, text="Unesite broj tela:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
num_of_bodies = tk.IntVar()
num_of_bodies.trace('w', create_text_fields)
tk.Entry(root, textvariable=num_of_bodies).grid(row=0, column=1, padx=10, pady=5, sticky="w")

# Mass
tk.Label(root, text="Unesite mase tela:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
mass_frame = tk.Frame(root)
mass_frame.grid(row=1, column=1, padx=10, pady=10, sticky="w")

mass_variables = {}

# Constant k
tk.Label(root, text="Unesite konstante elastičnosti:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
k_frame = tk.Frame(root)
k_frame.grid(row=2, column=1, padx=10, pady=10, sticky="w")

k_variables = {}

# Equilibrium deviation
tk.Label(root, text="Izaberite telo van ekvilibrijuma:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
deviation_frame = tk.Frame(root)
deviation_frame.grid(row=3, column=1, padx=10, pady=10, sticky="w")

deviation_body = tk.IntVar()

tk.Label(root, text="Udaljeniost od ekvilibrijuma:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
deviation_var = tk.DoubleVar()
tk.Entry(root, textvariable=deviation_var).grid(row=4, column=1, padx=10, pady=5, sticky="w")

# Submit Button
tk.Button(root, text="Submit", command=submit).grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
