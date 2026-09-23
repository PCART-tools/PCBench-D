    def freeze(self):
        super().freeze()
        for resource in self._resources:
            resource.freeze()
