#!/usr/bin/env python3

from typing import Tuple, Generator, List, Dict
from tabulate import tabulate

def collatz_op(x: int) -> Tuple[int, int]:
    """
    Perform a single Collatz operation.

    :param x: The current integer.
    :return: A tuple containing the next number in the sequence
             and the operation type (0 for even, 1 for odd).
    """
    return (x // 2, 0) if x % 2 == 0 else (3 * x + 1, 1)

def collatz(x: int, cache: Dict[int, List[int]]) -> List[int]:
    """
    Generate the Collatz sequence for a given integer using a cache for compact notation.

    :param x: The starting integer of the sequence. Must be a positive integer.
    :param cache: A dictionary to store and retrieve precomputed Collatz sequences.
    :return: The Collatz sequence, possibly compacted with C(num) notation.
    """
    if x <= 0:
        raise ValueError("Input must be a positive integer.")

    sequence = []
    while x != 1:
        if x in cache:
            # Use compact notation for the cached sequence
            sequence.append(f"C({x})")
            break
        sequence.append(x)
        x, _ = collatz_op(x)

    if x == 1:
        sequence.append(1)  # Add the final 1 to the sequence

    # Update the cache with the newly computed sequence
    for idx, num in enumerate(sequence):
        if isinstance(num, int):  # Only cache numbers, not compacted strings
            cache[num] = sequence[idx:]

    return sequence

def collatz_string(sequence: List[int]) -> str:
    """
    Convert a Collatz sequence into a string with binary operation hints.

    :param sequence: A list of integers in the Collatz sequence.
    :return: A string representation of the sequence with compacted references.
    """
    return "->".join(map(str, sequence))

# Cache for Collatz sequences
cache = {}

# Generate and display Collatz sequences for numbers from 1 to 19
data = []  # Store rows of data for tabulation
for i in range(1, 20):
    nums = collatz(i, cache)  # Generate the Collatz sequence with caching
    seq = collatz_string(nums)  # Convert to a compact string representation
    data.append([i, seq])  # Append the data for tabulation

# Create a table using tabulate
print(tabulate(
    data,
    headers=["Start", "Collatz Sequence"],
    tablefmt="fancy_grid",
    colalign=("right", "right")  # Right-align all columns
))