    @property
    def is_all_types(self):
        return self.main_type == '*' and self.sub_type == '*'
