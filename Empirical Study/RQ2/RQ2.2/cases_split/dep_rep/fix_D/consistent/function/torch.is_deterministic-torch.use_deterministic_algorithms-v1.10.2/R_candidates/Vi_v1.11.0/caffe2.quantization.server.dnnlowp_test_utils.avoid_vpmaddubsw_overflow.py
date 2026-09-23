def avoid_vpmaddubsw_overflow(
    strides,
    pads,
    kernels,
    dilations,
    sizes,
    input_channels,
    output_channels,
    batch_size,
    X,
    X_min,
    X_max,
    W,
    W_min,
    W_max,
):
    ndim = len(sizes)
    dkernels = tuple((dilations[i] * (kernels[i] - 1) + 1) for i in range(ndim))
    size_cols = tuple(
        (sizes[i] + 2 * pads[i] - dkernels[i]) // strides[i] + 1 for i in range(ndim)
    )
    for out_idx in np.ndindex((batch_size,) + size_cols + (output_channels,)):
        b = out_idx[0]
        oc = out_idx[-1]
        o_spatial = out_idx[1:-1]
        for filter_idx1, filter_idx2 in pairwise(
            np.ndindex(kernels + (input_channels,))
        ):
            f0 = filter_idx1[:-1]
            ic0 = filter_idx1[-1]

            f1 = filter_idx2[:-1]
            ic1 = filter_idx2[-1]

            i0s = tuple(
                strides[i] * o_spatial[i] - pads[i] + dilations[i] * f0[i]
                for i in range(ndim)
            )
            i1s = tuple(
                strides[i] * o_spatial[i] - pads[i] + dilations[i] * f1[i]
                for i in range(ndim)
            )

            w0 = W[(oc,) + f0 + (ic0,)] - 128 - W_min
            w1 = W[(oc,) + f1 + (ic1,)] - 128 - W_min

            if all(0 <= i0s[i] < sizes[i] for i in range(ndim)):
                x0 = X[(b,) + i0s + (ic0,)] - X_min
            else:
                # padding
                x0 = -X_min

            if all(0 <= i1s[i] < sizes[i] for i in range(ndim)):
                x1 = X[(b,) + i1s + (ic1,)] - X_min
            else:
                # padding
                x1 = -X_min

            if x0 * w0 + x1 * w1 < -(1 << 15):
                w1_adjusted = (-(1 << 15) - float(x0) * w0) / x1
                W[(oc,) + f1 + (ic1,)] = int(w1_adjusted) + 128 + W_min
            elif x0 * w0 + x1 * w1 >= (1 << 15):
                w1_adjusted = ((1 << 15) - 1 - float(x0) * w0) / x1
                W[(oc,) + f1 + (ic1,)] = int(w1_adjusted) + 128 + W_min

    # Go through the same loop again to double check we don't have any overflow
    for out_idx in np.ndindex((batch_size,) + size_cols + (output_channels,)):
        b = out_idx[0]
        oc = out_idx[-1]
        o_spatial = out_idx[1:-1]
        for filter_idx1, filter_idx2 in pairwise(
            np.ndindex(kernels + (input_channels,))
        ):
            f0 = filter_idx1[:-1]
            ic0 = filter_idx1[-1]

            f1 = filter_idx2[:-1]
            ic1 = filter_idx2[-1]

            i0s = tuple(
                strides[i] * o_spatial[i] - pads[i] + dilations[i] * f0[i]
                for i in range(ndim)
            )
            i1s = tuple(
                strides[i] * o_spatial[i] - pads[i] + dilations[i] * f1[i]
                for i in range(ndim)
            )

            w0 = W[(oc,) + f0 + (ic0,)] - 128 - W_min
            w1 = W[(oc,) + f1 + (ic1,)] - 128 - W_min

            if all(0 <= i0s[i] < sizes[i] for i in range(ndim)):
                x0 = X[(b,) + i0s + (ic0,)] - X_min
            else:
                # padding
                x0 = -X_min

            if all(0 <= i1s[i] < sizes[i] for i in range(ndim)):
                x1 = X[(b,) + i1s + (ic1,)] - X_min
            else:
                # padding
                x1 = -X_min

            assert -(1 << 15) <= x0 * w0 + x1 * w1 < (1 << 15)
