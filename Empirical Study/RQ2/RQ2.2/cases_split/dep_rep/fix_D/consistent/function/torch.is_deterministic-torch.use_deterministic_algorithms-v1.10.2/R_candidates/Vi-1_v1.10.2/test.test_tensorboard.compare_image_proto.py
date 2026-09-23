def compare_image_proto(actual_proto, function_ptr):
    expected_str = read_expected_content(function_ptr)
    expected_proto = Summary()
    text_format.Parse(expected_str, expected_proto)

    [actual, expected] = [actual_proto.value[0], expected_proto.value[0]]
    actual_img = Image.open(io.BytesIO(actual.image.encoded_image_string))
    expected_img = Image.open(io.BytesIO(expected.image.encoded_image_string))

    return (
        actual.tag == expected.tag and
        actual.image.height == expected.image.height and
        actual.image.width == expected.image.width and
        actual.image.colorspace == expected.image.colorspace and
        actual_img == expected_img
    )
