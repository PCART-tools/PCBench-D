    def replace_regex(self, **kwargs):
        return self.apply("_replace_regex", **kwargs, using_cow=using_copy_on_write())
