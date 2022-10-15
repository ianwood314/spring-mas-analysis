import json
import numpy as np
from scipy.sparse import diags
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import svds
import sys

def read_input(file = './input.json'):
	'''
	Reads the user supplied input data: a vector of spring constants and a vector of masses

	Args:
		file (str): optional filename and path

	Returns:
		All of the following are global variables...
		bc (str): the boundary condition of the problem
		num_strings (int): number of springs in the system
		springconsts_vec (numpy.ndarray): vector containing spring constants of each spring
		num_masses (int): number of masses in the system
		masses_vec (numpy.ndarray): vector containing the mass of each mass
	'''
	with open(file, 'r') as f:
		input_data = json.load(f)

	global bc
	global num_springs
	global springconsts_vec
	global num_masses
	global masses_vec

	springconsts_vec = np.array(input_data["Spring Constant(s) Vector"])
	num_springs = len(springconsts_vec)
	masses_vec = np.array(input_data["Mass Vector"])
	num_masses = len(masses_vec)

	# define the boundary condition from the input
	if (num_springs == num_masses) & ((num_springs+num_masses) != 0):
		bc = "fixed-open"
	elif ((num_springs-num_masses) == 1):
		bc = "fixed-fixed"
	else:
		sys.exit('-- Input not supported --\n  Please ensure input matches fixed-fixed or fixed-open conditions')

def construct_f(masses):
	'''
	Constructs the force vector by multiplying the mass vector with gravity 

	Args:
		masses (numpy.ndarray): vector of all the masses
	'''
	return 9.81*masses

def construct_K(springconsts, bc):
	'''
	Constructs the stiffness matrix based on the boundary condition: fixed-fixed and fixed-open.
	
	Args:
		springconsts (numpy.ndarray): a vector of spring constants
		bc (str): the boundary condition

	Returns:
		K (numpy.ndarray): the stiffness matrix
	'''
	global K

	if bc == "fixed-fixed":
		maindiag = np.add(springconsts[:len(springconsts)-1], springconsts[1:])
		offdiags = -springconsts[1:len(springconsts)-1]
	if bc == "fixed-open":
		temp = np.append(springconsts[1:], [0])
		maindiag = np.add(springconsts, temp)
		offdiags = -springconsts[1:]
	diagonals = [maindiag, offdiags, offdiags]
	K = diags(diagonals, [0, -1, 1]).toarray()
	return K

def calc_disp(K, f):
	'''
	Calculates the displacement of each mass, does so by solving u = inv(K)*f

	Args:
		K (numpy.ndarray): the stiffness matrix
		f (numpy.ndarray): the force vector
	'''
	return np.linalg.inv(K).dot(f)

def calc_elong(u):
	'''
	Calculates the elongation of each spring

	Args:
		u (numpy.ndarray): the displacement of each mass

	Returns:
		A*u: the difference matrix multiplied with the displacements is elongation
	'''
	global A

	A = diags([np.ones(num_springs), -np.ones(num_masses)], [0, -1], shape=(num_springs, num_masses))
	return A.dot(u.T)

def calc_stress(e, springconsts):
	'''
	Calculates the internal stress of each spring

	Args:
		e (numpy.ndarray): the elongation of each spring
		springconsts (numpy.ndarray): the spring constant for each spring

	Returns:
		C*e: the spring constants matrix multiplied with elongation is internal stress
	'''
	global C

	C = diags([springconsts], [0])
	return C.dot(e.T)

def calc_conditions(matrix):
	'''
	Calculates and prints the singular values, eigenvalues, and condition number of a matrix

	Args:
		matrix (scipy.sparse.dia.dia_matrix): a matrix in compressed spare row format

	Prints:
		s (numpy.ndarray): the singular values of the matrix
		s**2 (numpy.ndarray): the eigenvalues of the matrix (the singular values squared)
		condition number (float): defined as the ratio between the maximum and minimum eigenvalue
	'''
	U, s, VT = svds(matrix, k=min(matrix.shape)-1)
	print(f'  Singular Values: {s}')
	print(f'  Eigenvalues: {s**2}')
	print(f'  Condition Number: {max(s**2) / min(s**2)}')

def main():

	read_input()

	f = construct_f(masses_vec) # construct force vector, f
	K = construct_K(springconsts_vec, bc) # construct stiffness matrix, K
	#print(K)
	u = calc_disp(K, f) # calculate displacement of the masses
	#print(u)
	e = calc_elong(u) # calculate the elongation of each mass
	#print(e)
	w = calc_stress(e, springconsts_vec) # calculate the stress in each spring
	#print(w)

	# calculate singular values, eigenvalues, and condition number
	print('-- Matrix A --')
	calc_conditions(A)
	print('-- Matrix A transponse --')
	calc_conditions(A.T)
	print('-- Matrix C --')
	calc_conditions(C)
	print('-- Matrix K --')
	calc_conditions(K)

if __name__ == '__main__':
	main()