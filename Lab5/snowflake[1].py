"""
Name: Annie Mosley
Last updated: November 1, 2026
Description: Draws a Koch snowflake using recursive and stack-based methods,
             and compares the time and memory used by each approach.
"""

import turtle
import time
from memory_profiler import memory_usage


class KochSnowflake:
    """Draw and compare Koch snowflakes using recursion and an explicit stack."""

    def __init__(self, init_length=500, init_depth=3):
        """Initialize the turtle reference, starting edge length, and depth."""
        self.t = None
        self.init_length = init_length
        self.init_depth = init_depth

    def init_turtle(self):
        """Initialize the turtle and move it to the appropriate starting point."""
        t = turtle.Turtle()
        t.speed(8)
        t.teleport(-200, -200)
        self.t = t

    ######################
    # Draw curve methods #
    ######################

    def draw_curve_recursive(self):
        """Start drawing one side of the Koch snowflake recursively."""
        self.draw_curve_recursive_helper(self.init_length, self.init_depth)

    def draw_curve_recursive_helper(self, length, depth):
        """Draw one Koch-curve side by replacing each segment with four smaller curves."""
        if depth < 0:
            raise ValueError("Depth cannot be negative")

        # At depth zero, draw one straight segment.
        if depth == 0:
            self.t.forward(length)
        else:
            # Each recursive call draws one third of the current segment.
            third = length / 3
            self.draw_curve_recursive_helper(third, depth - 1)
            self.t.right(60)
            self.draw_curve_recursive_helper(third, depth - 1)
            self.t.left(120)
            self.draw_curve_recursive_helper(third, depth - 1)
            self.t.right(60)
            self.draw_curve_recursive_helper(third, depth - 1)

    def draw_curve_stack(self):
        """Draw one Koch-curve side iteratively using a last-in, first-out stack."""
        commands = [("add_curve", self.init_length, self.init_depth)]

        while commands:
            command = commands.pop()
            command_type = command[0]

            if command_type == "add_curve":
                length, depth = command[1], command[2]
                if depth < 0:
                    raise ValueError("Depth cannot be negative")

                if depth == 0:
                    self.t.forward(length)
                else:
                    third = length / 3
                    # Push operations in reverse order because the stack is LIFO.
                    commands.append(("add_curve", third, depth - 1))
                    commands.append(("right", 60))
                    commands.append(("add_curve", third, depth - 1))
                    commands.append(("left", 120))
                    commands.append(("add_curve", third, depth - 1))
                    commands.append(("right", 60))
                    commands.append(("add_curve", third, depth - 1))

            elif command_type == "left":
                self.t.left(command[1])
            elif command_type == "right":
                self.t.right(command[1])
            else:
                raise ValueError(f"Unknown drawing command: {command_type}")

    ##########################
    # Draw snowflake methods #
    ##########################

    def draw_snowflake_recursive(self):
        """Draw all three sides of the snowflake using the recursive curve method."""
        self.init_turtle()
        for _ in range(3):
            self.draw_curve_recursive()
            self.t.left(120)
        turtle.clearscreen()

    def draw_snowflake_stack(self):
        """Draw all three sides of the snowflake using the non-recursive stack method."""
        self.init_turtle()
        for _ in range(3):
            self.draw_curve_stack()
            self.t.left(120)
        turtle.clearscreen()

    ##########################
    # Compare the approaches #
    ##########################

    def compare_snowflake(self):
        """Print the time and memory used by the recursive and stack approaches."""
        rec_time, rec_mem = self.get_time_and_mem(self.draw_snowflake_recursive)
        nonrec_time, nonrec_mem = self.get_time_and_mem(self.draw_snowflake_stack)

        print(f"Recursive memory usage: {rec_mem} MB")
        print(f"Non-recursive memory usage: {nonrec_mem} MB")
        print()
        print(f"Recursive time taken: {rec_time:.5f} s")
        print(f"Non-recursive time taken: {nonrec_time:.5f} s")

    def get_time_and_mem(self, func):
        """Measure elapsed time and sampled memory increase while running a function."""
        time_start = time.perf_counter()
        mem_usage = memory_usage((func,), include_children=True, multiprocess=True)
        time_end = time.perf_counter()

        time_taken = time_end - time_start
        mem_used = max(mem_usage) - min(mem_usage)
        return time_taken, mem_used


if __name__ == "__main__":
    s = KochSnowflake(500, 0)

    # Part 2: run the recursive version first.
    s.draw_snowflake_recursive()

    # Part 3: to test the stack version, comment out the recursive line above
    # and uncomment the following line.
    # s.draw_snowflake_stack()

    # Part 4: to compare both versions, comment out the drawing call above
    # and uncomment the following line. Record the printed measurements.
    # s.compare_snowflake()
