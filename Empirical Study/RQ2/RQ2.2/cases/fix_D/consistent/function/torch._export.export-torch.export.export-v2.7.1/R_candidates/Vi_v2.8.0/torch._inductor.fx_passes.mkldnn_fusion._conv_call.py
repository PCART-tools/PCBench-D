    def _conv_call(users=1):
        return CallFunction(
            mkldnn._convolution_pointwise.default, *_conv_args, _users=users
        )
