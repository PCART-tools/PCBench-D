    def add_static(self, prefix, path, *, name=None, expect_handler=None,
                   chunk_size=256 * 1024,
                   show_index=False, follow_symlinks=False,
                   append_version=False):
        """Add static files view.

        prefix - url prefix
        path - folder with files

        """
        assert prefix.startswith('/')
        if prefix.endswith('/'):
            prefix = prefix[:-1]
        resource = StaticResource(prefix, path,
                                  name=name,
                                  expect_handler=expect_handler,
                                  chunk_size=chunk_size,
                                  show_index=show_index,
                                  follow_symlinks=follow_symlinks,
                                  append_version=append_version)
        self.register_resource(resource)
        return resource
