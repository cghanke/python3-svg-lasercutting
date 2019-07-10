
def edges(iterator):
    """
    Returns the edges from series of vertices as an interable of start
    and end (x, y) tuples.

    Args:
         iterator: iterator yielding (x, y) tuple

    Returns: iterable of ((x, y), (x, y)) tuples

    """
    # from official itertools recipes at
    # https://docs.python.org/3/library/itertools.html
    def pairwise(iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        from itertools import tee
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)

    first_corner = None
    for corner, next_corner in pairwise(iterator):
        if not first_corner:
            first_corner = corner
        yield corner, next_corner
    yield next_corner, first_corner

def rectangle(width, height, distance=None, num_fingers=-1):
    """
    returns rectangle  for a finger-joint as iterables of (x, y)
    four yielded tuples form a finger or a hole, 
    if you use it for a polyline or polygon resp.

    Args:
         width: width of the hole
         height: height of the hole
         distance: distance between fingers, defaults to width
         num_fingers: maximum number of fingers, defaults to
                      infinity

    Returns: iterable of (x,y) tuples
    """
    if distance is None:
        distance = width
    pos_x = 0
    count = 0
    while 1:
        yield(pos_x, 0)
        yield(pos_x, height)
        yield(pos_x + width, height)
        yield(pos_x + width, 0)
        pos_x += width + distance
        count += 1
        if num_fingers > 0 and count >= num_fingers:
            break
