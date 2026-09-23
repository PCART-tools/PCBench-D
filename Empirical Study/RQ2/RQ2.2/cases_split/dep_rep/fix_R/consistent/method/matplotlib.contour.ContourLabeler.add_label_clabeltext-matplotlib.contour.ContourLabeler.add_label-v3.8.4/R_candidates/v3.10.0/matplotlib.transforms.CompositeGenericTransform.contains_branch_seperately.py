    def contains_branch_seperately(self, other_transform):
        # docstring inherited
        if self.output_dims != 2:
            raise ValueError('contains_branch_seperately only supports '
                             'transforms with 2 output dimensions')
        if self == other_transform:
            return (True, True)
        return self._b.contains_branch_seperately(other_transform)
