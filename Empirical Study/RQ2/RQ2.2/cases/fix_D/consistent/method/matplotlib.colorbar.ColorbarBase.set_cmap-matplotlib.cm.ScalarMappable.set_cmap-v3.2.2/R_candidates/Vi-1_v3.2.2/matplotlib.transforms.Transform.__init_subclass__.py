    def __init_subclass__(cls):
        # 1d transforms are always separable; we assume higher-dimensional ones
        # are not but subclasses can also directly set is_separable -- this is
        # verified by checking whether "is_separable" appears more than once in
        # the class's MRO (it appears once in Transform).
        if (sum("is_separable" in vars(parent) for parent in cls.__mro__) == 1
                and cls.input_dims == cls.output_dims == 1):
            cls.is_separable = True
        # Transform.inverted raises NotImplementedError; we assume that if this
        # is overridden then the transform is invertible but subclass can also
        # directly set has_inverse.
        if (sum("has_inverse" in vars(parent) for parent in cls.__mro__) == 1
                and hasattr(cls, "inverted")
                and cls.inverted is not Transform.inverted):
            cls.has_inverse = True
