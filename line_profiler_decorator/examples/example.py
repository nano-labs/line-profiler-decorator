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


def memory_profiler(*args, **kwargs):
    """Line by line memory profiler.

    :param args[0]: If defined will output usage to the file otherwise print
        usage to stdout.
    """
    try:
        from memory_profiler import profile as mprofile
    except ImportError:
        raise Exception(
            "memory_profiler is not installed. "
            "You can install it with:"
            "\n\tpip install memory_profiler"
        )

    class DummyFileDescriptor:
        """Workaround to flush memory profiler output.

        memory_profiler may write output on file but never flushes it.
        This class forces flush on every write.
        """

        def __init__(self, filename):
            self.file = open(filename, "a")

        def write(self, line):
            response = self.file.write(line)
            self.file.flush()
            return response

    output_file = None
    if args:
        if callable(args[0]):
            return mprofile(args[0])
        else:
            output_file = args[0]
            return mprofile(stream=DummyFileDescriptor(output_file))

    return mprofile


@memory_profiler
def bla():
    x = [2] * 100000000
    e = "2eee" * 10000000000
    return x, e
