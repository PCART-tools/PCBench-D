    def _to_fp16(input_call):
        return CallFunction(
            prims.convert_element_type.default,
            input_call,
            KeywordArg("to_fp16"),
            _users=1,
        )
