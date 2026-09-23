    def add_routes(self, routes):
        """Append routes to route table.

        Parameter should be a sequence of RouteDef objects.
        """
        for route_obj in routes:
            route_obj.register(self)
