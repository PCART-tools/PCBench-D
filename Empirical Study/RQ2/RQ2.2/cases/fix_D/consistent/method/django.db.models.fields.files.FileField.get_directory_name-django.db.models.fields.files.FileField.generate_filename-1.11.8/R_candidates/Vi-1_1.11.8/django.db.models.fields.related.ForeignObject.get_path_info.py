    def get_path_info(self):
        """
        Get path from this field to the related model.
        """
        opts = self.remote_field.model._meta
        from_opts = self.model._meta
        return [PathInfo(from_opts, opts, self.foreign_related_fields, self, False, True)]
