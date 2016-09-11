#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
Construct and return sudoku CSP models.
'''

from cspbase import *
import itertools

def sudoku_csp_model_1(initial_sudoku_board):
    '''Return a CSP object representing a sudoku CSP problem along 
       with an array of variables for the problem. That is return

       sudoku_csp, variable_array

       where sudoku_csp is a csp representing sudoku using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the sudokup board (indexed from (0,0) to (8,8))

       
       
       The input board is specified as a list of 9 lists. Each of the
       9 lists represents a row of the board. If a 0 is in the list it
       represents an empty cell. Otherwise if a number between 1--9 is
       in the list then this represents a pre-set board
       position. E.g., the board
    
       -------------------  
       | | |2| |9| | |6| |
       | |4| | | |1| | |8|
       | |7| |4|2| | | |3|
       |5| | | | | |3| | |
       | | |1| |6| |5| | |
       | | |3| | | | | |6|
       |1| | | |5|7| |4| |
       |6| | |9| | | |2| |
       | |2| | |8| |1| | |
       -------------------
       would be represented by the list of lists
       
       [[0,0,2,0,9,0,0,6,0],
       [0,4,0,0,0,1,0,0,8],
       [0,7,0,4,2,0,0,0,3],
       [5,0,0,0,0,0,3,0,0],
       [0,0,1,0,6,0,5,0,0],
       [0,0,3,0,0,0,0,0,6],
       [1,0,0,0,5,7,0,4,0],
       [6,0,0,9,0,0,0,2,0],
       [0,2,0,0,8,0,1,0,0]]
       
       
       This routine returns Model_1 which consists of a variable for
       each cell of the board, with domain equal to {1-9} if the board
       has a 0 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.
       
       Model_1 also contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.), then invoke enforce_gac on those
       constraints. All of the constraints of Model_1 MUST BE binary
       constraints (i.e., constraints whose scope includes two and
       only two variables).
    '''
    result = []
    variable, constraints = creat_c_and_v_M1(initial_sudoku_board)
    simpleCSP = CSP("Soduku_M1", variable)
    
    for c in constraints:
        simpleCSP.add_constraint(c)
    solver = BT(simpleCSP)
        
    solver.unasgn_vars = []
    for v in solver.csp.vars:
        if not v.is_assigned():
            solver.unasgn_vars.append(v)

    status, prunings = prop_GAC(solver.csp)
    if status:
        status = solver.bt_recurse(prop_GAC, 1)   #now do recursive search
    solver.restore_all_variable_domains()
    if status == True:
         i = 0
         k = 0
         while i < 9:
            sub_result = []
            j = 0
            while j < 9:
                sub_result.append(simpleCSP.vars[k])
                k += 1
                j += 1
            result.append(sub_result)
            i += 1
    else:
        print(" it is a DWO!!!!! THERE IS NO SOLUTION!!!")
    
    return simpleCSP, result
    
    
    
    
    
    
    
#IMPLEMENT

##############################

def sudoku_csp_model_2(initial_sudoku_board):
    '''Return a CSP object representing a sudoku CSP problem along 
       with an array of variables for the problem. That is return

       sudoku_csp, variable_array

       where sudoku_csp is a csp representing sudoku using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the sudokup board (indexed from (0,0) to (8,8))

    The input board takes the same input format (a list of 9 lists
    specifying the board as sudoku_csp_model_1.
    
    The variables of model_2 are the same as for model_1: a variable
    for each cell of the board, with domain equal to {1-9} if the
    board has a 0 at that position, and domain equal {i} if the board
    has a fixed number i at that cell.

    However, model_2 has different constraints. In particular, instead
    of binary non-equals constaints model_2 has 27 all-different
    constraints: all-different constraints for the variables in each
    of the 9 rows, 9 columns, and 9 sub-squares. Each of these
    constraints is over 9-variables (some of these variables will have
    a single value in their domain). model_2 should create these
    all-different constraints between the relevant variables, then
    invoke enforce_gac on those constraints.
    '''
    result = []
    variable, constraints = creat_c_and_v(initial_sudoku_board)
    simpleCSP = CSP("Soduku_M2", variable)

    for c in constraints:
        simpleCSP.add_constraint(c)
    

    solver = BT(simpleCSP)
        
    solver.unasgn_vars = []
    for v in solver.csp.vars:
        if not v.is_assigned():
            solver.unasgn_vars.append(v)

    status, prunings = prop_GAC(solver.csp) 
    if status:
        status = solver.bt_recurse(prop_GAC, 1)
    solver.restore_all_variable_domains()
    if status == True:
         i = 0
         k = 0
         while i < 9:
            sub_result = []
            j = 0
            while j < 9:
                sub_result.append(simpleCSP.vars[k])
                k += 1
                j += 1
            result.append(sub_result)
            i += 1
    else:
        print(" it is a DWO!!!!! THERE IS NO SOLUTION!!!")
    
    return simpleCSP, result

#IMPLEMENT


def creat_c_and_v_M1(initial_sudoku_board):
    constraints = []
    variable = []
    i = 0
    while i < 9:
        j = 0
        while j < 9:
            if initial_sudoku_board[i][j] == 0:
                v = Variable('V'+str(i+1)+str(j+1), [1, 2, 3, 4, 5, 6, 7, 8, 9])
                variable.append(v)
            else:
                v = Variable('V'+str(i+1)+str(j+1), [initial_sudoku_board[i][j]])
                variable.append(v)
            j += 1
        i += 1
    
    
    k=0
    index_list = [0,1,2,3,4,5,6,7,8]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)
    
    index_list = [9,10,11,12,13,14,15,16,17]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)
    
    index_list = [18,19,20,21,22,23,24,25,26]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)
    
    index_list = [27,28,29,30,31,32,33,34,35]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)
    
    index_list = [36,37,38,39,40,41,42,43,44]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)
    
    index_list = [45,46,47,48,49,50,51,52,53]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)
    
    index_list = [54,55,56,57,58,59,60,61,62]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)
    
    index_list = [63,64,65,66,67,68,69,70,71]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)
    
    index_list = [72,73,74,75,76,77,78,79,80]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)

    

    index_list = [0,9,18,27,36,45,54,63,72]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)
    
    index_list = [1,10,19,28,37,46,55,64,73]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)
    
    index_list = [2,11,20,29,38,47,56,65,74]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)
    
    index_list = [3,12,21,30,39,48,57,66,75]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)
    
    index_list = [4,13,22,31,40,49,58,67,76]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)
    
    index_list = [5,14,23,32,41,50,59,68,77]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)
    
    index_list = [6,15,24,33,42,51,60,69,78]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)
    
    index_list = [7,16,25,34,43,52,61,70,79]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)
    
    index_list = [8,17,26,35,44,53,62,71,80]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)

    
    
    index_list = [0,1,2,9,10,11,18,19,20]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)
    
    index_list = [3,4,5,12,13,14,21,22,23]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)
    
    index_list = [6,7,8,15,16,17,24,25,26]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)
    
    index_list = [27,28,29,36,37,38,45,46,47]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)
    
    index_list = [30,31,32,39,40,41,48,49,50]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)
    
    index_list = [33,34,35,42,43,44,51,52,53]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)
    
    index_list = [54,55,56,63,64,65,72,73,74]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)
    
    index_list = [57,58,59,66,67,68,75,76,77]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)
    
    index_list = [60,61,62,69,70,71,78,79,80]
    delete_duplicte(index_list,variable)
    get_constraints(index_list,constraints,k,variable)
    
    
    return variable, constraints

def delete_duplicte(index_list,variable):
    for i in index_list:
        for j in index_list:
            if j != i:
                if (len(variable[j].cur_domain())== 1):
                    if variable[j].cur_domain()[0] in variable[i].cur_domain():
                        variable[i].prune_value(variable[j].cur_domain()[0])
            
def get_constraints(index_list,constraints,k,variable):
    for index in range(0,9):
        for index2 in range(index + 1, 9):
            c = Constraint('C'+str(k+1), [variable[index_list[index]], variable[index_list[index2]]])
            delete_duplicate(c)
            c.add_satisfying_tuples(satisfied_tuple_M1(c))
            constraints.append(c)
            k += 1


            
def satisfied_tuple_M1(c):
    s_tuple = []
    vars = c.get_scope()
    for variable1 in vars[0].cur_domain():
        for variable2 in vars[1].cur_domain():
            sub_tuple = [variable1,variable2]
            if check_tuple(sub_tuple):
                s_tuple.append(sub_tuple)
    return s_tuple

def creat_c_and_v(initial_sudoku_board):
    constraints = []
    variable = []
    i = 0
    while i < 9:
        j = 0
        while j < 9:
            if initial_sudoku_board[i][j] == 0:
                v = Variable('V'+str(i+1)+str(j+1), [1, 2, 3, 4, 5, 6, 7, 8, 9])
                variable.append(v)
            else:
                v = Variable('V'+str(i+1)+str(j+1), [initial_sudoku_board[i][j]])
                variable.append(v)
            j += 1
        i += 1
    
    k = 0
    m = 0
    while k < 9:
        c = Constraint('C'+str(k+1), [variable[m], variable[m+1], variable[m+2], variable[m+3], variable[m+4], variable[m+5], variable[m+6], variable[m+7], variable[m+8]])
        delete_duplicate(c)
        constraints.append(c)
        k += 1
        m += 9
    
    m = 0
    while k < 18:
        c = Constraint('C'+str(k+1), [variable[m], variable[m+9], variable[m+18], variable[m+27], variable[m+36], variable[m+45], variable[m+54], variable[m+63], variable[m+72]])
        delete_duplicate(c)
        constraints.append(c)
        k += 1
        m += 1
        
    m = 0
    while k < 21:
        c = Constraint('C'+str(k+1), [variable[m], variable[m+1], variable[m+2], variable[m+9], variable[m+10], variable[m+11], variable[m+18], variable[m+19], variable[m+20]])
        delete_duplicate(c)
        constraints.append(c)
        k += 1
        m += 3
        
    m = 27
    while k < 24:
        c = Constraint('C'+str(k+1), [variable[m], variable[m+1], variable[m+2], variable[m+9], variable[m+10], variable[m+11], variable[m+18], variable[m+19], variable[m+20]])
        delete_duplicate(c)
        constraints.append(c)
        k += 1
        m += 3

    m = 54
    while k < 27:
        c = Constraint('C'+str(k+1), [variable[m], variable[m+1], variable[m+2], variable[m+9], variable[m+10], variable[m+11], variable[m+18], variable[m+19], variable[m+20]])
        delete_duplicate(c)
        constraints.append(c)
        k += 1
        m += 3
    
    for c in constraints:
        c.add_satisfying_tuples(satisfied_tuple(c))

    return variable, constraints


def delete_duplicate(c):
    vals = []
    vars = c.get_scope()
    for var in vars:
        if var.domain_size() == 1:
            vals.append(var.domain())
    for var in vars:
        if var.cur_domain_size() != 1:
            for val in vals:
                if val[0] in var.cur_domain():
                    var.prune_value(val[0])

def satisfied_tuple(c):
    s_tuple = []
    vars = c.get_scope()
    for variable1 in vars[0].cur_domain():
        for variable2 in vars[1].cur_domain():
            if variable1 != variable2:
                for variable3 in vars[2].cur_domain():
                    if variable3 != variable1 and variable3 != variable2:
                        for variable4 in vars[3].cur_domain():
                            if variable4 != variable1 and variable4 != variable2 and variable4 != variable3:
                                for variable5 in vars[4].cur_domain():
                                    if variable5 != variable1 and variable5 != variable2 and variable5 != variable3 and variable5 != variable4:
                                        for variable6 in vars[5].cur_domain():
                                            if variable6 != variable1 and variable6 != variable2 and variable6 != variable3 and variable6 != variable4 and variable6 != variable5:
                                                for variable7 in vars[6].cur_domain():
                                                    if variable7 != variable1 and variable7 != variable2 and variable7 != variable3 and variable7 != variable4 and variable7 != variable5 and variable7 != variable6:
                                                        for variable8 in vars[7].cur_domain():
                                                            if variable8 != variable1 and variable8 != variable2 and variable8 != variable3 and variable8 != variable4 and variable8 != variable5 and variable8!= variable6 and variable8 != variable7:
                                                                for variable9 in vars[8].cur_domain():
                                                                    if variable9 != variable1 and variable9 != variable2 and variable9 != variable3 and variable9 != variable4 and variable9 != variable5 and variable9 != variable6 and variable9 != variable7 and variable9 != variable8:
                                                                        sub_tuple = [variable1,variable2,variable3,variable4,variable5,variable6,variable7,variable8,variable9]
                                                                        if check_tuple(sub_tuple):
                                                                            s_tuple.append(sub_tuple)

    return s_tuple
                                        
def check_tuple(a):
    for sub in a:
        if a.count(sub) > 1:
            return False
    return True
    
    

def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    
    pruned_pairs = []
    queue = []
    if not newVar:
        for c in csp.get_all_cons():
            queue.append(c)
        while queue != []:
            c = queue.pop(0)
            vars = c.get_scope()
            for var in vars:
                for small_value in var.cur_domain():
                    add = False
                    if not c.has_support(var, small_value):
                        pruned_pairs.append((var, small_value))
                        var.prune_value(small_value)
                        add = True
                    if var.cur_domain_size() == 0:
                        return False, pruned_pairs
                    if add:
                        update_list = csp.get_cons_with_var(var)
                        for con in queue:
                            if con in update_list:
                                update_list.remove(con)
                        for small_constraint in update_list:
                            queue.append(small_constraint)
            
        return True, pruned_pairs

    else:
        queue =  csp.get_cons_with_var(newVar)
        num = 0
        while queue != []:
            c = queue.pop(0)
            vars = c.get_scope()
            for var in vars:
                for small_value in var.cur_domain():
                    add = False
                    if not c.has_support(var, small_value):
                        pruned_pairs.append((var, small_value))
                        var.prune_value(small_value)
                        add = True
                    if var.cur_domain_size() == 0:
                        return False, pruned_pairs
                    if add:
                        update_list = csp.get_cons_with_var(var)
                        for con in queue:
                            if con in update_list:
                                update_list.remove(con)
                        for small_constraint in update_list:
                            queue.append(small_constraint)
            
        return True, pruned_pairs

