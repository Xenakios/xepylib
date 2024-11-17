# Super simple serialism related stuff, probably doesn't work like
# the standard serialism/dodecaphony stuff, this only for my own use really...


def transform_row(
    row: list[int], transpose=0, reversed=False, inverted=False
) -> list[int]:
    result = []
    for i in row:
        x = (i + transpose) % len(row)
        if inverted:
            x = (len(row) - x) % len(row)
        result.append(x)
    if reversed:
        result.reverse()
    return result


def generator_from_row(row: list):
    i = 0
    while True:
        yield row[i]
        i += 1
        if i == len(row):
            i = 0
