import png
from itertools import chain, repeat, cycle


def _interleave0(row, planes, new_planes):
    for i, item in zip(cycle(range(planes)), row):
        yield item
        if i == planes - 1:
            yield from repeat(0, new_planes - planes)


def add_alpha(pixels, meta):
    """
    Ensure alpha channel is available in a pypng image.
    """

    meta["alpha"] = True

    if "planes" not in meta:
        meta["planes"] = 4 if meta["alpha"] else 3

    if meta["planes"] < 4:
        pixels = map(lambda row: _interleave0(row, meta["planes"], 4), pixels)
        meta["planes"] = 4

    return pixels, meta


def add_row(pixels, meta, row):
    """
    Add a row to the end of a pypng image.
    """
    meta["size"] = meta["size"][0], meta["size"][1] + 1
    pixels = chain(pixels, [row])
    return pixels, meta


if __name__ == '__main__':
    _, _, pixels, meta = png.Reader(file=open("test.png", "rb")).read()

    pixels, meta = add_alpha(pixels, meta)
    pixels, meta = add_row(pixels, meta, repeat(0, meta["size"][0] * meta["planes"]))

    with open("test.out.png", "wb") as f:
        png.Writer(*meta["size"], **meta).write(f, pixels)
