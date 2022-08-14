using Test

my_tests = [
    "./examples/cvxpy/portfolio/portfolio_test.jl",
    "./examples/jump/sudoku/sudoku_test.jl",
    "./examples/jump/unit_commitment/unit_commitment_test.jl",
]

println("Running tests:")
@testset "Julia API examples" begin # update julia for verbose=true
    for my_test in my_tests
        println(my_test)
        include(my_test)
    end
end