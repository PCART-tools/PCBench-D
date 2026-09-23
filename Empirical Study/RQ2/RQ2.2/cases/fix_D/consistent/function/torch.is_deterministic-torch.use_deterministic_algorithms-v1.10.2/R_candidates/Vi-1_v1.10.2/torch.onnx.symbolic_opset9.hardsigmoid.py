@parse_args("v")
def hardsigmoid(g, self):
    # Set alpha_f to 1 / 6 to make op equivalent to PyTorch's definition of Hardsigmoid.
    # See https://pytorch.org/docs/stable/generated/torch.nn.Hardsigmoid.html
    return g.op("HardSigmoid", self, alpha_f=1 / 6)
