def verify_color_normalize(img, means, stds):
    # Note the RGB/BGR inversion
    # Operate on integers like the C version
    img = img * 255.0
    img[:, :, 0] = (img[:, :, 0] - means[2]) / stds[2]
    img[:, :, 1] = (img[:, :, 1] - means[1]) / stds[1]
    img[:, :, 2] = (img[:, :, 2] - means[0]) / stds[0]
    return img * (1.0 / 255.0)
