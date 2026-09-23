def angle(z: ArrayLike, deg=False):
    result = torch.angle(z)
    if deg:
        result = result * (180 / torch.pi)
    return result
