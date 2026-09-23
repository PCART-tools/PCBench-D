    def __init__(
        self,
        lut: bytearray | None = None,
        op_name: str | None = None,
        patterns: list[str] | None = None,
    ) -> None:
        """Create a binary morphological operator"""
        self.lut = lut
        if op_name is not None:
            self.lut = LutBuilder(op_name=op_name).build_lut()
        elif patterns is not None:
            self.lut = LutBuilder(patterns=patterns).build_lut()
