    def __hash__(self):
        l = (tuple(self.get_family()),
             self.get_slant(),
             self.get_variant(),
             self.get_weight(),
             self.get_stretch(),
             self.get_size(),
             self.get_file(),
             self.get_math_fontfamily())
        return hash(l)
