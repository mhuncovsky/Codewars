from functools import wraps


def memoize(f):
    results = {}

    @wraps(f)
    def wrapper(n):
        if n not in results:
            results[n] = f(n)
        return results[n]

    return wrapper


@memoize
def fib(n):
    """Dijkstra's algorithm for Fibonacci (EWD654 "In honor of Fibonacci")
    URL: http://www.cs.utexas.edu/users/EWD/ewd06xx/EWD654.PDF

    https://www.nayuki.io/page/fast-fibonacci-algorithms
    """

    if n == 0:
        return 0
    if n == 1:
        return 1

    if n < 0:
        n = -n
        if n % 2 == 0:
            return -fib2(n)

    if n % 2 == 0:
        nn = n // 2
        return (2 * fib2(nn - 1) + fib2(nn)) * fib2(nn)
    else:
        nn = n // 2 + 1
        return fib2(nn - 1)**2 + fib2(nn)**2
