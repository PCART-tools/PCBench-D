    def equals(self, other) -> bool:
        # override for significant performance improvement
        if self.dtype != other.dtype or self.shape != other.shape:
            return False
        return (self.values.view("i8") == other.values.view("i8")).all()
