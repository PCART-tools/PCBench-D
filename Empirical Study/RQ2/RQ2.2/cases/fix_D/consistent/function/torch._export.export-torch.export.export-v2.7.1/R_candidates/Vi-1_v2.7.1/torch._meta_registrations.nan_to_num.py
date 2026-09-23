@register_meta([aten.nan_to_num.default, aten.nan_to_num.out])
@out_wrapper()
def nan_to_num(self, nan=None, posinf=None, neginf=None):
    result_size = list(self.size())
    return self.new_empty(result_size)
