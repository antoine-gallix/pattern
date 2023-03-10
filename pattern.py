from dataclasses import dataclass
from typing import List
import click
import itertools
import time


@dataclass
class Sequence:
    sequence: List[int]

    def __add__(self, sequence):
        return Sequence(self.sequence + sequence.sequence)

    def __neg__(self):
        return Sequence([-x for x in self.sequence])

    def reverse(self):
        return Sequence(self.sequence[::-1])

    def offset(self, n):
        return Sequence([x + n for x in self.sequence])

    def __iter__(self):
        return iter(self.sequence)

    def __len__(self):
        return len(self.sequence)

    @property
    def span(self):
        return max(self) - min(self) + 1


class DisplayBuffer:
    def __init__(self, length, height):
        lines = []
        for l in range(height):
            line = []
            for c in range(length):
                line.append(False)
            lines.append(line)
        self.lines = lines

    def toggle(self, length, height):
        self.lines[height][length] = not (self.lines[height][length])

    def print(self):
        length = max(len(line) for line in self.lines)
        print("-" * length)
        for line in self.lines[::-1]:
            for position in line:
                print("*" if position else " ", end="")
            print()
        print("-" * length)


def print_sequence(sequence):
    buf = DisplayBuffer(len(sequence), sequence.span)
    normalized = sequence.offset(min(sequence))
    for i, off in enumerate(sequence):
        buf.toggle(i, off)
    buf.print()


def make_pattern(i):
    cell = Sequence([0])
    for _ in range(i):
        halfsequence = cell + (-cell).offset(cell.span)
        sequence = halfsequence + halfsequence.reverse()
        cell = sequence
    return sequence


def sequence_flow(sequence, freq=60):
    interval = 60 / freq
    for sample in itertools.cycle(sequence):
        print(" " * sample + "*")
        time.sleep(interval)


@click.command
@click.argument("order", type=click.INT)
@click.option("--freq", "-f", type=click.INT, default=60)
def flow(order, freq):
    sequence = make_pattern(order)
    sequence_flow(sequence, freq)


if __name__ == "__main__":
    flow()
