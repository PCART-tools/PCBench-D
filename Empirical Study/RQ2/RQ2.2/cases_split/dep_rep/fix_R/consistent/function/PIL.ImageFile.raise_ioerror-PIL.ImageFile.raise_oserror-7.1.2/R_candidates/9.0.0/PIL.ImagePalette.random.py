def random(mode="RGB"):
    from random import randint

    palette = []
    for i in range(256 * len(mode)):
        palette.append(randint(0, 255))
    return ImagePalette(mode, palette)
