@register_backend
def eager(gm, fake_tensor_inputs, **kwargs):
    if kwargs:
        log.warning("eager backend ignoring extra kwargs %s", kwargs)
    return gm.forward
