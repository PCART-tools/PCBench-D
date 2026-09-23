@register_meta(aten.relu_.default)
def meta_relu_(self):
    return self
