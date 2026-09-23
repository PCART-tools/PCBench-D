    @functools.cache
    def _mkldnn_fusion_init():
        # TODO: aarch64: enable op fusion for acl once it supports fused operators. Disabling it for now.
        # Otherwise even the matmul or innerproduct can not be accelerated with acl
        if (
            torch.backends.mkldnn.enabled
            and torch.backends.mkldnn.is_available()
            and not torch.ops.mkldnn._is_mkldnn_acl_supported()
        ):
            _register_unary_fusion()
            _register_inplace_fusion()
            _register_binary_unary_fusion()
            _register_binary_fusion()
            _register_quantization_lowerings()
            _register_woq_lowerings()
