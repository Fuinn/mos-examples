using Test

# Add Julia API examples to this list
my_tests = [
    "./src/cvxpy/portfolio/portfolio_test.jl",
    "./src/jump/sudoku/sudoku_test.jl",
    "./src/jump/unit_commitment/unit_commitment_test.jl",
    "./src/jump/simple_mip/simple_mip_test.jl",
    "./src/jump/rostering/nurse_rostering_test.jl",        
]

println("Running tests:")
@testset "Julia API examples" begin # update julia version for using verbose=true
    for my_test in my_tests
        println(my_test)
        include(my_test)
    end
end
