    def _disable_tensor_cores():
        torch.set_float32_matmul_precision(_default_float_32_precision)
