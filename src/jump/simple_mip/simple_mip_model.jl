#@ Model: Simple MIP JuMP Model
#@ Description: Implementation of MIP from https://jump.dev/JuMP.jl/dev/tutorials/applications/web_app/ $$\min 0$$$$x \geq \text{lower_bound}$$$$x\in \mathbb{Z}$$

using JuMP, Cbc, JSON, Test

#@ Input Object: lower_bound
#@ Description: Lower bound of variable
lower_bound = 1.2


#@ Solver: solver
solver = Cbc.Optimizer

#@ Problem: model
model = Model(with_optimizer(solver))

#@ Variable: x
#@ Description: Some variable x
@variable(model, x >= lower_bound, Int)


# Execution:
optimize!(model)

println("Value of x is:")
println(value(x))
