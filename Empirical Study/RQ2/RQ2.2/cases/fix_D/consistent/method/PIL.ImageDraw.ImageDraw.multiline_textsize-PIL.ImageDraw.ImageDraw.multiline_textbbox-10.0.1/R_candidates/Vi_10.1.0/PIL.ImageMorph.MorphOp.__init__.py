    def __init__(self, lut=None, op_name=None, patterns=None):
        """Create a binary morphological operator"""
        self.lut = lut
        if op_name is not None:
            self.lut = LutBuilder(op_name=op_name).build_lut()
        elif patterns is not None:
            self.lut = LutBuilder(patterns=patterns).build_lut()
