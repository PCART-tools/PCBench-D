    def set_paths(self, patches):
        paths = [p.get_transform().transform_path(p.get_path())
                 for p in patches]
        self._paths = paths
