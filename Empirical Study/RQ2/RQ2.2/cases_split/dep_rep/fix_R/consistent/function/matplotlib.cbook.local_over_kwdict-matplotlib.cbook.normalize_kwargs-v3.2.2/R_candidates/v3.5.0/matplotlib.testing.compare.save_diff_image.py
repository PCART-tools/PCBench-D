def save_diff_image(expected, actual, output):
    """
    Parameters
    ----------
    expected : str
        File path of expected image.
    actual : str
        File path of actual image.
    output : str
        File path to save difference image to.
    """
    # Drop alpha channels, similarly to compare_images.
    expected_image = np.asarray(Image.open(expected).convert("RGB"))
    actual_image = np.asarray(Image.open(actual).convert("RGB"))
    actual_image, expected_image = crop_to_same(
        actual, actual_image, expected, expected_image)
    expected_image = np.array(expected_image).astype(float)
    actual_image = np.array(actual_image).astype(float)
    if expected_image.shape != actual_image.shape:
        raise ImageComparisonFailure(
            "Image sizes do not match expected size: {} "
            "actual size {}".format(expected_image.shape, actual_image.shape))
    abs_diff_image = np.abs(expected_image - actual_image)

    # expand differences in luminance domain
    abs_diff_image *= 255 * 10
    save_image_np = np.clip(abs_diff_image, 0, 255).astype(np.uint8)
    height, width, depth = save_image_np.shape

    # The PDF renderer doesn't produce an alpha channel, but the
    # matplotlib PNG writer requires one, so expand the array
    if depth == 3:
        with_alpha = np.empty((height, width, 4), dtype=np.uint8)
        with_alpha[:, :, 0:3] = save_image_np
        save_image_np = with_alpha

    # Hard-code the alpha channel to fully solid
    save_image_np[:, :, 3] = 255

    Image.fromarray(save_image_np).save(output, format="png")
