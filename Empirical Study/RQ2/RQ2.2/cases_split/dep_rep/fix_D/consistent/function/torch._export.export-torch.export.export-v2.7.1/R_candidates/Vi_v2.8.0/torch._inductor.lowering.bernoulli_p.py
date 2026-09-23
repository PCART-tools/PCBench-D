@register_lowering(aten.bernoulli.p, type_promotion_kind=None)
def bernoulli_p(x, *args):
    assert config.fallback_random or x.get_device() == torch.device("cpu"), (
        "this should be handled in decomps unless config.fallback_random or the device is CPU"
    )
    return bernoulli_(clone(x), *args)
