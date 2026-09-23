def _decompression_bomb_check(size):
    if MAX_IMAGE_PIXELS is None:
        return

    pixels = size[0] * size[1]

    if pixels > 2 * MAX_IMAGE_PIXELS:
        raise DecompressionBombError(
            f"Image size ({pixels} pixels) exceeds limit of {2 * MAX_IMAGE_PIXELS} "
            "pixels, could be decompression bomb DOS attack."
        )

    if pixels > MAX_IMAGE_PIXELS:
        warnings.warn(
            f"Image size ({pixels} pixels) exceeds limit of {MAX_IMAGE_PIXELS} pixels, "
            "could be decompression bomb DOS attack.",
            DecompressionBombWarning,
        )
