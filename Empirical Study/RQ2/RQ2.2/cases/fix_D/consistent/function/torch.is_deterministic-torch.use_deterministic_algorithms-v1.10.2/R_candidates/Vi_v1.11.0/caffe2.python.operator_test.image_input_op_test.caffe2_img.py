def caffe2_img(img):
    # Convert RGB to BGR
    img = img[:, :, (2, 1, 0)]
    # Convert HWC to CHW
    img = img.swapaxes(1, 2).swapaxes(0, 1)
    img = img * 255.0
    return img.astype(np.int32)
