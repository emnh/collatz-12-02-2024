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

def binary_sequence(sequence: List[int]) -> str:
    """
    Generate the binary sequence of operations for a Collatz sequence.

    :param sequence: A list of integers in the Collatz sequence.
    :return: A binary string where 0 represents division by 2 and 1 represents 3x + 1.
    """
    return "".join(str(collatz_op(x)[1]) for x in sequence if isinstance(x, int))

# Cache for Collatz sequences
cache = {}

# Generate data for the table
data = []  # Store rows of data for tabulation
for i in range(1, 20):
    full_sequence = collatz(i, cache, restrict_cache=False)  # Compact for any cached x
    restricted_sequence = collatz(i, cache, restrict_cache=True)  # Compact only for x < starting number
    binary_seq = binary_sequence(full_sequence)  # Binary sequence of operations
    full_seq_str = collatz_string(full_sequence, separator="→")  # Full sequence with compacting for any x
    restricted_seq_str = collatz_string(restricted_sequence, separator="→")  # Compact sequence for x < starting number
    data.append([i, binary_seq, full_seq_str, restricted_seq_str])  # Append all columns

# Create a table using tabulate
print(tabulate(
    data,
    headers=["Start", "Binary Sequence", "Compact (C(x) for any x)", "Compact (C(x) only if x < Start)"],
    tablefmt="fancy_grid",
    colalign=("right", "right", "right", "right")  # Right-align all columns
))