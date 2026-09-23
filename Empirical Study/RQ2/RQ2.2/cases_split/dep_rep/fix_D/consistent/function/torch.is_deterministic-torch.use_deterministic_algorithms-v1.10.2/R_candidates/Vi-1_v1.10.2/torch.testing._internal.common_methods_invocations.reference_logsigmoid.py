def reference_logsigmoid(x):
    max_ = np.maximum(x.dtype.type(0), -x)
    z = np.exp(-max_) + np.exp(-x - max_)
    return -(max_ + np.log(z))
