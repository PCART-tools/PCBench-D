def _orthogonalize(matrix, epsilon=0):
    """
    Applies Gram-Schmidt procedure to orthogonalize a given 2D tensor.
    If epsilon is 0, this is equivalent to `torch.qr(matrix, out=(matrix, _))`,
    """
    # TODO Consider using Q = torch.orgqr(*torch.geqrf(A)) to compute the Q of the QR _much_ faster
    # and more reliably.
    # Works on FP32/64 or complex numbers (does not work for half precision)
    num_cols = matrix.shape[1]
    for i in range(num_cols):
        # Normalize the i'th column.
        col = matrix[:, i : i + 1]
        # If no epsilon is added here, division by zero may be caused by vanishing gradients.
        # This epsilon is not needed if the input matrix covers the gradients of at least one entire layer in the neural network.
        if epsilon == 0:
            # Note that col ** 2 can underflow/overflow if we use FP16.
            # May need to consider multiplying a scaling factor and dividing it later, or using bfloat16 instead.
            try:
                col /= torch.norm(col)
            except ZeroDivisionError:
                logging.error(
                    "The matrix to be orthogonalized has at least a column of all 0s. Please set a small value such as 1e-8 "
                    "as `orthogonalization_epsilon` in PowerSGD state."
                )
                # Recover the values from NaNs to 0s.
                col.fill_(0.0)
        else:
            col /= torch.norm(col) + epsilon
        # Project it on the rest and remove it.
        if i + 1 < num_cols:
            rest = matrix[:, i + 1 :]
            rest -= torch.sum(col * rest, dim=0) * col
