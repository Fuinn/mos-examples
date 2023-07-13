#@ Model: Knapsack Model
#@ Description: Sample knapsack model in JuMP $$\max p^T x$$$$w^T x \leq k$$$$x\in\{0,1\}^5$$

using JuMP, Cbc, JSON

# Labels
items = Dict()
for i in 1:5
    items[i] = "item_$(i)"
end

#@ Input File: profit_file
#@ Description: This is a sample input file
profit_file = open("./src/jump/knapsack/profit.json")

#@ Input Object: weight
#@ Description: Weight of items, w
weight = [2, 8, 4, 2, 5]

#@ Input Object: capacity
#@ Description: Capacity of knapsack, k
capacity = 10

#@ Helper object: profit
#@ Description: Profit of each item, p
profit = convert(Array{Int64,1}, JSON.parse(profit_file))

#@ Solver: solver
solver = Cbc.Optimizer

#@ Problem: model
model = Model(optimizer_with_attributes(solver, "print_level" => 1))

#@ Variable: x
#@ Description: 1 if an item is included in knapsack, 0 otherwise$$x\in\{0,1\}^5$$
#@ Labels: items
@variable(model, x[1:5], Bin)


#@ Function: objectivefn
#@ Description: objective function $$p^T x$$
@expression(model, objectivefn, profit' * x)


#@ Constraint: cap_constr
#@ Description: Items placed in knapsack may not exceed capacity $$w^T x \leq k$$
@constraint(model, 
            cap_constr, 
            convert(Array{Int64,1}, weight)' * x <= capacity)


# Execution: 
@objective(model, Max, objectivefn)
JuMP.optimize!(model)

#@ Output object: sum_x
#@ Description: This is a sample output objet
sum_x = sum(JuMP.value.(x))

#@ Output file: output.txt
#@ Description: This is a sample output file
open("output.txt", "w") do f
    xval = JuMP.value.(x)
    for i=1:5
        write(f, "$(xval[i])\n")
    end
end
