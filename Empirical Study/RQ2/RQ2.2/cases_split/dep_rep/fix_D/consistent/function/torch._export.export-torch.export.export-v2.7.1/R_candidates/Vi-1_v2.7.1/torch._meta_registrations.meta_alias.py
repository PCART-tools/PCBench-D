@register_meta(aten.alias.default)
def meta_alias(self):
    return self.view(self.shape)
