    def _linear_call(users=1):
        return CallFunction(
            mkldnn._linear_pointwise.default, *_linear_args, _users=users
        )
