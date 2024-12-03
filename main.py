#!/usr/bin/env python3

from typing import Tuple, Generator, List
from tabulate import tabulate

def collatz_op(x: int) -> Tuple[int, int]:
    """
    Perform a single Collatz operation.

    :param x: The current integer.
    :return: A tuple containing the next number in the sequence
             and the operation type (0 for even, 1 for odd).
    """
    return (x // 2, 0) if x % 2 == 0 else (3 * x + 1, 1)

def collatz(x: int) -> Generator[int, None, None]:
    """
    Generator function to produce the Collatz sequence for a given integer.

    :param x: The starting integer of the sequence. Must be a positive integer.
    :yield: The next number in the Collatz sequence.
    """
    if x <= 0:
        raise ValueError("Input must be a positive integer.")
    
    while x != 1:
        yield x
        x, _ = collatz_op(x)
    yield x  # Finally yield 1

def collatz_string(sequence: List[int]) -> str:
    """
    Convert a Collatz sequence into a binary string based on operations.

    :param sequence: A list of integers in the Collatz sequence.
    :return: A binary string where 0 represents an even operation
             and 1 represents an odd operation.
    """
    return "".join(
        str(collatz_op(x)[1]) for x in sequence
    )

def compact_sequence(sequence: List[int]) -> str:
    """
    Compactly represent a Collatz sequence as a comma-separated string.

    :param sequence: A list of integers in the Collatz sequence.
    :return: A compact string representation of the sequence.
    """
    return ",".join(map(str, sequence))

# Generate and display Collatz sequences for numbers from 1 to 19
data = []  # Store rows of data for tabulation
for i in range(1, 20):
    nums = list(collatz(i))  # Generate the Collatz sequence
    seq = collatz_string(nums)  # Generate the binary operation string
    compact_nums = compact_sequence(nums)  # Compact the Collatz numbers
    data.append([i, seq, compact_nums])  # Append the data for tabulation

# Create a table using tabulate with right-aligned columns and compacted number sequences
print(tabulate(
    data,
    headers=["Start", "Binary Sequence", "Collatz Sequence"],
    tablefmt="fancy_grid",
    colalign=("right", "right", "right")  # Right-align all columns
))
