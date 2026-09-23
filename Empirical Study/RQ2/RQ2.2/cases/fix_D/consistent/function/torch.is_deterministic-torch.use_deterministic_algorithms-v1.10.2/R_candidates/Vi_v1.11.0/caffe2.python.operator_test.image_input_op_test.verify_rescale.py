def verify_rescale(img, minsize):
    # Here we use OpenCV transformation to match the C code
    scale_amount = float(minsize) / min(img.shape[0], img.shape[1])
    if scale_amount <= 1.0:
        return img

    print("Scale amount is %f -- should be < 1.0; got shape %s" %
          (scale_amount, str(img.shape)))
    assert False
    img_cv = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    output_shape = (int(np.ceil(scale_amount * img_cv.shape[0])),
                    int(np.ceil(scale_amount * img_cv.shape[1])))
    resized = cv2.resize(img_cv,
                         dsize=output_shape,
                         interpolation=cv2.INTER_AREA)

    resized = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    assert resized.shape[0] >= minsize
    assert resized.shape[1] >= minsize
    return resized
