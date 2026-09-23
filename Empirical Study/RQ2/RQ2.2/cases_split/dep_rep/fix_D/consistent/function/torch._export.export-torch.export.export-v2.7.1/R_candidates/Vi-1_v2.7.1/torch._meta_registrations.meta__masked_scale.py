@register_meta(aten._masked_scale.default)
def meta__masked_scale(self, mask, scale):
    masked_scale = self.new_empty(self.size()).to(
        memory_format=utils.suggest_memory_format(self)
    )
    return masked_scale
