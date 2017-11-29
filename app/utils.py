from collections import namedtuple


OffsetIteration = namedtuple("OffsetIteration", ["offset", "count"])


def offset_range(total, count_max, offset=0):
    if total <= 0:
        raise ValueError("total must be pos int")
    if count_max <= 0:
        raise ValueError("count_max must be pos int")

    while total:
        if total < count_max:
            count_cur = total
        else:
            count_cur = count_max
        yield OffsetIteration(offset, count_cur)
        total -= count_cur
        offset += count_cur
