def isrealobj(x: ArrayLike):
    return not torch.is_complex(x)
