#@ Model: Nurse Rostering Model
#@ Description: Illustrative nurse rostering model. This illustrative model returns a solution if it can find a roster that meets all constraints, returns an error otherwise. Inspired by https://medium.com/@mobini/solving-the-nurse-rostering-problem-using-google-or-tools-755689b877c0. 


using JuMP, Cbc, JSON

#@ Helper Object: num_nurses
num_nurses = 5
#@ Helper Object: num_days
num_days = 7
#@ Helper Object: num_shifts
num_shifts = 2 * num_days



#@ Input Object: max_off
#@ Description: maximum number of consecutive shifts off
max_off = 4



#@ Input File: nurses_shifts_unavailable
#@ Description: list of shifts specific nurses are unavailable for
nurses_shifts_unavailable=open("out.csv","r")

# Process CSV file
nurses_out = zeros(Int,0)
shifts_out = zeros(Int,0)

done = 0;
row = 1;

while done != 1
    line = readline(nurses_shifts_unavailable)
    if row > 1
        if line !=""
            append!(nurses_out, parse.(Int, split(line, ","))[1])
            append!(shifts_out, parse.(Int, split(line, ","))[2])
        else
            global done=1
        end
    end
    global row += 1
end


#@ Helper Object: unavailable
#@ Description: Contents of out.csv
unavailable = Dict{String,String}()
force_off_map = Pair{Int64, Int64}[]
for i=1:row-3
    unavailable[string("nurse ",nurses_out[i])] = string("shift ",shifts_out[i])
    append!(force_off_map,[nurses_out[i] => shifts_out[i]])
end


#@ Solver: solver
solver = Cbc.Optimizer

#@ Problem: model
model = Model(optimizer_with_attributes(solver, "print_level" => 1))

#@ Variable: x
#@ Description: 1 if nurse is working shift, 0 otherwise
@variable(model, x[1:num_nurses,1:num_shifts], Bin)


#@ Constraint: assign
#@ Description: assign one nurse per shift
@constraint(model, assign[j=1:num_shifts],
            sum(x[i,j] for i in 1:num_nurses) == 1)


#@ Constraint: offcalc_min
#@ Description: After a working shift, a nurse is required to have at least two shifts off
@constraint(model, offcalc_min[i=1:num_nurses,j=1:num_shifts-2],
            sum(x[i,jj] for jj in j:j+2) <= 1)

#@ Constraint: offcalc_max
#@ Description: The maximum number of shifts off is set by the max_off input parameter
@constraint(model, offcalc_max[i=1:num_nurses,j=1:num_shifts-max_off],
            sum(x[i,jj] for jj in j:j+max_off) >= 1)

#@ Constraint: force_off
#@ Description: shifts nurses unavailable
@constraint(model, force_off[i=nurses_out,j=shifts_out; (i=>j) in force_off_map],
            x[i,j] == 0)


# Function: objectivefn
# Objective function not relevant in this current formulation of searching for a feasible solution
@expression(model, objectivefn, 0*sum(x[i,j] for i in 1:num_nurses for j in 1:num_shifts))


# Execution: 
@objective(model, Max, objectivefn)
JuMP.optimize!(model)


xval = JuMP.value.(x)

#@ Helper Object: roster
roster = Dict{String,String}()
for j=1:num_shifts
    index = findall(!iszero,xval[:,j])
    println("on shift ",j,", nurse ",index[1], " is rostered")
    roster[string("shift ",j)] = string("nurse ",index[1]) 
end





