    def get_reverse_path_info(self):
        """
        Get path from the related model to this field's model.
        """
        opts = self.model._meta
        from_opts = self.remote_field.model._meta
        pathinfos = [PathInfo(from_opts, opts, (opts.pk,), self.remote_field, not self.unique, False)]
        return pathinfos
