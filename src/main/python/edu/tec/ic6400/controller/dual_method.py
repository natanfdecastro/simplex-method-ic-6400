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
import math

# Third party imports

# Local application imports


def dual_method(max_min_operation_to_use, txt_generation_is_checked, objective_function,
                restriction_matrix, restriction_signs):

    # Round the numbers to float in the objective function
    objective_function = [math.floor(number) for number in objective_function]

    # Round the numbers to float in the whole table
    for i in range(len(restriction_matrix)):
        restriction_matrix[i] = [math.floor(number) for number in restriction_matrix[i]]

    print(objective_function)
    print(restriction_matrix)
    print(restriction_signs)

    if txt_generation_is_checked:
        print("Dual Method with txt generation")
    else:
        print("Dual Method with no txt generation")

    if max_min_operation_to_use == "maximize":
        print("Dual Method with maximization")
    else:
        print("Dual Method with minization")
