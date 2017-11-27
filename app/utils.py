from collections import namedtuple


OffsetIteration = namedtuple("OffsetIteration", ["offset", "count"])


# TODO: Add description
def offset_range(total, count_max):
    """
    :param total:
    :param count_max:
    :return:
    """
    if total <= 0:
        raise ValueError("total must be pos int")
    if count_max <= 0:
        raise ValueError("count_max must be pos int")

    offset = 0
    queue = total
    while queue:
        if queue < count_max:
            count_cur = queue
        else:
            count_cur = count_max
        yield OffsetIteration(offset, count_cur)
        queue -= count_cur
        offset += count_cur


def once():
    def gen():
        yield True
        while True:
            yield False
    g = gen()
    return lambda: next(g)
