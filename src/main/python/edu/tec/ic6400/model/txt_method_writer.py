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

def txt_method_writer():
    print("txt_method_writer")


# function that manipulates the text file with the solution of the big m method.
def writer_dual_method(flag, text):

    # Change the path to access to the folder
    txt_answer_file_path = sys.path[1] + '/src/resources/txt_solutions/dual_method/solucion_temporal.txt'

    # open the text file
    if flag:

        file = open(txt_answer_file_path, "w")
        file.close()
    # Close the text file
    elif flag == False and text == 2:
        file = open(txt_answer_file_path, "a")
        file.close()
    # write to text file
    else:
        file = open(txt_answer_file_path, "a")
        file.writelines(text)


# function that manipulates the text file with the solution of the big m method.
def writer_big_m_method(flag, text):

    # Change the path to access to the folder
    txt_answer_file_path = sys.path[1] + '/src/resources/txt_solutions/big_m_method/solucion_temporal.txt'
    # open the text file
    if flag:
        file = open(txt_answer_file_path, "w")
        file.close()
    # Close the text file
    elif flag == False and text == 2:
        file = open(txt_answer_file_path, "a")
        file.close()
    # write to text file
    else:
        file = open(txt_answer_file_path, "a")

        file.writelines(text)
