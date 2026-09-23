    def _conv_transpose_call(users=1):
        return CallFunction(
            mkldnn._convolution_transpose_pointwise.default,
            *_conv_transpose_args,
            _users=users,
        )
