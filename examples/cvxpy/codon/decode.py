#@ Model: Degenerate Codon Design
#@ Description: Adaptation for demonstration purposes from https://github.com/OrensteinLab/DeCoDe

import cvxpy
import numpy as np

#@ Input File: D_file
D_file = 'D.npy'
D = np.load(D_file)

#@ Input File: D_hat_file    
D_hat_file = 'D_hat.npy'
D_hat = np.load(D_hat_file)

#@ Input File: O_file
O_file = 'O.npy'
O = np.load(O_file)

#@ Input File: s_file
s_file = 'sequences.json'

#@ Helper Object: sequences
sequences = json.load(s_file)

#@ Helper Object: aa_idx
aa_idx = 'ACDEFGHIKLMNPQRSTVWY*-'


#@ Helper Object: O
O = {i: np.zeros((len(sequences[0]), 22)) for i in range(len(sequences))}
for i in O.keys():
    seq = sequences[i]
    for j, aa in enumerate(seq):
        O[i][j, aa_idx.index(aa)] = 1


#def solve_library(O, lib_lim, n_templates, bins=1e3, verbose=True, parallel=True, approximate=False, time_limit=0, threads=0):
    ####################
    # i = n_targets    #
    # s = n_templates  #
    # p = n_var_pos    #
    # a = n_aas        #
    ####################
    
# Extract number of codons and number of amino acid options
#@ Helper Object: n_codons
n_codons = D.shape[0]

#@ Helper Object: n_aas
n_aas = D.shape[1]

#@ Helper Object: n_targets
n_targets = len(O)

#@ Helper Object: n_var_pos
n_var_pos = len(O[0])

#    n_targets = len(sequences)
#    n_var_pos = len(sequences[0])


# Set up variables

#@ Variable: t
t = cvxpy.Variable(n_targets, boolean=True)

#@ Variable: G
G = cvxpy.Variable((n_var_pos, n_codons), boolean=True)

#@ Variable: B
B = cvxpy.Variable((n_targets), boolean=True)

#@ Function: C
#@ Description: Define relationship between C, G, and D
# D_hat 841x22, G 5 * 841
C = G * D_hat

#@ Constraint: one_degree_codon
#@ Description: Constrain only one deg. codon can be used
one_degree_codon = cvxpy.sum(G, axis=1) == 1

#### JM July 2021 this is 3d and this cvxpy way of expressing 3d variable does not really fit in with MOS yet
# we can just assume dim=1, as in default example
    
# so somehow we want 6*5*22 matrix multiplied by 5*22 matrix to return 6 by 1 vector        
# could O be comressed into a 6*5 or 6*22 thing?
# or just create multiple constraints as a quick fix

# Constrain "and" for all positions (check for cover of target)
# Need to vectorize this
for i in range(n_targets):
    expression = cvxpy.sum(cvxpy.multiply(O[i], C)) - n_var_pos + n_var_pos * (1 - B[i])
    constraints.append(expression >= 0)
    constraints.append(expression <= n_var_pos)


#@ Function: oligo
#@ Description: oligo expression
oligo = - cvxpy.sum(B, axis=1) + (n_templates + 1) * t 
    
#@ Constraint: oligo_ub    
#@ Description: Constrain "or" for all oligos (check whether target is covered by at least one oligo)
oligo_ub =  oligo >= 0
#@ Constraint: oligo_lb    
#@ Description: Constrain "or" for all oligos (check whether target is covered by at least one oligo)
oligo_lb = oligo <= n_templates


# Constrain library size for a single oligo
#if n_templates == 1 and not approximate:


#@ Function: lib_size
lib_size = cvxpy.sum(G[0] * cvxpy.log(cvxpy.sum(D, axis=1)))

#@ Constraint: library
#@ Description: Constrain library size
library = lib_size <= cvxpy.log(lib_lim)
        

# Define the objective            
objective = cvxpy.sum(t)

#@ Problem: problem
#@ Description: Maximize covered sequences subject to constraints
constraints = []
constraints.append(one_degree_codon)
# tricky constraints here
constraints.append(oligo_ub)
constraints.append(oligo_lb)
constraints.append(library)

problem = cvxpy.Problem(cvxpy.Maximize(objective), constraints)

#@ Solver: solver
#@ Description: Solving the problem
solver = "ECOS"

problem.solve(solver=solver, verbose=True)


#@ Helper Object: solution
#@ Description: Make all variables available within a dictionary
solution = {
    'binary_coverage': t.value,
    'coverage_count': np.sum(B.value, axis=1),
    'codon_selection': np.stack([G[x].value for x in G]),
    'problem': problem
}
    



