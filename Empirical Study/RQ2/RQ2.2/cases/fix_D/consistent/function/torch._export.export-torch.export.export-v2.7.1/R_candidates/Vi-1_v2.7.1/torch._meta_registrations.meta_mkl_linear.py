        @register_meta(torch.ops.mkl._mkl_linear)
        def meta_mkl_linear(input_tensor, packed_weight, orig_weight, bias, batch_size):
            return input_tensor.new_empty(
                (*input_tensor.shape[:-1], orig_weight.shape[0])
            )
