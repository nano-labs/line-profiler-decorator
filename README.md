# line-profiler-decorator
Wrapper around (line-profiler)[https://github.com/rkern/line_profiler] adding a few features as an decorator

## Install
```shell
pip install line-profiler-decorator
```

## Usage
```python
from time import sleep
from line_profiler_decorator import profiler


@profiler
def slow_function():
    print("quick line")
    sleep(1)  # slow one
    sleep(0.3)  # not that slow
```

### Output
```
quick line
Timer unit: 1e-06 s

Total time: 6.52823 s
File: /Users/fabio/projects/line-profiler-decorator/examples/example.py
Function: slow_function at line 5

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     5                                           @profiler(aggregate=True)
     6                                           def slow_function():
     7         5         69.0     13.8      0.0      print("quick line")
     8         5    5016944.0 1003388.8     76.8     sleep(1)  # slow one
     9         5    1511218.0 302243.6      23.1     sleep(0.3)  # not that slow

```

## Options

### Save output to a file
Save the output to a file instead of stdout
```python
@profiler("output_file.txt")
def slow_function():
    print("quick line")
    sleep(1)  # slow one
    sleep(0.3)  # not that slow
```

### Aggregate results
Aggregate the results of multiple calls to the decorated function
```python
@profiler(aggregate=True)
def slow_function():
    print("quick line")
    sleep(1)  # slow one
    sleep(0.3)  # not that slow

def run_slow(n=100):
    for _ in range(n):
        slow_function()
```

### Follow function
```python
from time import sleep
from line_profiler_decorator import profiler


def other_function():
    sleep(1)  # slow one
    sleep(0.3)  # not that slow


@profiler(follow=[other_function])
def function_that_calls_other_function(n):
    for _ in range(n):
        other_function()
```

#### Output
```
In [3]: function_that_calls_other_function(10)                                                                                                                                      
Timer unit: 1e-06 s

Total time: 13.0668 s
File: /Users/fabio/projects/line-profiler-decorator/examples/example.py
Function: other_function at line 17

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    17                                           def other_function():
    18        10   10037030.0 1003703.0     76.8      sleep(1)  # slow one
    19        10    3029725.0 302972.5     23.2      sleep(0.3)  # not that slow

Total time: 13.0672 s
File: /Users/fabio/projects/line-profiler-decorator/examples/example.py
Function: function_that_calls_other_function at line 22

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    22                                           @profiler(follow=[other_function])
    23                                           def function_that_calls_other_function(n):
    24        11         97.0      8.8      0.0      for _ in range(n):
    25        10   13067104.0 1306710.4    100.0          other_function()
```

### Grouped aggregations
Group aggregations using a key function.
`key` is a function that receives the same arguments as the decorated function and returns a value.
The profile results of each call of the decorated function will be grouped and aggregated together by the value returned by the `key` function

#### Example:
```python
from time import sleep
from line_profiler_decorator import profiler


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
```
#### Output
The `key` function returns value `True` for even numbers and `False` for odd numbers.
That way the aggregated results will be grouped into 2 profile results.

```
Timer unit: 1e-06 s

Total time: 3.533 s
File: /Users/fabio/projects/line-profiler-decorator/examples/example.py
Function: function_with_filtered_aggregations at line 28

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    28                                           @profiler(aggregate=True, key=lambda x: x % 2 == 0)
    29                                           def function_with_filtered_aggregations(number):
    30                                               """This function runs faster for even numbers."""
    31         5         17.0      3.4      0.0      if number % 2:
    32                                                   # sleep for 1 second if number is odd
    33                                                   sleep(1)
    34                                               else:
    35                                                   # sleep for 0.2 second if number is even
    36         5    1015312.0 203062.4     28.7          sleep(0.2)
    37         5    2517674.0 503534.8     71.3      sleep(0.5)

Timer unit: 1e-06 s

Total time: 7.53658 s
File: /Users/fabio/projects/line-profiler-decorator/examples/example.py
Function: function_with_filtered_aggregations at line 28

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    28                                           @profiler(aggregate=True, key=lambda x: x % 2 == 0)
    29                                           def function_with_filtered_aggregations(number):
    30                                               """This function runs faster for even numbers."""
    31         5         15.0      3.0      0.0      if number % 2:
    32                                                   # sleep for 1 second if number is odd
    33         5    5017337.0 1003467.4     66.6          sleep(1)
    34                                               else:
    35                                                   # sleep for 0.2 second if number is even
    36                                                   sleep(0.2)
    37         5    2519231.0 503846.2     33.4      sleep(0.5)
```
Looking at the results above we can see that the first block only aggregated call with even `number`
therefore spent no time at line 33. On the other hand, the second block shows the same for odd numbers
where no time was used on even numbers.
