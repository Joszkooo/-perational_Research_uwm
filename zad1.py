from pyomo.environ import *
import matplotlib.pyplot as plt
import numpy as np

# Function to plot the constraints and the solution
def plot(model):
    x1 = np.linspace(-2, 4, 400)
    x2 = np.linspace(-2, 4, 400)

    # Constraints
    c1 = (1 - x1)  # x1 - x2 <= 1
    c2 = 2 - x1     # x1 + x2 <= 2
    c3 = (0 - x1) / -2  # x1 - 2*x2 >= 0
    c4 = (1 - 2 * x1) / 2  # 2*x1 + 2*x2 >= 1

    # Plot constraints
    plt.figure(figsize=(8, 6))
    plt.plot(x1, c1, label=r'$x_1 - x_2 \leq 1$', color='blue')
    plt.plot(x1, c2, label=r'$x_1 + x_2 \leq 2$', color='green')
    plt.plot(x1, c3, label=r'$x_1 - 2x_2 \geq 0$', color='orange')
    plt.plot(x1, c4, label=r'$2x_1 + 2x_2 \geq 1$', color='yellow')

    # Plot feasible region
    plt.fill_between(x1, np.minimum.reduce([c1, c2, c3, c4]), where=(x1 >= 0), interpolate=True, color='gray', alpha=0.5)

    # Optimal point
    plt.plot(model.x1(), model.x2(), 'ro')
    plt.text(model.x1(), model.x2(), f'  Optimal\n  ({model.x1():.2f}, {model.x2():.2f})',
             verticalalignment='bottom')

    plt.xlim(-2, 4)
    plt.ylim(-2, 4)
    plt.xlabel('$x_1$')
    plt.ylabel('$x_2$')
    plt.title('Linear Programming Solution')
    plt.legend()

    plt.savefig('plot_exercise1.png', dpi=300)
    plt.show()

# Function to run the optimization model
def run(verbose: bool = False):
    model = ConcreteModel()
    model.x1 = Var(domain=NonNegativeReals)
    model.x2 = Var(domain=NonNegativeReals)

    # Objective
    model.objective_function = Objective(expr=model.x1 + 2 * model.x2, sense=minimize)

    # Constraints
    model.c1 = Constraint(expr=model.x1 - model.x2 <= 1)
    model.c2 = Constraint(expr=model.x1 + model.x2 <= 2)
    model.c3 = Constraint(expr=model.x1 - 2 * model.x2 >= 0)
    model.c4 = Constraint(expr=2 * model.x1 + 2 * model.x2 >= 1)

    # Solve
    SolverFactory('glpk').solve(model).write()

    print('*** *** *** ***')
    model.objective_function.display()
    model.x1.display()
    model.x2.display()
    if verbose:
        plot(model)

if __name__ == '__main__':
    run(verbose=True)
