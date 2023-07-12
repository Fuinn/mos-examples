#@ Model: Sudoku JuMP Model
#@ Description: This is a sample sudoku model

using JuMP, Cbc, Test

#@ Input File: initial_grid_file
#@ Description: Initial grid file
initial_grid_file = open("./examples/jump/sudoku/data.csv", "r")

#@ Helper Object: initial_grid
#@ Description: Initial grid array
initial_grid = zeros(Int, 9, 9)
for row in 1:9
    line = readline(initial_grid_file)
    initial_grid[row, :] .= parse.(Int, split(line, ","))
end

#@ Solver: solver
solver = Cbc.Optimizer
    
#@ Problem: model
model = Model(with_optimizer(solver, print_level=1))

# Labels
xx = Dict()
cell_labels = Dict()
row_labels = Dict()
col_labels = Dict()
ilabels = Dict()
for i in 1:9
    for j in 1:9
        cell_labels[(i,j)] = "row_$(i)_col_$(j)_single_num"
        row_labels[(i,j)] = "row_$(i)_num_$(j)_once"
        col_labels[(i,j)] = "col_$(i)_num_$(j)_once"
        for k in 1:9
            xx[(i,j,k)] = "row_$(i)_col_$(j)_num_$(k)"
        end
        if initial_grid[i, j] != 0
            k = initial_grid[i, j]
            ilabels[(i,j)] = "row_$(i)_col_$(j)_init_num_$(k)"
        end
    end
end

#@ Variable: x
#@ Description: Some variable x
#@ Labels: xx
@variable(model, x[1:9, 1:9, 1:9], Bin)

#@ Constraint: cell
#@ Description: Only one value appears in each cell
#@ Labels: cell_labels
@constraint(model, cell[i in 1:9, j in 1:9], sum(x[i, j, :]) == 1)

#@ Constraint: row
#@ Description: Each value appears in each row once only
#@ Labels: row_labels
@constraint(model, row[i in 1:9, k in 1:9], sum(x[i, :, k]) == 1)

#@ Constraint: col
#@ Description: Each value appears in each column once only
#@ Labels: col_labels
@constraint(model, col[j in 1:9, k in 1:9], sum(x[:, j, k]) == 1)

#@ Constraint: subgrid
#@ Description: Each value appears in each 3x3 subgrid once only
#@ Labels: sg_labels
@constraint(model, subgrid[i=1:3:7, j=1:3:7, val=1:9], sum(x[i:i+2, j:j+2, val]) == 1)

sg_labels = Dict()
for i in 1:3
    for j in 1:3
        for k in 1:9
            sg_labels[(i,j,k)] = "subgrid_$(i)_$(j)_num_$(k)"
        end
    end
end

#@ Constraint: initial
#@ Description: initial solution constraint
#@ Labels: ilabels
@constraint(model, 
            initial[row in 1:9, col in 1:9; initial_grid[row, col] != 0],
            x[row, col, initial_grid[row, col]] == 1)

# Execution:
JuMP.optimize!(model)

#@ Helper Object: solved_grid
#@ Description: Solved grid
values = JuMP.value.(x)
solved_grid = zeros(Int, 9, 9)
for row in 1:9, col in 1:9, val in 1:9
    if values[row, col, val] >= 0.9
        solved_grid[row, col] = val
    end
end

#@ Output File: output.txt
#@ Description: This is a sample output file
open("output.txt", "w") do f
    write(f, "Solution:\n")
    write(f,"[-----------------------]\n")
    for row in 1:9
        write(f, "[ \n")
        for col in 1:9
            write(f, string(solved_grid[row, col]), " ")
            if col % 3 == 0 && col < 9
                write(f, "| \n")
            end
        end
        write(f, "\n]\n")
        if row % 3 == 0
            write(f, "[-----------------------]\n")
        end
    end
end