    def add_routes(self, routes):
        """Append routes to route table.

        Parameter should be a sequence of RouteDef objects.
        """
        # TODO: add_table maybe?
        for route in routes:
            route.register(self)
