def sepia(white="#fff0c0"):
    bands = [make_linear_lut(0, band) for band in ImageColor.getrgb(white)]
    return ImagePalette("RGB", [bands[i % 3][i // 3] for i in range(256 * 3)])
