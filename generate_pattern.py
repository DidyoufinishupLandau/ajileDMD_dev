# -*- coding: utf-8 -*-
"""
Author: Pan Zhang
"""
import numpy as np
import scipy
from skimage import transform
class DmdPattern():
    def __init__(self,pattern: str, width: int, height: int, gray_scale: int=255):
        """
        A class to generate mask pattern for DMD
        :param pattern: the name of pattern. Can be "hadamard" or "random"
        :param width: the width of image
        :param height: the height of image
        :param gray_scale: the gray scale of image. Range from 0 to 255.
        """
        self.pattern = pattern
        self.width = width
        self.height = height
        self.hadmard_size = width**2
        self.gray_scale = gray_scale
    def execute(self, random_sparsity:int = 1):
        """
        The execution function for mask generation.
        :param random_sparsity: The percentage of elements in random mask to be 1.
        :return:
        Under hadamard mode:
        List: A list contain whole set of hadamard pattern that drive the DMD to point to left.
        List: A list contain whole set of hadamard pattern that drive the DMD to point to right.
        Under random mode:
        nd.array: A single random pattern with given sparsity that point left.
        nd.array: A single random pattern with given sparsity that point right.
        """
        if self.pattern == "hadamard":
            positive_image = hadmard_matrix(self.hadmard_size)
            positive_image = walsh_to_hadmard_mask(positive_image)

            def reshape_image(two_dimension_image):
                two_dimension_image = two_dimension_image * self.gray_scale
                return two_dimension_image.T[:,:, np.newaxis]
            positive_image_list = map(reshape_image, positive_image)

            return list(positive_image_list)

        elif self.pattern == "random":
            positive_image = random_pattern(self.width, self.height, random_sparsity) * self.gray_scale
            return positive_image.T[:,:,np.newaxis]
###############################################################################following code do random pattern
def random_pattern(width, height, sparsity):
    mask_array = (np.random.rand(height, width) < sparsity).astype(int)
    return mask_array.astype(np.uint8)
############################################################################### following code do hadmard mask
def bit_reverse_permutation(num_bits):
    data = np.linspace(0,2**num_bits-1, 2**num_bits)
    n = len(data)
    num_bits = len(bin(n - 1)) - 2
    result = [0] * n
    for i in range(n):
        reversed_index = int(format(i, f'0{num_bits}b')[::-1], 2)
        result[reversed_index] = data[i]
    
    return result
def generate_gray_code(n):
    if n <= 0:
        return [""]
    smaller_gray_codes = generate_gray_code(n - 1)
    result = []
    for code in smaller_gray_codes:
        result.append("0" + code)
    for code in reversed(smaller_gray_codes):
        result.append("1" + code)

    return result

def gray_code_permutation(num_bits):
    gray_codes = generate_gray_code(num_bits)
    decimal_permutation = [int(code, 2) for code in gray_codes]
    return decimal_permutation

def hadmard_matrix(system_size):
    """
    generate hadmard matrix using scipy library
    :param system_size: The width or height of hadmard matrix.
    :return:
        array: Two dimension array
        array: two dimension array
    """
    hadmard_matrix = scipy.linalg.hadamard(system_size)
    array_one = (hadmard_matrix == 1).astype(int)
    array_one = array_one.astype(np.uint8)
    return array_one

def walsh_to_hadmard_mask(input_matrix):
    """
    Map the hadmard matrix into walsh matrix
    :param input_matrix: 2D array
    :return: walsh matrix
    """
    small_matrix_size = int(np.sqrt(len(input_matrix[0])))
    num_rows, num_cols = input_matrix.shape
    num_small_matrices = num_rows // small_matrix_size
    small_matrices = []

    reverse_bit_string = bit_reverse_permutation(int(np.log2(num_rows)))
    gray_code_string = generate_gray_code(int(np.log2(num_rows)))
    for i in range(len(gray_code_string)):
        gray_code_string[i] = int(gray_code_string[i], 2)

    def mapping(n):
        n = gray_code_string[int(reverse_bit_string[n])]
        return n
    mapping_list = [mapping(i) for i in range(num_rows)]
    mapping_list = np.array(mapping_list)
    new_list = []
    for i in range(len(mapping_list)):
        new_list.append(np.where(mapping_list==i)[0][0])
    new_list = np.array(new_list)
    for i in range(num_small_matrices):
        for j in range(num_small_matrices):
            start_row = i * small_matrix_size
            end_row = start_row + small_matrix_size
            start_col = j * small_matrix_size
            end_col = start_col + small_matrix_size
            small_matrix = []
            row_number = np.linspace(start_row, end_row - 1, end_row-start_row).astype(int)
            for n in range(len(row_number)):
                small_matrix.append(input_matrix[new_list[row_number[n]], start_col:end_col])
            small_matrix = np.array(small_matrix)
            small_matrices.append(small_matrix)
    return np.array(small_matrices)
