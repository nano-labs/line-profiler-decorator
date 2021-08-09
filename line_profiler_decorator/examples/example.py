from time import sleep
from line_profiler_decorator import profiler


@profiler(aggregate=True)
def slow_function():
    print("quick line")
    sleep(1)  # slow one
    sleep(0.3)  # not that slow


def run_slow(n=100):
    for _ in range(n):
        slow_function()


def other_function():
    sleep(1)  # slow one
    sleep(0.3)  # not that slow


@profiler(follow=[other_function])
def function_that_calls_other_function(n):
    for _ in range(n):
        other_function()


@profiler(aggregate=True, key=lambda x: x % 2 == 0)
def function_with_grouped_aggregations(number):
    """This function runs faster for even numbers."""
    if number % 2:
        # sleep for 1 second if number is odd
        sleep(1)
    else:
        # sleep for 0.2 second if number is even
        sleep(0.2)
    sleep(0.5)


def run_function_with_grouped_aggregations(n=10):
    for _ in range(n):
        function_with_grouped_aggregations(_)
