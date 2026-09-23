    def register_route(self, route):
        assert isinstance(route, ResourceRoute), \
            'Instance of Route class is required, got {!r}'.format(route)
        self._routes.append(route)
