def check_quantized_results_close(outputs, ref=None, symmetric=False, atol_scale=0.53):
    if ref is None:
        ref = outputs[0][0]
    if ref.size == 0:
        return
    ref_min = min(np.min(ref), 0)
    ref_max = max(np.max(ref), 0)
    if symmetric:
        ref_scale = 2 * max(abs(ref_max), abs(ref_min)) / 255
    else:
        ref_scale = (ref_max - ref_min) / 255
    # should be divided by 2 in an exact math, but divide by 1.9 here
    # considering finite precision in floating-point numbers
    atol = ref_scale * atol_scale
    for o in outputs[1:]:
        np.testing.assert_allclose(o[0], outputs[0][0], atol=atol, rtol=0)
