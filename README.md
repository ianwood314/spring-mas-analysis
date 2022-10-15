# Spring-Mass System Analysis

This code calculates the displacement, elongation, and internal forces of each spring-mass in the system. The following sections will describe the following: initial setup for the input, how to run the code, and how to interpret the results.

## Initial Setup

### Download Dependencies

The two dependencies for this code are the `scipy` and `numpy` Python code libraries. To install these libraries on your local machine, run the following lines of code:

1. Type `pip3 install scipy` to  download `scipy`
2. Type `pip3 install numpy` to download `numpy`

For more information on `scipy`, please visit their documentation page [here](https://scipy.org). For more information about `numpy`, please visit their documentation page [here](https://numpy.org/doc/stable/user/whatisnumpy.html). 

### Define the Input

Before running the `main.py` script, the spring constants and masses for the spring-mass system must be defined by the user. The user will define these values as vectors in the `input.json` file as shown in the example below:

```
{
  "Spring Constant(s) Vector": [1,1,1,1],
  "Mass Vector": [1,1,1]
}
```

In the input above, we can see that the user has defined four springs each with a spring constant of 1 and three masses each with a value of 1. The example in the previous section would be a `fixed-fixed` boundary condition.

## Supported Setup

Note that the user does not have the specify the boundary condition of the problem as this can be ascertained from the number of springs and the number of masses. Specifically, if the number of springs is one more than the number of masses, then the boundary condition is `fixed-fixed`. If the number of springs is equal to the number of masses, then the boundary condition is `fixed-open`. Any other case is not supported by this code.

## How to Run the Code

1. Open a terminal in the `spring-mass-analysis` folder
2. Make sure that the `input.json` file is in the same directory as the `main.py` file
3. Alter the input file for the problem you are trying to solve
4. Run the code by typing `python3 main.py` into the terminal

## How to Interpret the Results

After running the `python3 main.py` command, the terminal will output the singular values, eigenvalues, and condition number for A, C, A<sup>T</sup>, and K matrices for the given input below:

**Sample Input**
```
{
  "Spring Constant(s) Vector": [1,1,1,1],
  "Mass Vector": [1,1,1]
}
```

**Sample Output**
```
ianwood@Ians-MacBook-Pro-2 project-1-wood-ian % python3 main.py
-- Matrix A --
  Singular Values: [1.1755705  1.61803399 1.90211303]
  Eigenvalues: [1.38196601 2.61803399 3.61803399]
  Condition Number: 2.6180339887498945
-- Matrix A transponse --
  Singular Values: [1.1755705  1.61803399 1.90211303]
  Eigenvalues: [1.38196601 2.61803399 3.61803399]
  Condition Number: 2.6180339887498945
-- Matrix C --
  Singular Values: [1. 1. 1. 1.]
  Eigenvalues: [1. 1. 1. 1.]
  Condition Number: 1.0
-- Matrix K --
  Singular Values: [1.38196601 2.61803399 3.61803399]
  Eigenvalues: [ 1.90983006  6.85410197 13.09016994]
  Condition Number: 6.85410196624969
```
Here we can see each matrix has its own section with the singular values, eigenvalues, and condition number clearly labeled.

