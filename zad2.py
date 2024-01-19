from pyomo.environ import *

Demand = {
    'Customer1': 25,
    'Customer2': 25,
    'Customer3': 40,
    'Customer4': 30,
    'Fictional_Customer': 5
}               # 25 + 25 + 40 + 30 = 120 + 5 = 125

Supply = {
    'Supplier1': 30,
    'Supplier2': 35,
    'Supplier3': 60
}               # 30 + 35 + 60 = 125

T = {
    ('Customer1', 'Supplier1'): 5, ('Customer2', 'Supplier1'): 5, ('Customer3', 'Supplier1'): 6, ('Customer4', 'Supplier1'): 2, ('Fictional_Customer', 'Supplier1'): 0,
    ('Customer1', 'Supplier2'): 1, ('Customer2', 'Supplier2'): 7, ('Customer3', 'Supplier2'): 4, ('Customer4', 'Supplier2'): 2, ('Fictional_Customer', 'Supplier2'): 0,
    ('Customer1', 'Supplier3'): 6, ('Customer2', 'Supplier3'): 3, ('Customer3', 'Supplier3'): 2, ('Customer4', 'Supplier3'): 1, ('Fictional_Customer', 'Supplier3'): 0
    }

model = ConcreteModel()
model.dual = Suffix(direction=Suffix.IMPORT)

customers = list(Demand.keys())
suppliers = list(Supply.keys())

model.x = Var(customers, suppliers, domain=NonNegativeReals)


@model.Objective(sense=minimize)
def cost(m):
    return sum([T[c, s] * model.x[c, s] for c in customers for s in suppliers])


@model.Constraint(suppliers)
def src(m, s):
    return sum([model.x[c, s] for c in customers]) <= Supply[s]


@model.Constraint(customers)
def dmd(m, c):
    return sum([model.x[c, s] for s in suppliers]) == Demand[c]


results = SolverFactory('glpk').solve(model)

if 'ok' == str(results.Solver.status):
    print("Total Shipping Costs = ", value(model.cost))
    print("\nShipping Table:")
    for s in suppliers:
        for c in customers:
            if model.x[c, s]() > 0:
                print("Ship from ", s, " to ", c, ":", model.x[c, s]())
else:
    print("No Valid Solution Found")
