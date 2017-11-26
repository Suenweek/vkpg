def offset(max_count, total):
    while total:
        if total < max_count:
            cur_count = total
        else:
            cur_count = max_count
        total -= cur_count
        yield cur_count
