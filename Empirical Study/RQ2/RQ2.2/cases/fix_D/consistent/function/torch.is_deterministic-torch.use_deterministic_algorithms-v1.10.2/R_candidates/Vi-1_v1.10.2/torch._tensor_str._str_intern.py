def _str_intern(inp):
    prefix = 'tensor('
    indent = len(prefix)
    suffixes = []

    # This is used to extract the primal value and thus disable the forward AD
    # within this function.
    # TODO(albanD) This needs to be updated when more than one level is supported
    self, tangent = torch.autograd.forward_ad.unpack_dual(inp)

    # Note [Print tensor device]:
    # A general logic here is we only print device when it doesn't match
    # the device specified in default tensor type.
    # Currently torch.set_default_tensor_type() only supports CPU/CUDA, thus
    # torch._C._get_default_device() only returns either cpu or cuda.
    # In other cases, we don't have a way to set them as default yet,
    # and we should always print out device for them.
    if self.device.type != torch._C._get_default_device()\
            or (self.device.type == 'cuda' and torch.cuda.current_device() != self.device.index):
        suffixes.append('device=\'' + str(self.device) + '\'')

    # TODO: add an API to map real -> complex dtypes
    _default_complex_dtype = torch.cdouble if torch.get_default_dtype() == torch.double else torch.cfloat
    has_default_dtype = self.dtype in (torch.get_default_dtype(), _default_complex_dtype, torch.int64, torch.bool)
    if self.is_sparse:
        suffixes.append('size=' + str(tuple(self.shape)))
        suffixes.append('nnz=' + str(self._nnz()))
        if not has_default_dtype:
            suffixes.append('dtype=' + str(self.dtype))
        indices_prefix = 'indices=tensor('
        indices = self._indices().detach()
        indices_str = _tensor_str(indices, indent + len(indices_prefix))
        if indices.numel() == 0:
            indices_str += ', size=' + str(tuple(indices.shape))
        values_prefix = 'values=tensor('
        values = self._values().detach()
        values_str = _tensor_str(values, indent + len(values_prefix))
        if values.numel() == 0:
            values_str += ', size=' + str(tuple(values.shape))
        tensor_str = indices_prefix + indices_str + '),\n' + ' ' * indent + values_prefix + values_str + ')'
    elif self.is_sparse_csr:
        suffixes.append('size=' + str(tuple(self.shape)))
        suffixes.append('nnz=' + str(self._nnz()))
        if not has_default_dtype:
            suffixes.append('dtype=' + str(self.dtype))
        crow_indices_prefix = 'crow_indices=tensor('
        crow_indices = self.crow_indices().detach()
        crow_indices_str = _tensor_str(crow_indices, indent + len(crow_indices_prefix))
        if crow_indices.numel() == 0:
            crow_indices_str += ', size=' + str(tuple(crow_indices.shape))
        col_indices_prefix = 'col_indices=tensor('
        col_indices = self.col_indices().detach()
        col_indices_str = _tensor_str(col_indices, indent + len(col_indices_prefix))
        if col_indices.numel() == 0:
            col_indices_str += ', size=' + str(tuple(col_indices.shape))
        values_prefix = 'values=tensor('
        values = self.values().detach()
        values_str = _tensor_str(values, indent + len(values_prefix))
        if values.numel() == 0:
            values_str += ', size=' + str(tuple(values.shape))
        tensor_str = crow_indices_prefix + crow_indices_str + '),\n' + ' ' * indent +\
            col_indices_prefix + col_indices_str + '),\n' + ' ' * indent +\
            values_prefix + values_str + ')'
    elif self.is_quantized:
        suffixes.append('size=' + str(tuple(self.shape)))
        if not has_default_dtype:
            suffixes.append('dtype=' + str(self.dtype))
        suffixes.append('quantization_scheme=' + str(self.qscheme()))
        if self.qscheme() == torch.per_tensor_affine or self.qscheme() == torch.per_tensor_symmetric:
            suffixes.append('scale=' + str(self.q_scale()))
            suffixes.append('zero_point=' + str(self.q_zero_point()))
        elif self.qscheme() == torch.per_channel_affine or self.qscheme() == torch.per_channel_symmetric \
                or self.qscheme() == torch.per_channel_affine_float_qparams:
            suffixes.append('scale=' + str(self.q_per_channel_scales()))
            suffixes.append('zero_point=' + str(self.q_per_channel_zero_points()))
            suffixes.append('axis=' + str(self.q_per_channel_axis()))
        tensor_str = _tensor_str(self.dequantize(), indent)
    else:
        if self.is_meta:
            suffixes.append('size=' + str(tuple(self.shape)))
            if self.dtype != torch.get_default_dtype():
                suffixes.append('dtype=' + str(self.dtype))
            # TODO: This implies that ellipses is valid syntax for allocating
            # a meta tensor, which it could be, but it isn't right now
            tensor_str = '...'
        else:
            if self.numel() == 0 and not self.is_sparse:
                # Explicitly print the shape if it is not (0,), to match NumPy behavior
                if self.dim() != 1:
                    suffixes.append('size=' + str(tuple(self.shape)))

                # In an empty tensor, there are no elements to infer if the dtype
                # should be int64, so it must be shown explicitly.
                if self.dtype != torch.get_default_dtype():
                    suffixes.append('dtype=' + str(self.dtype))
                tensor_str = '[]'
            else:
                if not has_default_dtype:
                    suffixes.append('dtype=' + str(self.dtype))

                if self.layout != torch.strided:
                    tensor_str = _tensor_str(self.to_dense(), indent)
                else:
                    tensor_str = _tensor_str(self, indent)

    if self.layout != torch.strided:
        suffixes.append('layout=' + str(self.layout))

    # Use inp here to get the original grad_fn and not the one generated by the forward grad
    # unpacking.
    if inp.grad_fn is not None:
        name = type(inp.grad_fn).__name__
        if name == 'CppFunction':
            name = inp.grad_fn.name().rsplit('::', 1)[-1]
        suffixes.append('grad_fn=<{}>'.format(name))
    elif inp.requires_grad:
        suffixes.append('requires_grad=True')

    if self.has_names():
        suffixes.append('names={}'.format(self.names))

    if tangent is not None:
        suffixes.append('tangent={}'.format(tangent))

    return _add_suffixes(prefix + tensor_str, suffixes, indent, force_newline=self.is_sparse)
