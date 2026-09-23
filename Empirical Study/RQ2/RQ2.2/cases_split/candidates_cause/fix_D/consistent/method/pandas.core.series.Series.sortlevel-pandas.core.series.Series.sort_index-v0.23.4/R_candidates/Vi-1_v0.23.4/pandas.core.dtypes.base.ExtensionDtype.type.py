    @property
    def type(self):
        # type: () -> type
        """The scalar type for the array, e.g. ``int``

        It's expected ``ExtensionArray[item]`` returns an instance
        of ``ExtensionDtype.type`` for scalar ``item``.
        """
        raise AbstractMethodError(self)
