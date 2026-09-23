    def __init__(self, resources):
        self._routes = []
        for resource in resources:
            for route_obj in resource:
                self._routes.append(route_obj)
