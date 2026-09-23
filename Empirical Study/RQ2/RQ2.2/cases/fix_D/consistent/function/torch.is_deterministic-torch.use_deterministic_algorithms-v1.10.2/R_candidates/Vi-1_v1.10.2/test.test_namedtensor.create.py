def create(namedshape, factory=torch.randn):
    # namedshape: str
    names, shape = parse_compressed_namedshape(namedshape)
    return factory(shape, names=names)
