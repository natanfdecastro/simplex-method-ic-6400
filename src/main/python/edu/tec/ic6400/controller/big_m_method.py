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

# Third party imports
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QVBoxLayout,
    QWidget,
)
import math, copy
# Local application imports
from src.main.python.edu.tec.ic6400.view.simplex_program_gui import *
from src.main.python.edu.tec.ic6400.model.txt_method_writer import *



error=""
variable=""
def big_m_method(constraints, equals,objective,symbol,operation,flag,var):
    global error
    error=""
    print(constraints,equals,objective,symbol,operation,flag,var)
    writer_big_m_method(True, "")
    global variable
    variable=var
    writer_big_m_method(True, "")
    M = 100
    (matrix, variables, basic, pos) = table(constraints, equals, objective, symbol, operation, M)  # M al final
    matrix_with_pivot_base = pivot_base(matrix, pos)
    if flag:
        print_problem(constraints, equals, objective, symbol, operation)
        writer_big_m_method(False, "\nInitial table")
        writer_big_m_method(False,2)
        print_table(matrix, basic, variables)
    if flag:
        writer_big_m_method(False,"\nTabla con variables M")
        writer_big_m_method(False, 2)
        print_table(matrix_with_pivot_base, basic, variables)
        writer_big_m_method(False, "\nBasic variables =")
        writer_big_m_method(False,basic)

        writer_big_m_method(False, "\nIndex of basic variables =")
        writer_big_m_method(False, str(pos))
        writer_big_m_method(False, "\n\n\n ---Simplex Method---")
        writer_big_m_method(False, 2)
    for k in range(0, 10):
        index = index_pivot(matrix_with_pivot_base, basic, variables)
        if index[0] > -1 and index[1] > -1:
            matrix_with_pivot_base = pivot(matrix_with_pivot_base, index)
            basic[index[0] - 1] = variables[index[1] - 1]
            if flag:
                writer_big_m_method(False, "\n Step: " + str(k + 1) + ": pivot found in index=" + str(index))
                writer_big_m_method(False,2)
                print_table(matrix_with_pivot_base, basic, variables)
    if check_error(matrix_with_pivot_base, M, variables,flag) == "":
        if flag:
            writer_big_m_method(False,"\n Solution:")
            writer_big_m_method(False,2)

        return results(matrix_with_pivot_base, basic, len(objective), pos, operation,flag)
    else:
        writer_big_m_method(False,2)
        if flag:
            print_table(matrix_with_pivot_base, basic, variables)
        else:
            pass
        return error


def print_problem(constraints, equals, objective, ine, prob):

    copy_constraints = copy.deepcopy(constraints)
    copy_equals = copy.deepcopy(equals)
    copy_objective = copy.deepcopy(objective)
    n = len(objective)
    m = len(equals)
    # Objective Function
    writer_big_m_method(False, prob + ' ')
    for i in range(n):
        t = objective[i]
        if i > 0:
            if t < 0:
                t = -1 * t
                writer_big_m_method(False, ' - ')
            else:
                writer_big_m_method(False, ' + ')
        elif t == -1:
            t = -1 * t
            writer_big_m_method(False, '-')
        if t == 1:
            writer_big_m_method(False, f'x{i + 1}')
        else:
            writer_big_m_method(False, f'{t}x{i + 1}')

    # restrictions
    writer_big_m_method(False, "\n" + ' subject to:')
    for i in range(m):
        writer_big_m_method(False, '\n  ')

        for j in range(n):
            t = constraints[i][j]
            if t == 0:
                writer_big_m_method(False,'   ')

            else:
                if j > 0:
                    if t < 0:
                        t = -1 * t
                        writer_big_m_method(False, ' - ')

                    else:
                        writer_big_m_method(False, ' + ')

                elif t == -1:
                    t = -1 * t
                    writer_big_m_method(False, '-')
                if t == 1:
                    writer_big_m_method(False, f'x{j + 1}')

                else:
                    writer_big_m_method(False, f'x{j + 1}')

        if ine[i] == 1:
            writer_big_m_method(False, ' \u2265 ' + str(copy_equals[i]) + ' ')
        elif ine[i] == -1:
            writer_big_m_method(False, ' \u2264 ' + str(copy_equals[i]) + ' ')

        elif ine[i] == 0:
            writer_big_m_method(False,' = ' + str(copy_equals[i]))

    # variables >= 0
    writer_big_m_method(False, '\n  ')
    for i in range(n):
        writer_big_m_method(False, f'x{i + 1}')
        if i < n - 1:
            writer_big_m_method(False, ',')

    writer_big_m_method(False, ' \u2265 0\n')
    writer_big_m_method(False, 2)


def check_error(matrix_with_pivot_base, M, var,flag):
    global error
    n = len(matrix_with_pivot_base[0]) - 1
    m = len(matrix_with_pivot_base) - 1
    funb = 0
    finf = 0
    for j in range(n):
        #  checked only between slack variables
        if var[j][0:1] == 's' and matrix_with_pivot_base[m][j] > 0:
            var_error = (var[j][0:2])
            funb = 1
        elif var[j][0:1] == 's' and matrix_with_pivot_base[m][j] <= -M:
            var_error = (var[j][0:2])
            finf = 1
    if funb:
        error=("\n Error: The problem is not limited.\n      It grows indifinitely in the direction of the variable: " + var_error + ".")
        if flag:
            """
            f.writelines(
            "\n Error: The problem is not limited.\n      It grows indifinitely in the direction of the variable" + var_error + ".")
            """
            writer_big_m_method(False, "\n Error: The problem is not limited.\n      It grows indifinitely in the direction of the variable" + var_error + ".")
    if finf:
        error=('\n Error: The iterations have completed and there are artificial variables in the base with values strictly greater than 0,\n '
            'so the problem has no solution (infeasible).')
        if flag:
            """
            f.writelines(
                '\n Error: The iterations have completed and there are artificial variables in the base with values strictly greater than 0,\n '
                'so the problem has no solution (infeasible).'
            )
            """
            writer_big_m_method(False,
                                '\n Error: The iterations have completed and there are artificial variables in the base with values strictly greater than 0,\n '
                                'so the problem has no solution (infeasible).'
                                )
    return error


# build the table of the data.
def table(constraints, equals, objective, symbol, operation, M):
    copy_constraints = copy.deepcopy(constraints)
    copy_equals = copy.deepcopy(equals)
    copy_objective = copy.deepcopy(objective)
    copy_symbol = copy.deepcopy(symbol)
    copy_operation = copy.deepcopy(operation)

    # list of variables
    variables = []
    base = []
    posbase = []
    len_objetive = len(copy_objective)
    len_constraints = len(copy_constraints)


    for j in range(len_objetive):
        variables.append(f"x{j + 1}")
    c = [x * -1 for x in copy_objective]  # for minimization
    if copy_operation == 'max':
        c = copy.deepcopy(objective)
    copy_constraints.append(c)  # add at the end
    copy_equals.append(0)
    zero = [0.0] * len(copy_equals)
    naux = 0
    nslack = 0  # slack variables

    # table construction
    for i in range(0, len(copy_symbol)):
        copy_constraints = append_col(copy_constraints, zero)
        if copy_symbol[i] == 1:
            copy_constraints[i][len_objetive + nslack + naux] = -1
            variables.append(f"s{nslack + 1}")
            nslack += 1
            # bigM aux
            copy_constraints = append_col(copy_constraints, zero)
            copy_constraints[i][len_objetive + nslack + naux] = 1
            variables.append(f"a{naux + 1}")
            base.append(f"a{naux + 1}")
            copy_constraints[len_constraints][len_objetive + nslack + naux] = -M
            naux += 1
        elif copy_symbol[i] == 0:
            copy_constraints[i][len_objetive + nslack + naux] = 1
            variables.append(f"a{naux + 1}")
            base.append(f"a{naux + 1}")
            copy_constraints[len_constraints][len_objetive + nslack + naux] = -M
            naux += 1
        elif copy_symbol[i] == -1:
            variables.append(f"s{nslack + 1}")
            base.append(f"s{nslack + 1}")
            copy_constraints[i][len_objetive + nslack + naux] = 1
            nslack += 1
        posbase.append(len_objetive + nslack + naux)
    return (append_col(copy_constraints, copy_equals), variables, base, posbase)


def pivot(A, pivot_index):  # pivota un index+1 en una matriz A
    # Perform operations on pivot.

    T = copy.deepcopy(A)
    i, j = pivot_index[0] - 1, pivot_index[1] - 1
    pivot = T[i][j]
    T[i] = [element / pivot for
            element in T[i]]
    for index, row in enumerate(T):
        if index != i:
            row_scale = [y * T[index][j]
                         for y in T[i]]
            T[index] = [x - y for x, y in
                        zip(T[index],
                            row_scale)]
    return T


#    consecutive pivots based on column vector
def pivot_base(matrix, pos):
    copy_matrix = copy.deepcopy(matrix)
    copy_pos = copy.deepcopy(pos)
    for k in range(0, len(copy_pos)):
        copy_matrix = pivot(copy_matrix, [k + 1, copy_pos[k]])
    return copy_matrix


# simplex column evaluation returns indexj
def pivot_j_index(last_position_matrix_pivot, vari):
    copy_last_position_matrix_pivot = copy.deepcopy(last_position_matrix_pivot)
    vmax = -1
    jmax = -2
    for j in range(0, len(copy_last_position_matrix_pivot) - 1):
        temp = copy_last_position_matrix_pivot[j]
        if vari[j][0:1] != 'x':
            temp = temp - 0.00009
        if temp > 0 and temp > vmax:
            vmax = copy_last_position_matrix_pivot[j]
            jmax = j
    return jmax


# simplex row evaluation returns indexi
def pivote_i_index(vector_2, vector_1, basi):
    copy_vector_2 = copy.deepcopy(vector_2)
    copy_vector_1 = copy.deepcopy(vector_1)
    vmin = 999999999.99
    imin = -2
    temp = vmin
    for i in range(0, len(vector_1) - 1):
        if copy_vector_2[i] != 0:
            temp = copy_vector_1[i] / copy_vector_2[i]
        if basi[i][0:1] == 's':
            temp = temp - 0.009
        if copy_vector_2[i] != 0 and temp > 0 and temp < vmin:
            vmin = temp
            imin = i
    return imin


# get the pivot position in the matrix
def index_pivot(matrix_pivot, basi, vari):
    copy_matrix_pivot = copy.deepcopy(matrix_pivot)
    indexj = pivot_j_index(copy_matrix_pivot[len(copy_matrix_pivot) - 1], vari) + 1
    vector_1 = v_col(copy_matrix_pivot, len(copy_matrix_pivot[0]))
    vector_2 = v_col(copy_matrix_pivot, indexj)
    indexi = pivote_i_index(vector_2, vector_1, basi) + 1
    return [indexi, indexj]


# auxiliary tools

# add the vector (column) to matrix List
def append_col(list, vector):  # añade el vector vc (columna) a matriz T
    copy_list = copy.deepcopy(list)
    copy_vector = copy.deepcopy(vector)
    for i in range(0, len(copy_list)):
        copy_list[i] += [copy_vector[i]]  # add to the end of the sum
    return copy_list

# Gets a vector from matrix
def v_col(matrix, column):
    copy_len = copy.deepcopy(column)
    copy_len -= 1
    v = []
    for i in range(0, len(matrix)):
        v.append(matrix[i][copy_len])
    return v


# Print the table to the text file
def print_table(matrix, basic, variables):  # Muestra tableu
    global variable
    copy_matrix = copy.deepcopy(matrix)
    copy_variables = copy.deepcopy(variables)
    copy_basic = copy.deepcopy(basic)
    copy_basic.append(variable+' ')

    writer_big_m_method(False,'\n       ')

    for i in copy_variables:
        writer_big_m_method(False,
                            '{0:7}'.format(i)
                            )

    writer_big_m_method(False,'\n')
    for k in range(0, len(copy_matrix)):
        writer_big_m_method(False, copy_basic[k])
        for j in range(0, len(copy_matrix[k])):
            val = round_up(copy_matrix[k][j])
            writer_big_m_method(False, '{0:7.1f}'.format(val))
        writer_big_m_method(False, '\n')
    writer_big_m_method(False,2)

def round_up(x):
    x = math.ceil(x * 10000) / 10000
    return x


#Shows the final results
def results(matrix_with_pivot_base, bas, n, pos, pr,flag):
    global variable
    res="\n " +"Solution"
    variables = []
    valor = []
    m = len(bas)  # number of constraints or basic variables
    mA = len(matrix_with_pivot_base[0]) - 1
    for k in range(n):  # for all x
        variables.append(f"x{k + 1}")
        valor.append(0)
        for i in range(m):  # for all basic variables
            if variables[k] == bas[i]:
                valor[k] = matrix_with_pivot_base[i][mA]
        if flag:
            writer_big_m_method(False, "\n " + variables[k] + " " + str(valor[k]))
        res+=("\n "+ variables[k] + " " + str(valor[k]))
    if flag:
        writer_big_m_method(False, "\n " + variable+" = " + str(round_up(matrix_with_pivot_base[m][mA]) * (-1 if pr == 'max' else 1)))
    res += ("\n " + variable+" = " + str(round_up(matrix_with_pivot_base[m][mA]) * (-1 if pr == 'max' else 1)))
    writer_big_m_method(False,2)
    return res