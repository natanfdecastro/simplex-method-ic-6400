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
    You should have received restriction_matrix copy of the GNU General Public License
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
import numpy as np

# Third party imports

# Local application imports
from src.main.python.edu.tec.ic6400.model.txt_method_writer import *


class DualMethod:
    """
    Class that is in charge of defining the attributes and methods related to
    the resolution of the dual method
    Inputs: None
    Outputs: None
    Restrictions: None
    """
    def __init__(self, objective_function, restriction_matrix, restriction_results, max_min_operation_to_use,
                 restriction_signs):
        """
        Constructor for class that is in charge of the initialization of the new object
        of Dual Method type
        Inputs:
            - objective_function
            - restriction_matrix
            - restriction_results
            - max_min_operation_to_use: Contains the type of operation to use. Could be max or min
            - restriction_signs: numpy array that contains the signs of the constraints. Ex: [<=, >=, =]
        Outputs: None
        Restrictions: None
        """

        # Info of the operation data
        # number of variables
        self.function_variables_len = restriction_matrix.shape[1]
        # number of restrictions
        self.constraints_len = restriction_matrix.shape[0]
        # number of variables and restrictions
        self.variables_len = self.function_variables_len + self.constraints_len
        # Minization or maximization
        self.max_min_operation_to_use = max_min_operation_to_use
        self.restriction_signs = restriction_signs
        self.have_solution = True

        # function coefficients
        self.function_coefficients = np.concatenate([objective_function, np.zeros((self.constraints_len + 1))])
        # values of function W
        self.w_function_values = np.zeros((self.variables_len + 1))
        self.variables_index = [i + self.function_variables_len for i in range(self.constraints_len)]

        self.table = np.zeros((self.constraints_len, self.variables_len + 1))

        self.create_table(restriction_matrix, restriction_results)

    # table initialization
    def create_table(self, restriction_matrix, restriction_results):
        """
        Function that is in charge of creating the table to use
        Inputs: restriction_matrix, restriction_results
        Outputs: Table with the actual values of variables with the processes of solving
        Restrictions: None
        """
        for i in range(self.constraints_len):
            for j in range(self.function_variables_len):
                self.table[i][j] = restriction_matrix[i][j]

            for j in range(self.constraints_len):
                self.table[i][j + self.function_variables_len] = int(i == j)

            self.table[i][-1] = restriction_results[i]

    # getting a row with a maximum negative value of W
    def check_negative_in_row(self):
        """
        Function that is in charge of checking if the row have a negative value
        Inputs: None
        Outputs: The row with the negative value
        Restrictions: None
        """
        row = -1

        for i, a_row in enumerate(self.table):
            if a_row[-1] < 0 and (row == -1 or abs(a_row[-1]) > abs(self.table[row][-1])):
                row = i

        return row

    # getting the column with the maximum modulo element in the row
    def check_negative_in_column(self, row):
        """
        Function that is in charge of check negative value in column
        Inputs: row
        Outputs: The column with the negative value
        Restrictions: None
        """
        column = -1

        for i, aij in enumerate(self.table[row][:-1]):
            if aij < 0 and (column == -1 or abs(aij) > abs(self.table[row][column])):
                column = i

        return column

    # removal of negative free coefficients
    def check_negative_w_function(self):
        """
        Function that is in charge of checking negative values in the calculation of W function
        Inputs: None
        Outputs: None
        Restrictions: None
        """
        while True:
            row = self.check_negative_in_row()  # looking for a line containing negative W

            if row == -1:  # if you do not find such a line
                return True  # then everything is fine :)

            column = self.check_negative_in_column(row)  # looking for a resolving column

            if column == -1:
                return False  # no se pudo borrar

            self.gauss_jordan_method(row, column)  # haciendo eliminación de gauss
            self.solve_for_w_function_values()
            step_line = "\n[!] Negative in LD has been removed in row " + str(row + 1)
            writer_dual_method(False, step_line)
            writer_dual_method(False, 2)
            self.show_table()

    # performing a Gaussian step
    def gauss_jordan_method(self, row, column):
        """
        Function that is in charge of aplying the gauss jordan method to the matrix
        Inputs: row, column
        Outputs: None
        Restrictions: None
        """
        self.table[row] /= self.table[row][column]

        for i in range(self.constraints_len):
            if i != row:
                self.table[i] -= self.table[row] * self.table[i][column]

        self.variables_index[row] = column  # make the variable base

    # calculation of W values
    def solve_for_w_function_values(self):
        """
        Function that is in charge of solving for the w function
        Inputs: None
        Outputs: None
        Restrictions: None
        """
        for i in range(self.variables_len + 1):
            self.w_function_values[i] = -self.function_coefficients[i]

            for j in range(self.constraints_len):
                self.w_function_values[i] += self.function_coefficients[self.variables_index[j]] * self.table[j][i]

    # calculating simplex relations for column column
    def calculate_column_to_column(self, column):
        """
        Function that is in charge of
        Inputs: None
        Outputs: None
        Restrictions: None
        """
        q = []

        for i in range(self.constraints_len):
            if self.table[i][column] == 0:
                q.append(np.inf)
            else:
                q_i = self.table[i][-1] / self.table[i][column]
                q.append(q_i if q_i >= 0 else np.inf)

        return q

    # getting a decision
    def iterate_data(self):
        """
        Function that is in charge of travel the data of the variables in the partial or final solutions
        Inputs: None
        Outputs: None
        Restrictions: None
        """
        y = np.zeros(self.variables_len)

        # fill in the solution
        for i in range(self.constraints_len):
            y[self.variables_index[i]] = self.table[i][-1]

        return y

    # decision
    def solve(self):
        """
        Function that is in charge of solving the dual method, it applies the simplex method,
        but with the matrix trasposed
        Inputs: None
        Outputs: Values calculated
        Restrictions: None
        """
        step_line = '\n[ Step № 0 ]'
        writer_dual_method(False, step_line)
        writer_dual_method(False, 2)

        self.solve_for_w_function_values()
        self.show_table()

        if not self.check_negative_w_function():

            step_line = "\n[!] The dual operation introduced doesn't have a solution"
            self.have_solution = False
            writer_dual_method(False, step_line)
            writer_dual_method(False, 2)
            return False

        step = 1

        while True:
            self.solve_for_w_function_values()

            step_line = "\n | Step № " + str(step) + " |"
            writer_dual_method(False, step_line)
            writer_dual_method(False, 2)

            self.show_table()

            if all(fi >= 0 if self.max_min_operation_to_use == "max" else fi <= 0
                   for fi in self.w_function_values[:-1]):  # if the plan is optimal
                break  # finish the operation

            column = (np.argmin if self.max_min_operation_to_use == "max"
                      else np.argmax)(self.w_function_values[:-1])  # we get the resolving column
            q = self.calculate_column_to_column(column)  # we get a simplex relationship for the found column

            if all(qi == np.inf for qi in q):  # if no resolving string could be found
                step_line = "\n[!] The dual operation introduced doesn't have a solution"
                self.have_solution = False
                writer_dual_method(False, step_line)
                writer_dual_method(False, 2)
                return False

            self.gauss_jordan_method(np.argmin(q), column)  # doing gauss elimination
            step += 1

        return True  # there is a solution

    def show_solutions(self):
        """
        Function that is in charge of showing or writing to the txt file the final solutions
        Inputs: None
        Outputs: The result contained in a string
        Restrictions: None
        """
        result = ""

        result += "\n[ Dual method operation result ]\n" + "Solution W " + self.max_min_operation_to_use + " = " \
                  + str(self.w_function_values[self.variables_len])

        y = np.zeros(self.variables_len)

        # fill in the solution
        for i in range(self.constraints_len):
            y[self.variables_index[i]] = self.table[i][-1]

        for i in range(self.function_variables_len):
            result += "\n" + "y" + str(i + 1) + " = " + str(y[i])

        writer_dual_method(False, result)
        writer_dual_method(False, 2)

        return result

    # simplex table output
    def show_table(self):
        """
        Function that is in charge of
        Inputs: None
        Outputs: None
        Restrictions: None
        """
        txt_table = "\n" + '     |' + ''.join(
            ['   y%-3d |' % (i + 1) for i in range(self.variables_len)]) + '    LD  |'

        for i in range(self.constraints_len):
            txt_table += "\n" + '%4s |' % ('y' + str(self.variables_index[i] + 1)) \
                         + ''.join([' %6.2f |' % aij for j, aij in enumerate(self.table[i])])

        txt_table += "\n" + '  W  |' + ''.join([' %6.2f |' % aij for aij in self.w_function_values])

        txt_table += "\n" + '  y0 |' + ''.join([' %6.2f |' % xi for xi in self.iterate_data()]) + "\n"

        writer_dual_method(False, txt_table)
        writer_dual_method(False, 2)

    # coefficient output
    @staticmethod
    def show_coefficients(posterior_coefficient, i):
        """
        Function that is in charge of
        Inputs: None
        Outputs: None
        Restrictions: None
        """
        if posterior_coefficient == 1:
            return 'y%d' % (i + 1)

        if posterior_coefficient == -1:
            return '-y%d' % (i + 1)

        return '%.2fy%d' % (posterior_coefficient, i + 1)

    # task output
    def show_dual_operation_statement(self, full=False):
        """
        Function that is in charge of print or write in txt file the values of the dual operation to solve
        Inputs: None
        Outputs: None
        Restrictions: None
        """
        operation_dual = "[ Dual Method Operation Statement ]\n\n" + "Objective Function"
        operation_dual += '\n ' + ' + '.join(['%.2fy%d' % (ci, i + 1) for i, ci in
                                             enumerate(self.function_coefficients[:self.function_variables_len])
                                             if ci != 0]) + ' -> ' + str(self.max_min_operation_to_use) + '\n '
        operation_dual += "Subject to: \n"
        # Writes in the txt file
        writer_dual_method(False, operation_dual)
        # Close the txt file
        writer_dual_method(False, 2)
        i = 0
        for row in self.table:
            if full:
                dual_operation_variables = ' + '.join([self.show_coefficients(posterior_coefficient, i)
                                                       for i, posterior_coefficient in
                                                       enumerate(row[:self.variables_len])
                                                       if posterior_coefficient != 0]) + '=' + str(row[-1]) + '\n '
                # Writes in the txt file
                writer_dual_method(False, dual_operation_variables)
                # Close the txt file
                writer_dual_method(False, 2)
            else:
                dual_operation_variables = ' + '.join([self.show_coefficients(posterior_coefficient, i)
                                                       for i, posterior_coefficient
                                                       in enumerate(row[:self.function_variables_len])
                                                       if posterior_coefficient != 0]) + " " + \
                                           str(self.restriction_signs[i]) + " " + str(row[-1]) + '\n '
                # Writes in the txt file
                writer_dual_method(False, dual_operation_variables)
                # Close the txt file
                writer_dual_method(False, 2)
                i += 1


def reformat_arrays(objective_function_raw, restriction_matrix_raw):
    """
    Function that is in charge of reformating the arrays for better use in the functions
    Inputs: objective_function_raw, restriction_matrix_raw
    Outputs: objective_function, restriction_matrix, restriction_results
    Restrictions: None
    """
    data_len = (len(objective_function_raw))

    # Selects 1: (all elements except the first one)
    objective_function = np.array(objective_function_raw[1:])

    # Create the numpy array
    restriction_matrix_temp = np.array(restriction_matrix_raw)

    # Selects the rows 1: (all rows except first one)
    # and columns 1:data_len (all columns except first one)
    restriction_matrix = restriction_matrix_temp[1:, 1:data_len]

    # Selects the rows 1: (all rows except first one)
    # and columns data_len (only the first one)
    restriction_results = restriction_matrix_temp[1:, 0]

    return objective_function, restriction_matrix, restriction_results


def primal_to_dual(restriction_matrix, restriction_results, objective_function):
    """
    Function that is in charge of trasposing of the arrays obtained to apply the dual method
    Inputs: restriction_matrix, restriction_results, objective_function
    Outputs: The arrays trasposed an set to use the dual instead of primal
    Restrictions: None
    """
    # The T stands for the numpy method to traspose a matrix
    return -restriction_matrix.T, -objective_function, restriction_results


def dual_method(max_min_operation_to_use, txt_generation_is_checked, objective_function_raw,
                restriction_matrix_raw, restriction_signs):
    """
    Function that is in charge of reformating the obtained
    Inputs: max_min_operation_to_use, txt_generation_is_checked, objective_function_raw,
                restriction_matrix_raw, restriction_signs
    Outputs: The result of the desired dual method operation
    Restrictions: None
    """

    # Create the txt file or cleans it
    writer_dual_method(True, "")

    # Set the arrays for doing more organized the algorithm
    objective_function, restriction_matrix, restriction_results = reformat_arrays(objective_function_raw,
                                                                                  restriction_matrix_raw)

    restriction_matrix, restriction_results, objective_function = primal_to_dual(restriction_matrix,
                                                                                 restriction_results,
                                                                                 objective_function)

    dual_method_operation = DualMethod(objective_function, restriction_matrix, restriction_results,
                                       max_min_operation_to_use, restriction_signs)

    dual_method_operation.show_dual_operation_statement()
    dual_method_operation.solve()

    if dual_method_operation.have_solution:
        result = dual_method_operation.show_solutions()
    else:
        result = "\n[!] The dual operation introduced doesn't have a solution \n W " \
                 + max_min_operation_to_use + " = ∞"

    return result
