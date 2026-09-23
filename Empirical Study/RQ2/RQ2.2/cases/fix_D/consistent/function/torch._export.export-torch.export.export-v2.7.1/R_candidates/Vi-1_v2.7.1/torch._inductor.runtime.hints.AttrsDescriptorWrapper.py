        def AttrsDescriptorWrapper(
            divisible_by_16=None,
            equal_to_1=None,
        ):
            return {(x,): [["tt.divisibility", 16]] for x in divisible_by_16}
