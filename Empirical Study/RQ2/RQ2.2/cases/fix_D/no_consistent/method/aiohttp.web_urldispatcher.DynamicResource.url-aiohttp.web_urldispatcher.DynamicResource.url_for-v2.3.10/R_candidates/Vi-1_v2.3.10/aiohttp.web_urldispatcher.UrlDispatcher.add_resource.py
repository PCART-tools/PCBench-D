    def add_resource(self, path, *, name=None):
        if path and not path.startswith('/'):
            raise ValueError("path should be started with / or be empty")
        if not ('{' in path or '}' in path or ROUTE_RE.search(path)):
            url = URL(path)
            resource = PlainResource(url.raw_path, name=name)
            self.register_resource(resource)
            return resource
        resource = DynamicResource(path, name=name)
        self.register_resource(resource)
        return resource
