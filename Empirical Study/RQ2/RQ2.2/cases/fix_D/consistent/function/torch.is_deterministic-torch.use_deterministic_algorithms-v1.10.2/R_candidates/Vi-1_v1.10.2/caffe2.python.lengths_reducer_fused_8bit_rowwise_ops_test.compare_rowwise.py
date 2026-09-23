def compare_rowwise(emb_orig, emb_reconstructed, fp16):
    # there is an absolute error introduced per row through int8 quantization
    # and a relative error introduced when quantizing back from fp32 to fp16
    assert emb_orig.shape == emb_reconstructed.shape
    rtol = 1e-8
    if fp16:
        rtol = 1e-3
    erange = np.amax(emb_orig, axis=1) - np.amin(emb_orig, axis=1)

    threshold = erange / 255.0 / 1.9

    for i in range(emb_orig.shape[0]):
        r_orig = emb_orig[i, :]
        r_reconstructed = emb_reconstructed[i, :]

        isclose = np.isclose(r_orig, r_reconstructed, atol=threshold[i], rtol=rtol)
        n_violated = isclose.size - isclose.sum()

        if n_violated > 0:
            print(isclose, threshold[i])
            print(i, r_orig, r_reconstructed, threshold[i], r_orig - r_reconstructed)
        assert n_violated == 0
