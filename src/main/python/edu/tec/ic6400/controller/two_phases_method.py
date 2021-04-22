"""
======================================================================
Copyright (C) 2021 Natan & Diego & Adriel
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    Instituto Tecnologico de Costa Rica
    Investigación de Operaciones - IC-6400
    Simplex Method
    Disponible en: https://github.com/natanfdecastro/simplex-method-ic-6400
    Natan Fernandez de Castro - 2017105774
    Diego Acuña Cerdas - 2018109507
    Adriel Casco Parker - 2016254510
========================================================================
"""

# Standard library imports
import sys


# Third party imports

# Local application imports

# Global variables
extra_solutions = False
flagDeg = False
operation_to_use = ''
txt_generation = ''
objective_function = ''
restriction_matrix = ''
restriction_signs = ''
slack_variables = 0
artificial_variables = 0
number_variables = 0
matrix = []
txt_answer_file = sys.path[1] + '/src/resources/txt_solutions/two_phases/two_phases_answers.txt'
file = ''


'''
    This function clean all de global variables 
'''
def clear():
    global operation_to_use,txt_generation,objective_function,restriction_matrix,restriction_signs,slack_variables,artificial_variables,number_variables,matrix,file
    operation_to_use = ''
    txt_generation = ''
    objective_function = ''
    restriction_matrix = ''
    restriction_signs = ''
    slack_variables = 0
    artificial_variables = 0
    number_variables = 0
    matrix = []
    file = ''


'''
    This function ist the start function, here al global variables set, and starts the process of the two phases method
'''
def two_phases_method(max_min_operation_to_use, txt_generation_is_checked, objective_function_original, restriction_matrix_original, restriction_signs_original):
    global operation_to_use, txt_generation, objective_function, restriction_matrix, restriction_signs, number_variables, file, txt_answer_file
    operation_to_use = max_min_operation_to_use
    txt_generation = txt_generation_is_checked
    objective_function = objective_function_original.tolist()
    restriction_matrix = restriction_matrix_original.tolist()
    restriction_signs = restriction_signs_original
    number_variables = len(restriction_matrix[1])-1
    file = open(txt_answer_file, 'w')

    create_initial_matrix()
    first_phase()
    #print(matrix_to_string())
    simplex_method(1)
    file.close()

    clear()


'''
    This function creates a list of n zeros 
    :parameter-> n= number of zeros to hold the list
'''
def list_zeros_creator(n):
    return [float(0)]*n


'''
    This function starts the first actions to start the simplex method to complete the two phases method
'''
def first_phase():
    global slack_variables, artificial_variables, number_variables, file
    artificial_index = number_variables + slack_variables + 1
    for i in range(artificial_index,len(matrix[1])-1):
        if(matrix[1][i] == -1):
            for j in range(1,len(matrix)):
                if (matrix[j][i]== 1):
                    sum_row(j)
    for i in range(1,len(matrix[1])):
        matrix[1][i] *= -1

    simplex_method(1)
    if matrix[1][-1] == 0:
        #second_phase()
        print('second phase')
    else:
        file.write("No es posible solucionar este problema.")


'''
    This function adds the row in parameter with the objective function to eliminate the artificial variables
    :parameter -> j= index of the row to add
'''
def sum_row(j):
    global matrix
    for i in range(1,len(matrix[1])):
        matrix[1][i] = matrix[1][i] + matrix[j][i]


'''
    This function create a empty matrix to for a the two phases method
'''
def set_empty_matrix():
    global slack_variables, artificial_variables, number_variables, restriction_matrix
    temp = ["VB"]
    set_variables()
    lenght = number_variables + artificial_variables + slack_variables
    count = 1
    while (count < lenght + 1):
        if count > (number_variables + slack_variables):
            temp.append("r" + str(count - (slack_variables + number_variables)))

        elif count > number_variables:
            temp.append("s" + str(count - number_variables))
        else:
            temp.append("x" + str(count))
        count += 1
    temp.append("LD")
    matrix.append(temp)
    len_matrix = len(restriction_matrix)
    for i in range(len_matrix):
        temp = list_zeros_creator(lenght + 2)
        matrix.append(temp)


'''
    This function is to count how many slack and artificial variables
'''
def set_variables():
    global slack_variables, artificial_variables, restriction_signs
    for i in range(0, len(restriction_signs)):
        if restriction_signs[i] == "≤":
            slack_variables += 1
        elif restriction_signs[i] == "≥":
            slack_variables += 1
            artificial_variables += 1
        else:
            artificial_variables += 1


'''
    This function creates the initial matrix to perform the two phases method
'''
def create_initial_matrix():
    set_empty_matrix()
    matrix[1][0] = "U"
    create_new_objetive_function()
    set_variables_to_matrix()


'''
    This function makes the new objective function and adds to the matrix
'''
def create_new_objetive_function():
    global artificial_variables, restriction_matrix
    for i in range(1, len(restriction_matrix[1])):
        if (artificial_variables > 0):
            matrix[1][i] = restriction_matrix[0][i]
            k = 1
            while (k < len(matrix[1]) - 1):
                if (k < number_variables + slack_variables + 1):
                    matrix[1][k] = float(0)
                else:
                    matrix[1][k] = float(-1)
                k += 1
        else:
            matrix[1][i] = -1 * restriction_matrix[0][i]


'''
    This function insert the values of variables in the matrix
'''
def set_variables_to_matrix():
    global restriction_signs, restriction_matrix, matrix,number_variables, slack_variables
    slack_index = number_variables + 1
    artificial_index = number_variables + slack_variables +1
    for i in range(2,len(restriction_matrix)+1):
        if restriction_signs[i-2] == "≤":
            matrix[i][0] = matrix[0][slack_index]
            matrix[i][slack_index] = float(1)
            slack_index += 1
        elif restriction_signs[i-2] == "≥":
            matrix[i][0] = matrix[0][artificial_index]
            matrix[i][slack_index] = float(-1)
            slack_index += 1
            matrix[i][artificial_index] = float(1)
            artificial_index += 1
        elif restriction_signs[i-2] == "=":
            matrix[i][0] = matrix[0][artificial_index]
            matrix[i][artificial_index] = float(1)
            artificial_index += 1

    for i in range(1,len(restriction_matrix)):
        matrix[i + 1][len(matrix[i]) - 1] = restriction_matrix[i][0]
        for j in range(1,len(restriction_matrix[i])):
            matrix[i+1][j] = restriction_matrix[i][j]


'''
    This function reserch in objetive function to verify if exist more than one solution
'''
def check_extra_solution():
    global extra_solutions
    for i in range(number_variables+1,len(matrix[1])):
                   if matrix[1][i] == 0:
                       extra_solutions = True


'''
    This function is for check what collum will be the pivot 
'''
def get_most_negative_variable():
    answer = [None, 0, 0]  # The answer has the form [variable,value,number of column]
    var_amount = len(matrix[0]) - 1  # Gets the amount of variables in the matrix
    i = 1

    # Checks every variable to see which one is the minimun negative
    while i < var_amount:
        if matrix[1][i] <= answer[1] and matrix[1][i] != 0:
            answer = [matrix[0][i], matrix[1][i], i]
        i = i + 1

    return answer


'''
    This function returns a string with the matrix in rows for to print
'''
def matrix_to_string():
    answer = ""
    for line in matrix:
        for word in line:
            word_len = len(str(word))
            if word_len > 6:
                word_len = 6
            answer = answer + ('%.6s' % str(word))
            blank_spaces = 8 - word_len
            answer = answer + (" " * blank_spaces)
        answer = answer + "\n"

    return answer


# -----------------------------------------------Simplex Method------------------------------------------------------- #

def simplex_method(iteration):
    global file
    mnv = determine_minimum_negative_variable()

    # When there is no negative variables, the simplex method ends
    if mnv[0] == None:
        check_extra_solution()
        print_solution()
        return 0

    else:
        restriction = determine_restriction(mnv[2], iteration)
        # When there is no elegible restriction, means that there is no solution with simplex
        if restriction[0] == None:
            file.write("El problema no está acotado" + "\n")
            file.write(str(mnv[0]) + " puede crecer tanto como quiera" + "\n")
        else:
            # Prints the current iteration and graphs the current state of the matrix
            file.write("" + "\n")
            file.write("Iteración " + str(iteration) + "\n")
            file.write("Variable básica que entra: " + mnv[0] + "\n")
            file.write("Variable básica que sale: " + restriction[0] + "\n")
            file.write("Pivote: " + str(matrix[restriction[2]][mnv[2]]) + "\n")

            matrix[restriction[2]][0] = mnv[0]
            row_operations(mnv[2], restriction[2])

            file.write("" + "\n")
            file.write(matrix_to_string() + "\n")

            return simplex_method(iteration + 1)


'''
Function that determines the minimum negative value of a variable of the matrix.
'''
def determine_minimum_negative_variable():
    answer = [None, 0, 0]  # The answer has the form [variable,value,number of column]
    var_amount = len(matrix[0]) - 1  # Gets the amount of variables in the matrix
    i = 1

    # Checks every variable to see which one is the minimun negative
    while i < var_amount:
        if matrix[1][i] <= answer[1] and matrix[1][i] != 0:
            answer = [matrix[0][i], matrix[1][i], i]
        i = i + 1

    return answer


'''
Function that determines the restriction selected according to the minimum negative variable (mnv)
'''
def determine_restriction(mnv, iteration):
    global flagDeg
    divisions = []
    answer = [None, 0, 0]  # The answer has the form [restriction,division with the mnv result,number of row]
    restriction_amount = len(matrix)  # Gets the amount of restrictions in the matrix
    i = 1
    # Checks every restriction to see which one divided by de mnv gives the lowest result
    while i < restriction_amount:
        # Checks that the mnv in this row is bigger than 0 (to avoid division by 0)
        if matrix[i][mnv] > 0 and matrix[i][-1] >= 0:
            division_result = matrix[i][-1] / matrix[i][mnv]
            divisions.append(matrix[i][-1] / matrix[i][mnv])
            # If is the first division, just put it as a partial answer
            if answer[0] == None:
                answer = [matrix[i][0], division_result, i]

            else:
                # Checks if the current division is lower than the current answer
                if division_result < answer[1]:
                    answer = [matrix[i][0], division_result, i]

        i = i + 1
    if divisions != [] and divisions.count(min(divisions)) > 1:
        flagDeg = True
        degenerada = iteration
    return answer


'''
This function is used to apply the necesary operations on the matrix for the current iteration.
'''
def row_operations(mnv, restriction):
    file.write("Operaciones fila realizadas:" + "\n")
    row_amount = len(matrix)
    column_amount = len(matrix[0])
    # Calculates the inverse multiplicative of the mnv value in the choosen restriction in order to multiply them and make sure the result is 1
    inverse_multiplicative = 1 / matrix[restriction][mnv]
    j = 1
    file.write("f" + str(restriction - 1) + " * " + str(inverse_multiplicative) + " -> f" + str(restriction - 1) + "\n")

    # Multiplies the choosen restriction row by the inverse multiplicative
    while j < column_amount:
        matrix[restriction][j] = matrix[restriction][j] * inverse_multiplicative
        j = j + 1

    i = 1

    # Goes trough the matrix, making the mnv column 0 (Except the choosen restriction)
    while i < row_amount:

        if i != restriction:
            j = 1
            multiplier = - matrix[i][mnv]
            if multiplier != 0:
                file.write(
                    str(multiplier) + "f" + str(restriction - 1) + " + f" + str(i - 1) + " -> f" + str(i - 1) + "\n")
            while j < column_amount:
                matrix[i][j] = round(matrix[restriction][j] * multiplier + matrix[i][j], 2)
                j = j + 1

        i = i + 1


'''
Function that prints the final solution of the matrix, it also checks if the answer is degenerate
and does some simple final changes.
'''
def print_solution():
    global file
    if flagDeg:
        file.write("" + "\n")
        file.write("Solución Degenerada" + "\n")
    if extra_solutions:
        file.write("" + "\n")
        file.write("Solución Multiple" + "\n")
    if not extra_solutions and not flagDeg:
        file.write("" + "\n")
        file.write("Solución" + "\n")
    file.write("" + "\n")
    file.write("Valor de las variables:" + "\n")
    answer = {}
    # Finds every variable
    for column in matrix[0]:
        if column[0] == "x" or column[0] == "s" or column[0] == "r":
            answer[column] = 0

    # Finds the value of every value
    for row in matrix[1:]:
        if row[0][0] in ["x", "U", "r", "s"]:
            answer[row[0]] = row[-1]

    if operation_to_use == "min" :
        answer["U"] *= -1
    # Prints every value
    for variable in sorted(answer.keys()):
        file.write(variable + " = " + str(answer[variable]) + "\n")
    # Prints the optimal value of z
    file.write("Por lo tanto el valor óptimo de U es: " + "\n")
    file.write("U = " + str(answer["U"]) + "\n")

'''
def second_phase():
    global slack_variables, number_variables
    i = 0
    while(i < len(matrix)):
        j = 0
        while(j < slack_variables):
            matrix[i].pop(number_variables + slack_variables + 1)
            j += 1
        i += 1

    i = 1
    while(i <= number_variables):
        matrix[1][i] = -1*float(Lines[1][i-1])
        i += 1

    i = 2
    while(i < len(matrix)):
        j = 1
        multiplier = abs(matrix[1][matrix[i].index(1)])
        while(j < len(matrix[1])):
            matrix[1][j] = round(round(matrix[i][j] * multiplier, 2) + matrix[1][j], 2)
            j += 1
        i += 1
    j = 1
    while(j<len(matrix[1])):
        matrix[1][j]*=-1
        j+=1
    #print(matrix_to_string())
    initialize_simplex()
'''