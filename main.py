#!/usr/bin/env python3

def collatzOp(x):
    if x % 2 == 0:
        return (x // 2, 0)
    else:
        return (3 * x + 1, 1)

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
        x = collatzOp(x)[0]
    yield x  # Finally yield 1

def collatzString(sequence):
    l = [str(collatzOp(x)[1]) for x in sequence]
    return "".join(l)

for i in range(1, 20):
    nums = list(collatz(i))
    seq = collatzString(nums)
    print(seq, nums)