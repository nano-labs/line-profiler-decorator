from line_profiler import LineProfiler, show_text


def profiler(*args, **kwargs):
    """Line profiler Output time usage per line.

    :param args[0]: If defined will output usage to the file otherwise print
        usage to stdout
    :param aggregate: If True will aggregate results of each time the function
        is called
    :param key: Aggregation key to be used. Accepts string or callable.
        if callable the key will be called using same args and kwargs as the
        decorated function. This param is useful to filter or diff profiles.
    :param follow: List of functions to follow when profiling.
        If follow functions are defined the output will be the decorated
        function's profile plus all followed functions
    """

    def caller(function):
        def wrapper(*args, **kwargs):
            if aggregate:
                agg_key = key or function.__name__
                if callable(agg_key):
                    agg_key = agg_key(*args, **kwargs)
                if "_LP_AGGREGATORS" not in globals():
                    global _LP_AGGREGATORS  # pylint: disable=global-variable-undefined
                    _LP_AGGREGATORS = {}
                lp, lp_wrapper = _LP_AGGREGATORS.get(agg_key, (None, None))
                if not lp:
                    lp = LineProfiler()
                    for f in follow:
                        lp.add_function(f)
                    lp_wrapper = lp(function)
            else:
                lp = LineProfiler()
                for f in follow:
                    lp.add_function(f)
                lp_wrapper = lp(function)

            response = lp_wrapper(*args, **kwargs)
            if aggregate:
                _LP_AGGREGATORS[agg_key] = (lp, lp_wrapper)

            if output_file:
                with open(output_file, "a") as f:
                    stats = lp.get_stats()
                    show_text(stats.timings, stats.unit, stream=f)
            else:
                lp.print_stats()
            return response

        return wrapper

    aggregate = kwargs.get("aggregate", False)
    key = kwargs.get("key")
    follow = kwargs.get("follow", [])

    output_file = None
    if args:
        if callable(args[0]):
            return caller(args[0])
        output_file = args[0]

    return caller
