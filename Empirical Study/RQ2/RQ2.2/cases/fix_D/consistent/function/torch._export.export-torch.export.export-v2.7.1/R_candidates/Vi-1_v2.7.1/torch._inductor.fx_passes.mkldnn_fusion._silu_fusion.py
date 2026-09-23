    def _silu_fusion(computation_call):
        return CallFunction(
            aten.mul, computation_call, CallFunction(aten.sigmoid, computation_call)
        )
