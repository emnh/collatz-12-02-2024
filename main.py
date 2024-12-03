#!/usr/bin/env python3

def collatz(x):
    """
    Generator function to produce the Collatz sequence for a given integer x.

    :param x: The starting integer of the sequence. Must be a positive integer.
    :yield: The next number in the Collatz sequence.
    """
    if x <= 0:
        raise ValueError("Input must be a positive integer.")
    
    while x != 1:
        yield x
        if x % 2 == 0:  # If x is even
            x //= 2
        else:           # If x is odd
            x = 3 * x + 1
    yield x  # Finally yield 1

for i in range(1, 20):
    nums = list(collatz(i))
    print(nums)
