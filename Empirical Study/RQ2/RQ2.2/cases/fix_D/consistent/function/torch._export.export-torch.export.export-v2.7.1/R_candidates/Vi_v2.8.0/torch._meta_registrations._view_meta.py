@register_meta(aten.view.default)
def _view_meta(a, *shape):
    if torch.fx.experimental._config.backed_size_oblivious or _view_has_unbacked_input(
        a, shape
    ):
        return _view_unbacked_meta(a, shape)
    else:
        return torch._refs._reshape_view_helper(a, *shape, allow_copy=False)
