def transform_row(row: list, transpose=0, reversed=False, inverted=False):
    result = []
    for i in row:
        x = (i + transpose) % len(row)
        if inverted:
            x = (len(row) - x) % len(row)
        result.append(x)
    if reversed:
        result.reverse()
    return result


def generator_from_row(row:list):
    i = 0
    while True:
        yield row[i]
        i += 1
        if i == len(row):
            i = 0

