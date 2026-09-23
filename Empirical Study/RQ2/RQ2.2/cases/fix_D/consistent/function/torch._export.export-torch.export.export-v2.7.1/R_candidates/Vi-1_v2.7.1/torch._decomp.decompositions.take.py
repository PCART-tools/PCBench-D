@register_decomposition(aten.take)
@out_wrapper()
def take(self, index):
    flattened = self.reshape(-1)
    return flattened[index]
