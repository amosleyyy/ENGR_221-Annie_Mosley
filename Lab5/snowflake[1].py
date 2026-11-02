
"""
ENGR 221 - Lab 5: Recursion
Koch Snowflake implementation using recursion and an explicit stack.
"""

import turtle
import time
from memory_profiler import memory_usage


class KochSnowflake:
    """Draw and compare recursive and non-recursive Koch snowflakes."""

    def __init__(self, length, depth):
        """Set the starting side length and recursion depth."""
        self.init_length = length
        self.init_depth = depth
        self.t = None

    def init_turtle(self):
        """Set up the Turtle graphics window."""
        self.t = turtle.Turtle()
        self.t.speed(0)
        self.t.pensize(2)
        self.t.penup()
        self.t.goto(-self.init_length / 2, self.init_length / 3)
        self.t.setheading(0)
        self.t.pendown()

    def draw_curve_recursive(self):
        """Draw one side of the snowflake recursively."""
        self.draw_curve_recursive_helper(
            self.init_length, self.init_depth
        )

    def draw_curve_recursive_helper(self, length, depth):
        """Draw one Koch curve using recursive calls."""
        if depth == 0:
            self.t.forward(length)
            return

        third = length / 3

        self.draw_curve_recursive_helper(third, depth - 1)
        self.t.left(60)

        self.draw_curve_recursive_helper(third, depth - 1)
        self.t.right(120)

        self.draw_curve_recursive_helper(third, depth - 1)
        self.t.left(60)

        self.draw_curve_recursive_helper(third, depth - 1)

    def draw_curve_stack(self):
        """Draw one Koch curve using an explicit stack."""
        commands = [("curve", self.init_length, self.init_depth)]

        while commands:
            command = commands.pop()
            kind = command[0]

            if kind == "curve":
                length = command[1]
                depth = command[2]

                if depth == 0:
                    self.t.forward(length)
                else:
                    third = length / 3

                    # Add commands in reverse drawing order.
                    commands.append(("curve", third, depth - 1))
                    commands.append(("left", 60))
                    commands.append(("curve", third, depth - 1))
                    commands.append(("right", 120))
                    commands.append(("curve", third, depth - 1))
                    commands.append(("left", 60))
                    commands.append(("curve", third, depth - 1))

            elif kind == "left":
                self.t.left(command[1])

            elif kind == "right":
                self.t.right(command[1])

    def draw_snowflake_recursive(self):
        """Draw all three sides using recursion."""
        self.init_turtle()

        for _ in range(3):
            self.draw_curve_recursive()
            self.t.right(120)

        turtle.done()

    def draw_snowflake_stack(self):
        """Draw all three sides using an explicit stack."""
        self.init_turtle()

        for _ in range(3):
            self.draw_curve_stack()
            self.t.right(120)

        turtle.done()

    def get_time_and_mem(self, func):
        """Measure execution time and memory usage."""
        time_start = time.perf_counter()
        mem_usage = memory_usage(
            (func,), interval=0.1, include_children=True
        )
        time_end = time.perf_counter()

        time_taken = time_end - time_start
        mem_used = max(mem_usage) - min(mem_usage)

        return time_taken, mem_used

    def compare_snowflake(self):
        """Compare the time and memory used by both methods."""
        rec_time, rec_mem = self.get_time_and_mem(
            self.draw_snowflake_recursive
        )

        stack_time, stack_mem = self.get_time_and_mem(
            self.draw_snowflake_stack
        )

        print(f"Recursive memory usage: {rec_mem:.4f} MB")
        print(f"Stack memory usage: {stack_mem:.4f} MB")
        print(f"Recursive time taken: {rec_time:.5f} seconds")
        print(f"Stack time taken: {stack_time:.5f} seconds")


if __name__ == "__main__":
    # Change the 2 to 0, 1, 2, or 3 to change the detail.
    snowflake = KochSnowflake(300, 2)

    # Part 2: Recursive version
    snowflake.draw_snowflake_recursive()

    # Part 3: Stack version (use this instead when testing):
    # snowflake.draw_snowflake_stack()

    # Part 4: Comparison (use this instead when measuring):
    # snowflake.compare_snowflake()
