#!/usr/bin/env python3

from typing import Tuple, List, Dict
from tabulate import tabulate
from sympy import symbols, simplify, solve, diff, integrate, limit, series, Matrix
from sympy.plotting import plot
from modular_integer_solver import find_integer_solutions, find_solution_equation

def collatz_op(x: int) -> Tuple[int, int]:
    """
    Perform a single Collatz operation.

    :param x: The current integer.
    :return: A tuple containing the next number in the sequence
             and the operation type (0 for even, 1 for odd).
    """
    return (x // 2, 0) if x % 2 == 0 else (3 * x + 1, 1)

def collatz(x: int, cache: Dict[int, List[int]], restrict_cache: bool = False) -> List[int]:
    """
    Generate the Collatz sequence for a given integer.

    :param x: The starting integer of the sequence. Must be a positive integer.
    :param cache: A dictionary to store and retrieve precomputed Collatz sequences.
    :param restrict_cache: Whether to use compact notation only for numbers smaller than the starting number.
    :return: The Collatz sequence, possibly compacted with C(num) notation.
    """
    if x <= 0:
        raise ValueError("Input must be a positive integer.")

    sequence = []
    starting_number = x

    while x != 1:
        if x in cache and (not restrict_cache or x < starting_number):
            sequence.append(f"C({x})")
            break
        sequence.append(x)
        x, _ = collatz_op(x)

    if x == 1:
        sequence.append(1)  # Add the final 1 to the sequence

    # Cache the computed sequence
    if not restrict_cache:
        for idx, num in enumerate(sequence):
            if isinstance(num, int):  # Only cache numbers, not compacted strings
                cache[num] = sequence[idx:]

    return sequence

def collatz_string(sequence: List[int], separator: str = "→") -> str:
    """
    Convert a Collatz sequence into a string.

    :param sequence: A list of integers in the Collatz sequence.
    :param separator: The separator to use between numbers in the sequence.
    :return: A string representation of the sequence.
    """
    return separator.join(map(str, sequence))

def full_binary_sequence(start: int) -> str:
    """
    Generate the full binary sequence of operations for a starting number.

    :param start: The starting integer.
    :return: A binary string where 0 represents division by 2 and 1 represents 3x + 1.
    """
    binary_seq = []
    x = start
    while x != 1:
        _, operation = collatz_op(x)
        binary_seq.append(str(operation))
        x, _ = collatz_op(x)
    return "".join(binary_seq)

def collatz_transformation(start: int) -> Tuple[int, int]:
    """
    Calculate the effect of the Collatz sequence on the algebraic variable x.

    :param start: The starting integer.
    :return: A tuple (a, b) such that the transformation is ax + b.
    """
    x_var = symbols("x")  # Define a symbolic variable
    transformation = x_var
    current = start

    while current != 1:
        if current % 2 == 0:  # Even operation
            transformation = simplify(transformation / 2)
            current //= 2
        else:  # Odd operation
            transformation = simplify(3 * transformation + 1)
            current = 3 * current + 1

    # Return the coefficients a and b of the transformation ax + b
    return transformation.as_coefficients_dict()[x_var], transformation.as_coefficients_dict()[1]

def findIntegersMatchingAXPlusB(a, b):
    matches = []
    for x in range(1, 1000):
        y = a * x + b
        #print("y = ax + b:", y, "=", a, "*", x, "+", b)
        # Let y1 and y2 be integer solutions for x1 and xy2.
        # Then y1 = a * x1 + b and y2 = a * x2 + b.
        # y2 - y1 = a * x2 + b - (a * x1 + b) = a * (x2 - x1).
        # So then y2 = y1 + a * (x2 - x1)
        if int(y) == y:
            matches.append((x, y))
            continue
            for i in range(1, 11):
                x2 = x * i
                y2 = a * x2 + b
                matches.append((x2, y2))
            #break
    return matches

def main():

    # Cache for Collatz sequences
    cache = {}

    N = 20

    # Generate data for the table
    data = []  # Store rows of data for tabulation
    for i in range(1, N + 1):
        full_sequence = collatz(i, cache, restrict_cache=False)  # Compact for any cached x
        restricted_sequence = collatz(i, cache, restrict_cache=True)  # Compact only for x < starting number
        binary_seq = full_binary_sequence(i)  # Full binary sequence for the starting number
        full_seq_str = collatz_string(full_sequence, separator="→")  # Full sequence with compacting for any x
        restricted_seq_str = collatz_string(restricted_sequence, separator="→")  # Compact sequence for x < starting number
        a, b = collatz_transformation(i)  # Algebraic transformation coefficients
        eqx, eqy = find_solution_equation(a.numerator, a.denominator, b.numerator, b.denominator)
        nums = find_integer_solutions(a.numerator, a.denominator, b.numerator, b.denominator)
        data.append([i, binary_seq, full_seq_str, restricted_seq_str, f"{a}x + {b}", eqx, eqy, nums[0:2]])  # Append all columns

    headers = []
    headers += ["Start", "Full Binary Sequence", "Compact (C(x) for any x)", "Compact (C(x) only if x < Start)", "Transformation"]
    headers += ["X Equation", "Y Equation", "Sample"]

    # Create a table using tabulate
    print(tabulate(
        data,
        headers,
        tablefmt="fancy_grid",
        colalign=("right", "right", "right", "right", "right")  # Right-align all columns
    ))

    for i in range(1, N + 1):
        break
        a, b = collatz_transformation(i)
        matches = findIntegersMatchingAXPlusB(a, b)
        toPrint = []
        for x, y in matches:
            toPrint.append(str(x) + "→" + str(y))
        print(str(i) + ":", "y = ax + b:", "y", "=", a, "*", "x", "+", str(b) + ":", toPrint)
        print("")

if __name__ == "__main__":
    main()
