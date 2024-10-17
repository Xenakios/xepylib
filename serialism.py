def transform_row(row:list, transpose=0, reversed=False, inverted=False):
    result = []
    for i in row:
        x = (i + transpose) % len(row)
        if inverted:
            x = (len(row) - x) % len(row)
        result.append(x)
    if reversed:
        result.reverse()
    return result
