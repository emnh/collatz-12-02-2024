#!/usr/bin/env python3

from math import gcd

def find_solution_equation(a_num, a_den, b_num, b_den):
    """
    Find the parametric equation for integer solutions of y = (a_num/a_den) * x + (b_num/b_den).
    
    Parameters:
    a_num: int - Numerator of a
    a_den: int - Denominator of a
    b_num: int - Numerator of b
    b_den: int - Denominator of b
    
    Returns:
    equation: tuple - (y_general, x_general), the parametric solution as strings
    """
    from math import gcd

    # Step 1: Clear fractions
    m = lcm(a_den, b_den)
    p_prime = m * a_num // a_den
    r_prime = m * b_num // b_den

    # Step 2: Solve modular equation for smallest y
    g = gcd(m, abs(p_prime))
    delta_y = abs(p_prime) // g
    delta_x = m // g

    # Check if modular inverse exists
    mod_inverse = modular_inverse(m, abs(p_prime))
    if mod_inverse == -1:
        raise ValueError("No modular inverse exists; no solutions possible.")

    # Smallest positive y
    y_initial = (mod_inverse * (r_prime % abs(p_prime))) % abs(p_prime)

    # General equations
    y_general = f"y = {y_initial} + k * {delta_y}"
    x_general = f"x = ({m} * y - {r_prime}) / {p_prime}"

    return x_general, y_general

def find_integer_solutions(a_num, a_den, b_num, b_den):
    """
    Find integer solutions for y = (a_num/a_den) * x + (b_num/b_den)

    Parameters:
    a_num: int - Numerator of a
    a_den: int - Denominator of a
    b_num: int - Numerator of b
    b_den: int - Denominator of b

    Returns:
    solutions: list of tuples [(x, y), ...] for the first few solutions
    """
    # Step 1: Clear fractions by finding lcm of denominators
    m = lcm(a_den, b_den)  # Least common multiple of a_den and b_den
    p_prime = m * a_num // a_den  # Scaled integer coefficient for x
    r_prime = m * b_num // b_den  # Scaled constant term

    # Step 2: Solve the modular equation m * y ≡ r_prime (mod p_prime)
    # Find the smallest positive y using modular arithmetic
    y_initial = modular_inverse(m, abs(p_prime)) * (r_prime % abs(p_prime)) % abs(p_prime)

    # Step 3: Find general solution
    solutions = []
    delta_y = abs(p_prime) // gcd(m, p_prime)  # Step size for y
    delta_x = m // gcd(m, p_prime)            # Step size for x

    # Generate the first few solutions
    for c in range(0, 6):  # Adjust range for how many solutions you want
        y = y_initial + c * delta_y
        x = (m * y - r_prime) // p_prime
        if x > 0 and y > 0:
            solutions.append((x, y))

    return solutions


def lcm(a, b):
    """Calculate least common multiple of two integers."""
    return abs(a * b) // gcd(a, b)

def modular_inverse(a, m):
    """
    Calculate modular inverse of a modulo m using Extended Euclidean Algorithm.
    Returns -1 if no modular inverse exists.
    """
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return -1  # No modular inverse if gcd(a, m) != 1
    return x % m

def extended_gcd(a, b):
    """Extended Euclidean Algorithm. Returns gcd(a, b), x, y such that ax + by = gcd(a, b)."""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y

if __name__ == "__main__":
    # Example Usage
    # Solve y = (3/64)x + (1/16)
    a_num, a_den = 3, 64  # a = 3/64
    b_num, b_den = 1, 16  # b = 1/16

    solutions = find_integer_solutions(a_num, a_den, b_num, b_den)
    print("Integer solutions (x, y):", solutions)