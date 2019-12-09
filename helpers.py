# Sorting functions
def priority(x):
    return x.priority


def approach(a, b, max_step):
    """ Returns a new value for a, which approaches b with a particular step size, such that
        it doesn't pass b.
    """

    # If the values are equal, you don't need to approach
    if a == b:
        return a

    # Otherwise, move in the closer direction at a max speed of rate
    diff = b - a
    if diff < 0:
        return a - min(max_step, abs(diff))
    else:
        return a + min(max_step, diff)