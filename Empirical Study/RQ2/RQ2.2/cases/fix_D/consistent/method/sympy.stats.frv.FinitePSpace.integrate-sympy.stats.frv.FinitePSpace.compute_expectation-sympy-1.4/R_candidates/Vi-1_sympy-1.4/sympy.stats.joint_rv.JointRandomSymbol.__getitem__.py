    def __getitem__(self, key):
        if isinstance(self.pspace, JointPSpace):
            if self.pspace.component_count <= key:
                raise ValueError("Index keys for %s can only up to %s." %
                    (self.name, self.pspace.component_count - 1))
            return Indexed(self, key)
