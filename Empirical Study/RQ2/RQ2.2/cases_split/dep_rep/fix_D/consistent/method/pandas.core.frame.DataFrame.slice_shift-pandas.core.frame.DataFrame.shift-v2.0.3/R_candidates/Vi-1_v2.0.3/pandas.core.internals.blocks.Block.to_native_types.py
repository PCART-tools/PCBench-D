    @final
    def to_native_types(self, na_rep: str = "nan", quoting=None, **kwargs) -> Block:
        """convert to our native types format"""
        result = to_native_types(self.values, na_rep=na_rep, quoting=quoting, **kwargs)
        return self.make_block(result)
