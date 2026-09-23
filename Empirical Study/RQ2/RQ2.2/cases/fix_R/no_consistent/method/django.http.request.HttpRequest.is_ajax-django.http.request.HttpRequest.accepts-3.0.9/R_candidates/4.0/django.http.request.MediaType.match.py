    def match(self, other):
        if self.is_all_types:
            return True
        other = MediaType(other)
        if self.main_type == other.main_type and self.sub_type in {'*', other.sub_type}:
            return True
        return False
