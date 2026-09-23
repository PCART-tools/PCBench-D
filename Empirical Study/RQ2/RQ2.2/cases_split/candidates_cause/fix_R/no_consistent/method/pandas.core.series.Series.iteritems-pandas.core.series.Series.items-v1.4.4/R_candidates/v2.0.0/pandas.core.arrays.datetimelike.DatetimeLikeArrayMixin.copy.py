    def copy(self: DatetimeLikeArrayT, order: str = "C") -> DatetimeLikeArrayT:
        # error: Unexpected keyword argument "order" for "copy"
        new_obj = super().copy(order=order)  # type: ignore[call-arg]
        new_obj._freq = self.freq
        return new_obj
