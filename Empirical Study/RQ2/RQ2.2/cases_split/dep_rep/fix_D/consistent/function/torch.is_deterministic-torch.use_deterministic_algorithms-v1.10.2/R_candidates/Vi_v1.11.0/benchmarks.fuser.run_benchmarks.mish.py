def mish(a):
    return a * ((a * 1.0).exp().log1p() / 1.0).tanh()
