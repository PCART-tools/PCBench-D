def bundle_jpeg_image(img_tensor, quality):
    # turn NCHW to HWC
    if img_tensor.dim() == 4:
        assert(img_tensor.size(0) == 1)
        img_tensor = img_tensor[0].permute(1, 2, 0)
    pixels = img_tensor.numpy()
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    _, enc_img = cv2.imencode(".JPEG", pixels, encode_param)
    enc_img_tensor = torch.from_numpy(enc_img)
    enc_img_tensor = torch.flatten(enc_img_tensor).byte()
    obj = torch.utils.bundled_inputs.InflatableArg(enc_img_tensor, "torch.ops.fb.decode_bundled_image({})")
    return obj
