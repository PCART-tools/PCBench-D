    def get_col(self, alias, output_field=None):
        return super().get_col(alias, output_field or self.target_field)
