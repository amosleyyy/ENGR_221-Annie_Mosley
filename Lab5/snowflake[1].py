"""
Name: [Annie Mosley]
Last updated: November 1, 2026
Description: Draws a Koch snowflake using recursive and stack-based methods,
             and compares their execution time and memory usage.
"""

import turtle
import time
from memory_profiler import memory_usage


class KochSnowflake:
    """Draw and compare Koch snowflakes using recursion and an explicit stack."""

    def __init__(self, init_length=500, init_depth=3):
        """Store the starting side length and recursion depth."""
        self.t = None
        self.init_length = init_length
        self.init_depth = init_depth

    def init_turtle(self):
        """Create the turtle and move it to the starting position."""
        t = turtle.Turtle()
        t.speed(8)
        t.teleport(-200, -200)
        self.t = t

    def draw_curve_recursive(self):
        """Draw one side of the snowflake using the recursive helper."""
        self.draw_curve_recursive_helper(self.init_length, self.init_depth)

    def draw_curve_recursive_helper(self, length, depth):
        """Draw one Koch-curve side by recursively replacing each segment."""
        if depth < 0:
            raise ValueError("Depth cannot be negative")

        if depth == 0:
            self.t.forward(length)
            return

        third = length / 3

        # The four smaller curves and turns create the outward triangular bump.
        self.draw_curve_recursive_helper(third, depth - 1)
        self.t.right(60)
        self.draw_curve_recursive_helper(third, depth - 1)
        self.t.left(120)
        self.draw_curve_recursive_helper(third, depth - 1)
        self.t.right(60)
        self.draw_curve_recursive_helper(third, depth - 1)

    def draw_curve_stack(self):
        """Draw one Koch-curve side without Python recursion, using a LIFO stack."""
        commands = [("add_curve", self.init_length, self.init_depth)]

        while commands:
            command = commands.pop()
            kind = command[0]

            if kind == "add_curve":
                length, depth = command[1], command[2]
                if depth < 0:
                    raise ValueError("Depth cannot be negative")

                if depth == 0:
                    self.t.forward(length)
                else:
                    third = length / 3
                    # Push in reverse order because a stack is last-in, first-out.
                    commands.append(("add_curve", third, depth - 1))
                    commands.append(("right", 60))
                    commands.append(("add_curve", third, depth - 1))
                    commands.append(("left", 120))
                    commands.append(("add_curve", third, depth - 1))
                    commands.append(("right", 60))
                    commands.append(("add_curve", third, depth - 1))

            elif kind == "left":
                self.t.left(command[1])
            elif kind == "right":
                self.t.right(command[1])
            else:
                raise ValueError(f"Unknown command: {kind}")

    def draw_snowflake_recursive(self):
        """Draw all three sides of the snowflake using recursion."""
        self.init_turtle()
        for _ in range(3):
            self.draw_curve_recursive()
            self.t.left(120)
        turtle.clearscreen()

    def draw_snowflake_stack(self):
        """Draw all three sides of the snowflake using an explicit stack."""
        self.init_turtle()
        for _ in range(3):
            self.draw_curve_stack()
            self.t.left(120)
        turtle.clearscreen()

    def compare_snowflake(self):
        """Measure and print time and memory for both drawing approaches."""
        rec_time, rec_mem = self.get_time_and_mem(self.draw_snowflake_recursive)
        nonrec_time, nonrec_mem = self.get_time_and_mem(self.draw_snowflake_stack)

        print(f"Recursive memory usage: {rec_mem:.4f} MB")
        print(f"Non-recursive memory usage: {nonrec_mem:.4f} MB")
        print()
        print(f"Recursive time taken: {rec_time:.5f} s")
        print(f"Non-recursive time taken: {nonrec_time:.5f} s")

    def get_time_and_mem(self, func):
        """Return elapsed wall-clock time and peak memory increase for a function."""
        time_start = time.perf_counter()
        mem_usage = memory_usage((func,), include_children=True, multiprocess=True)
        time_end = time.perf_counter()

        time_taken = time_end - time_start
        mem_used = max(mem_usage) - min(mem_usage)
        return time_taken, mem_used


if __name__ == "__main__":
    # Use a small depth first; increase to 2 or 3 to see more detail.
    snowflake = KochSnowflake(500, 0)

    # Part 2: test the recursive implementation.
    snowflake.draw_snowflake_recursive()

    # Part 3: to test the stack implementation, comment out the line above
    # and uncomment the line below.
    # snowflake.draw_snowflake_stack()

    # Part 4: to compare both methods, comment out the draw call above
    # and uncomment the line below. Record the printed results in answers.txt.
    # snowflake.compare_snowflake()
