# BEGIN OUTLINE
"""
A benchmark utility *en miniature*.

Example. The following code...
```
    from benchtools import timed, timed_titled
    from math import factorial

    @timed
    def weeks_to_seconds(weeks):
        seconds = weeks * 7 * 24 * 60 * 60
        return seconds

    weeks_6 = weeks_to_seconds(6)
    fac_10 = timed(factorial)(10)
    test = timed_titled("equality test", lambda: weeks_6 == fac_10)()
    print(f"{'Yes' if test else 'No'}, 10! is {'exactly' if test else 'not'} equal to the number of seconds in six weeks.")
```
...should result in output akin to the following:
```
    | +0.000s | weeks_to_seconds
    | +0.000s | factorial
    | +0.000s | equality test
    Yes, 10! is exactly equal to the number of seconds in six weeks.
```
"""
# END   OUTLINE


# BEGIN IMPORTS

import time
import functools as ft

# END   IMPORTS


# BEGIN CONSTANTS
# No constants
# END   CONSTANTS


# BEGIN DECORATORS

def timed_titled(title, f, show_args=False, show_kwargs=False):
    """Produce a timed function associated with an explicit title.

    Args:
        title (str): Title to be printed when printing measured time to console.
        f (callable): Arbitrary function to be run.
        show_args (bool): Whether to additionally print all normal arguments.
        show_kwargs (bool): Whether to additionally print all keyword arguments.

    Returns:
        callable: Identical signature to original function f.
    """
    @ft.wraps(f)
    def timed_f(*args, **kwargs):
        begin_time = time.perf_counter()
        result     = f(*args, **kwargs)
        end_time   = time.perf_counter()
        time_taken = end_time - begin_time
        str1 = f"| +{time_taken:.03f}s | {title}"
        str2 = f"\n{len(str1)*' '}|{args}" if show_args and args else ''
        str3 = f"\n{len(str1)*' '}|{kwargs}" if show_kwargs and kwargs else ''
        print(f"{str1}{str2}{str3}")
        return result
    return timed_f

def timed(f):
    """Produce a timed function with its __name__ as title.

    Args:
        f (callable): Arbitrary function to be run.

    Returns:
        callable: Identical signature to original function f.
    """
    return timed_titled(f.__name__, f)

# END   DECORATORS


# BEGIN CLASSES
# No classes
# END   CLASSES


# BEGIN FUNCTIONS
# No functions
# END   FUNCTIONS


# BEGIN MAIN
# No main
# END   MAIN
