def logsumexp_grad(grad_out, outputs, inputs):
    sum_exps = np.sum(np.exp(inputs[0]), axis=0)
    return np.repeat(
        np.expand_dims(grad_out / sum_exps, 0),
        inputs[0].shape[0],
        axis=0
    ) * np.exp(inputs[0])
