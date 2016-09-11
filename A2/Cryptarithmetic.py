#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
Construct and return sudoku CSP models.
'''

from cspbase import *
from itertools import product

def puzzle(initial_sudoku_board):

    result = []
    variable, constraints = creat_c_and_v(initial_sudoku_board)
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
        

            
    for v in variable:
        if v.name != "0":
            print(v.name + ": " + str(v.cur_domain()[0])) 
       
    
    
    


#IMPLEMENT


def creat_c_and_v(equation):
    constraints = []
    variable = []
    if equation[3] == "+" or equation[3] == "*":
        length_max = len(equation[2])
     
        length_1 = len(equation[0])
        length_2 = len(equation[1])
        first = equation[0]
        second = equation[1]
        result = equation[2]
        diff = length_max - length_1
        i = 0
        while (i < diff):
            first.insert(0,0)
            i += 1

        diff = length_max - length_2
        i = 0
        while (i < diff):
            second.insert(0,0)
            i += 1
        equation = [first,second,result,equation[3]]
        
    if equation[3] == "-" or equation[3] == "/":
        length_max = len(equation[0])
     
        length_1 = len(equation[1])
        length_2 = len(equation[2])
        first = equation[0]
        second = equation[1]
        result = equation[2]
        diff = length_max - length_1
        i = 0
        while (i < diff):
            second.insert(0,0)
            i += 1

        diff = length_max - length_2
        i = 0
        while (i < diff):
            result.insert(0,0)
            i += 1
        equation = [first,second,result,equation[3]]
    
    i = 0
    add = False
    case = []
    while i < 3:
        j = 0
        while j < length_max:
            if equation[i][j] != 0:
                if (j - 1) >= 0:
                    if equation[i][j-1] == 0:
                        v = Variable(str(equation[i][j]), [1, 2, 3, 4, 5, 6, 7, 8, 9])
                        if equation[i][j] not in case:
                            variable.append(v)
                            case.append(equation[i][j])
                        
                    else:
                        v = Variable(str(equation[i][j]), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
                        if equation[i][j] not in case:
                            variable.append(v)
                            case.append(equation[i][j])
                else:
                    v = Variable(str(equation[i][j]), [1, 2, 3, 4, 5, 6, 7, 8, 9])
                    if equation[3] == '+':
                        if i == 2 and length_1 < length_max and length_2 < length_max:
                            v = Variable(str(equation[i][j]), [1])
                    if equation[i][j] not in case:
                            variable.append(v)
                            case.append(equation[i][j])
            else:
                if add == False:
                    v = Variable('0', [0])
                    variable.append(v)
                    add = True
            j += 1
        i += 1
    z = 0
    while z < 3:
        index_list = []
        for a in equation[z]:
            for k in variable:
                if k.name == str(a):
                    index_list.append(variable.index(k))
                    break
        constraint_list = []
        for b in index_list:
            constraint_list.append(variable[b])
        c = Constraint('C'+str(z), constraint_list)
        duplicate = []
        for e in range(0,len(constraint_list)):
            for d in range(e+1,len(constraint_list)):
                if constraint_list[e] == constraint_list[d]:
                    duplicate.append([e,d])

        input_string = "product("
        for i in range(0, len(constraint_list)):
            new_value = []
            for v in constraint_list[i].domain():
                new_value.append(v)
            
            input_string += str(new_value)

            if i != (len(constraint_list) - 1):
               input_string += ", "
        input_string += ")"
        new_values_list = []
        for p in eval(input_string):
            p = list(p)
            new_values_list.append(p)
        remove_list = []
        if duplicate != []:
            for t in duplicate:
                for p in new_values_list:
                    if p[t[0]] != p[t[1]]:
                        index_remove = new_values_list.index(p)
                        if index_remove not in remove_list:
                            remove_list.append(index_remove)
            remove_list.sort()
            remove_list.reverse()
            for r in remove_list:
                new_values_list.pop(r)

        
        remove_list = []
        d_index = []
        for dd in duplicate:
            d_index.append(dd[0])
        
        for p in new_values_list:
            for pp in p:
                if p.index(pp) not in d_index:
                    if p.count(pp) > 1:
                        remove_list.append(new_values_list.index(p))
                        break
        
        remove_list.sort()
        remove_list.reverse()
        for r in remove_list:
            new_values_list.pop(r)
                              
        
        if z == 0:
            first_result = new_values_list
        if z == 1:
            second_result = new_values_list
        if z == 2:
            final_result = new_values_list
        c.add_satisfying_tuples(new_values_list)
        
        constraints.append(c)
        
        z += 1
        



    
    
    z = 0
    constraint_list = []
    index_list = []
    while z < 3:
        for a in equation[z]:
            for k in variable:
                if k.name == str(a):
                    index_list.append(variable.index(k))
                    break
        constraint_list = []
        for b in index_list:
            constraint_list.append(variable[b])
        z = z + 1
    c = Constraint('C'+str(3), constraint_list)

    duplicate = []
    for e in range(0,len(constraint_list)):
        for d in range(e+1,len(constraint_list)):
            if constraint_list[e] == constraint_list[d]:
                duplicate.append([e,d])


    
    final_result_int = []
    for fr in final_result:
        fr_number = ''
        for ffr in fr:
            fr_number += str(ffr)
        fr_number  = int(fr_number)
        final_result_int.append(fr_number)

    satisfied_tuple = []


    constraint_list2 = []
    z = 0
    while z < 3:
        for a in equation[z]:
            for k in variable:
                if k.name == str(a):
                    constraint_list2.append(k)
        z += 1
    
    if equation[3] == "+":
        for f in first_result:
            f_number = ''
            for ff in f:
                f_number += str(ff)
            f_number  = int(f_number)
            for s in second_result:
                s_number = ''
                for ss in s:
                    s_number += str(ss)
                s_number  = int(s_number)
                if (f_number + s_number) in final_result_int:
                    sub = []
                    for fn in f:
                        sub.append(fn)
                    for sn in s:
                        sub.append(sn)
                    for frn in final_result[final_result_int.index(f_number + s_number)]:
                        sub.append(frn)
                    append = True
                    
                    check_list = f + s + final_result[final_result_int.index(f_number + s_number)]
                    count = 0
                    for sub_variable in constraint_list2:
                        if sub_variable.name == '0':
                            count += 1

                    for sub_variable in constraint_list2: 
                        if sub_variable.name != '0':
                            if check_list[constraint_list2.index(sub_variable)] == 0:
                                if check_list.count(check_list[constraint_list2.index(sub_variable)]) != (constraint_list2.count(sub_variable) + count):
                                    append = False
                                    break
                            else:
                                if check_list.count(check_list[constraint_list2.index(sub_variable)]) != constraint_list2.count(sub_variable ):
                                    
                                    append = False
                                    

                    if append:
                        satisfied_tuple.append(sub)
    
    if equation[3] == "*":
        for f in first_result:
            f_number = ''
            for ff in f:
                f_number += str(ff)
            f_number  = int(f_number)
            for s in second_result:
                s_number = ''
                for ss in s:
                    s_number += str(ss)
                s_number  = int(s_number)
                if (f_number * s_number) in final_result_int:
                    sub = []
                    for fn in f:
                        sub.append(fn)
                    for sn in s:
                        sub.append(sn)
                    for frn in final_result[final_result_int.index(f_number * s_number)]:
                        sub.append(frn)
                    append = True
                    
                    check_list = f + s + final_result[final_result_int.index(f_number * s_number)]
                    count = 0
                    for sub_variable in constraint_list2:
                        if sub_variable.name == '0':
                            count += 1

                    for sub_variable in constraint_list2: 
                        if sub_variable.name != '0':
                            if check_list[constraint_list2.index(sub_variable)] == 0:
                                if check_list.count(check_list[constraint_list2.index(sub_variable)]) != (constraint_list2.count(sub_variable) + count):
                                    append = False
                                    break
                            else:
                                if check_list.count(check_list[constraint_list2.index(sub_variable)]) != constraint_list2.count(sub_variable ):
                                    
                                    append = False
                                    

                    if append:
                        satisfied_tuple.append(sub)
        
    if equation[3] == "-":
        for f in first_result:
            f_number = ''
            for ff in f:
                f_number += str(ff)
            f_number  = int(f_number)
            for s in second_result:
                s_number = ''
                for ss in s:
                    s_number += str(ss)
                s_number  = int(s_number)
                if (f_number - s_number) in final_result_int:
                    sub = []
                    for fn in f:
                        sub.append(fn)
                    for sn in s:
                        sub.append(sn)
                    for frn in final_result[final_result_int.index(f_number - s_number)]:
                        sub.append(frn)
                    append = True
                    
                    check_list = f + s + final_result[final_result_int.index(f_number - s_number)]
                    count = 0
                    for sub_variable in constraint_list2:
                        if sub_variable.name == '0':
                            count += 1

                    for sub_variable in constraint_list2: 
                        if sub_variable.name != '0':
                            if check_list[constraint_list2.index(sub_variable)] == 0:
                                if check_list.count(check_list[constraint_list2.index(sub_variable)]) != (constraint_list2.count(sub_variable) + count):
                                    append = False
                                    break
                            else:
                                if check_list.count(check_list[constraint_list2.index(sub_variable)]) != constraint_list2.count(sub_variable ):
                                    
                                    append = False
                                    

                    if append:
                        satisfied_tuple.append(sub)

    if equation[3] == "/":
        for f in first_result:
            f_number = ''
            for ff in f:
                f_number += str(ff)
            f_number  = int(f_number)
            for s in second_result:
                s_number = ''
                for ss in s:
                    s_number += str(ss)
                s_number  = int(s_number)
                if (f_number / s_number) in final_result_int:
                    sub = []
                    for fn in f:
                        sub.append(fn)
                    for sn in s:
                        sub.append(sn)
                    for frn in final_result[final_result_int.index(f_number / s_number)]:
                        sub.append(frn)
                    append = True
                    
                    check_list = f + s + final_result[final_result_int.index(f_number / s_number)]
                    count = 0
                    for sub_variable in constraint_list2:
                        if sub_variable.name == '0':
                            count += 1

                    for sub_variable in constraint_list2: 
                        if sub_variable.name != '0':
                            if check_list[constraint_list2.index(sub_variable)] == 0:
                                if check_list.count(check_list[constraint_list2.index(sub_variable)]) != (constraint_list2.count(sub_variable) + count):
                                    append = False
                                    break
                            else:
                                if check_list.count(check_list[constraint_list2.index(sub_variable)]) != constraint_list2.count(sub_variable ):
                                    
                                    append = False
                                    

                    if append:
                        satisfied_tuple.append(sub) 
                    
    
                   
    c.add_satisfying_tuples(satisfied_tuple)
    constraints.append(c)
    


   
                    
    return variable, constraints
    


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



if __name__=="__main__":
    print("a + bb = acc")
    print("solution:")
    puzzle([['a'],['b','b'],['a','c','c'],'+'])
    print("")
    print("")

    
    print("ab + cbd = ccb")
    print("solution:")
    puzzle([['a','b'],['c','b','d'],['c','c','b'],'+'])
    print("")
    print("")
    

    print("abc + cab = dac")
    print("solution:")
    puzzle([['a','b','c'],['c','a','b'],['d','a','c'],'+'])
    print("")
    print("")
    

    print("ab + ccb = adde")
    print("solution:")
    puzzle([['a','b'],['c','c','b'],['a','d','d','e'],'+'])
    print("")
    print("")

    
    print("ab * bc = dcb")
    print("solution:")
    puzzle([['a','b'],['b','c'],['d','c','b'],'*'])
    print("")
    print("")


    print("abc * cc = adac")
    print("solution:")
    puzzle([['a','b','c'],['c','c'],['a','d','a','c'],'*'])
    print("")
    print("")


    print("abb - a = cc")
    print("solution:")
    puzzle([['a','b','b'],['a'],['c','c'],'-'])
    print("")
    print("")


    print("abcd - cdb = efb")
    print("solution:")
    puzzle([['a','b','c','d'],['c','d','b'],['e','f','b'],'-'])
    print("")
    print("")


    print("aba / aa = aa")
    print("solution:")
    puzzle([['a','b','a'],['a','a'],['a','a'],'/'])
    print("")
    print("")


    print("abcd / eae = ad")
    print("solution:")
    puzzle([['a','b','c','d'],['e','a','e'],['a','d'],'/'])
    print("")
    print("")
    
