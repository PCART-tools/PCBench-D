        def __str__(self):
            # either just return the name of this TransformNode, or it's repr
            return self._shorthand_name or repr(self)
