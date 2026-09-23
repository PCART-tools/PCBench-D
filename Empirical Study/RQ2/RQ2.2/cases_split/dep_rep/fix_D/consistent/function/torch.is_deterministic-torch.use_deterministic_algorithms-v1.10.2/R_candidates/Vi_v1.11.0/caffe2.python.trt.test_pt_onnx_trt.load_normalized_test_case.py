def load_normalized_test_case(input_shape, test_image, pagelocked_buffer, normalization_hint):
    def normalize_image(image):
        c, h, w = input_shape
        image_arr = np.asarray(image.resize((w, h), Image.ANTIALIAS)).transpose([2, 0, 1])\
            .astype(trt.nptype(trt.float32)).ravel()
        if (normalization_hint == 0):
            return (image_arr / 255.0 - 0.45) / 0.225
        elif (normalization_hint == 1):
            return (image_arr / 256.0 - 0.5)
    np.copyto(pagelocked_buffer, normalize_image(Image.open(test_image)))
    return test_image
