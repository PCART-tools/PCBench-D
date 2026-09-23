@register_meta([aten._fft_c2c.default, aten._fft_c2c.out])
@out_wrapper()
def meta_fft_c2c(self, dim, normalization, forward):
    torch._check(self.dtype.is_complex)
    if not dim:
        return self.clone()

    sorted_dims = _sort_dims(self, dim)
    out = self.new_empty(self.size())
    return _exec_fft(out, self, self.size(), sorted_dims, forward=forward)
