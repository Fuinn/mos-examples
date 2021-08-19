#@ Model: Degenerate Codon Design
#@ Description: Adaptation for demonstration purposes from https://github.com/OrensteinLab/DeCoDe

import cvxpy
import numpy as np
import json
from itertools import compress


#@ Input Object: MIP
MIP = True

#@ Input File: D_file
D_file = 'D.npy'
D = np.load(D_file)

#@ Input File: D_hat_file    
D_hat_file = 'D_hat.npy'
D_hat = np.load(D_hat_file)


#@ Input File: s_file
s_file = open('sequences.json', 'r')

#@ Helper Object: sequences
sequences=json.load(s_file)


#@ Helper Object: aa_idx
aa_idx = 'ACDEFGHIKLMNPQRSTVWY*-'


#@ Helper Object: O
O = {i: np.zeros((len(sequences[0]), 22)) for i in range(len(sequences))}
for i in O.keys():
    seq = sequences[i]
    for j, aa in enumerate(seq):
        O[i][j, aa_idx.index(aa)] = 1

O_ = np.zeros((len(sequences),len(sequences[0]) * 22))
for i in O:
    O_[i] = O[i].ravel()

for i in range(len(O)):
    O[i] = O[i].tolist()

# Extract number of codons and number of amino acid options

#@ Helper Object: n_codons
n_codons = D.shape[0]

#@ Helper Object: n_aas
n_aas = D.shape[1]

#@ Helper Object: n_targets
n_targets = len(O)

#@ Helper Object: n_var_pos
n_var_pos = len(O[0])

#@ Helper Object: lib_lim
lib_lim = 6


if MIP == True:
    boolean_switch = True
    nneg_switch = False
else:
    boolean_switch = False
    nneg_switch = True


# Set up variables

#@ Variable: t
#@ Description: description
#@ Labels: targets
t = cvxpy.Variable(n_targets, nonneg=nneg_switch, boolean=boolean_switch)
targets = dict([(i, sequences[i]) for i in range(n_targets)])

#@ Variable: G
#@ Labels: G_labels
G = cvxpy.Variable((n_var_pos, n_codons), nonneg=nneg_switch, boolean=boolean_switch)

G_labels = {}
for i in range(n_var_pos):
    for j in range(n_codons):
        G_labels[(i,j)] = 'pos. {}, codon {}'.format(i, j)


#@ Variable: B
#@ Labels: targets
B = cvxpy.Variable(n_targets, nonneg=nneg_switch, boolean=boolean_switch)

#@ Function: C
#@ Labels: C_labels
C = G * D_hat
C_labels = {}
for i in range(n_var_pos):
    for j in range(len(aa_idx)):
        C_labels[(i,j)] = 'pos. {}, {}'.format(i, aa_idx[j])



#@ Constraint: one_degree_codon
#@ Description: Constrain only one deg. codon can be used
one_degree_codon = cvxpy.sum(G, axis=1) == 1


#@ Function: expression
#@ Labels: targets
expression = (O_ @ cvxpy.vec(C)) - (n_var_pos * np.ones(n_targets)) + (n_var_pos * (1 - B))

#@ Constraint: cover_lb
#@ Description: Constrain "and" for all positions (check for cover of target)
#@ Labels: targets
cover_lb = expression >= 0
#@ Constraint: cover_ub
#@ Description: Constrain "and" for all positions (check for cover of target)
#@ Labels: targets
cover_ub = expression <= n_var_pos


#@ Function: oligo
#@ Description: oligo expression
#@ Labels: targets
oligo = - B + (2 * t)
    
#@ Constraint: oligo_ub    
#@ Description: Constrain "or" for all oligos (check whether target is covered by at least one oligo)
#@ Labels: targets
oligo_ub =  oligo >= 0
#@ Constraint: oligo_lb    
#@ Description: Constrain "or" for all oligos (check whether target is covered by at least one oligo)
#@ Labels: targets
oligo_lb = oligo <= 1


#@ Function: lib_size
lib_size = cvxpy.sum(G * cvxpy.log(cvxpy.sum(D, axis=1)))

#@ Constraint: library
#@ Description: Constrain library size
library = lib_size <= cvxpy.log(lib_lim)
        

#@ Function: objective
#@ Description: Define the objective            
objective = cvxpy.sum(t)

#@ Problem: problem
#@ Description: Maximize covered sequences subject to constraints
constraints = []
constraints.append(one_degree_codon)
constraints.append(cover_ub)
constraints.append(cover_lb)
constraints.append(oligo_ub)
constraints.append(oligo_lb)
constraints.append(library)
#constraints.append(t<=1)
#constraints.append(G<=1)
#constraints.append(B<=1)

problem = cvxpy.Problem(cvxpy.Maximize(objective), constraints)

#@ Solver: solver
#@ Description: Solving the problem
if MIP == True:
    solver = "ECOS_BB"
else:
    solver = "ECOS"

problem.solve(solver=solver, max_iters=1000, verbose=True)


#@ Helper object: solution
# Make all variables available within a dictionary
tvl = t.value.tolist()
solution = {
    'binary_coverage': tvl,
    'covered_sequences': list(compress(sequences,[round(i) for i in tvl])),
    'coverage_count': np.sum(B.value).tolist(),
    'codon_selection': G.value.tolist(),
    'codon_selected': np.max(G.value,axis=1).tolist(),    
}
# last step is to only return indices of G where 1 for each pos, rather than what is returned now    

print(solution)

