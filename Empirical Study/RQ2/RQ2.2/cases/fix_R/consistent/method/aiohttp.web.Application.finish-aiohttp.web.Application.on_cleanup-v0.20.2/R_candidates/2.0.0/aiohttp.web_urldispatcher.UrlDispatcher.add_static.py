    def add_static(self, prefix, path, *, name=None, expect_handler=None,
                   chunk_size=256*1024, response_factory=StreamResponse,
                   show_index=False, follow_symlinks=False):
        """Add static files view.

        prefix - url prefix
        path - folder with files

        """
        # TODO: implement via PrefixedResource, not ResourceAdapter
        assert prefix.startswith('/')
        if prefix.endswith('/'):
            prefix = prefix[:-1]
        resource = StaticResource(prefix, path,
                                  name=name,
                                  expect_handler=expect_handler,
                                  chunk_size=chunk_size,
                                  response_factory=response_factory,
                                  show_index=show_index,
                                  follow_symlinks=follow_symlinks)
        self.register_resource(resource)
        return resource
