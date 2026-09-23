    def __repr__(self):
        info = []
        for name, value in sorted(self.kwargs.items()):
            info.append(", {}={!r}".format(name, value))
        return ("<RouteDef {method} {path} -> {handler.__name__!r}"
                "{info}>".format(method=self.method, path=self.path,
                                 handler=self.handler, info=''.join(info)))
