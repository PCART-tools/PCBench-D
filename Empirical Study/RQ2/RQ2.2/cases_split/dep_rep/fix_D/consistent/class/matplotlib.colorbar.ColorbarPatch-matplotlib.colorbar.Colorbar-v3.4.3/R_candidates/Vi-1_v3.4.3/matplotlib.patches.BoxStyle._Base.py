    @_api.deprecated("3.4")
    class _Base:
        """
        Abstract base class for styling of `.FancyBboxPatch`.

        This class is not an artist itself.  The `__call__` method returns the
        `~matplotlib.path.Path` for outlining the fancy box. The actual drawing
        is handled in `.FancyBboxPatch`.

        Subclasses may only use parameters with default values in their
        ``__init__`` method because they must be able to be initialized
        without arguments.

        Subclasses must implement the `__call__` method. It receives the
        enclosing rectangle *x0, y0, width, height* as well as the
        *mutation_size*, which scales the outline properties such as padding.
        It returns the outline of the fancy box as `.path.Path`.
        """

        @_api.deprecated("3.4")
        def transmute(self, x0, y0, width, height, mutation_size):
            """Return the `~.path.Path` outlining the given rectangle."""
            return self(self, x0, y0, width, height, mutation_size, 1)

        # This can go away once the deprecation period elapses, leaving _Base
        # as a fully abstract base class just providing docstrings, no logic.
        def __init_subclass__(cls):
            transmute = _api.deprecate_method_override(
                __class__.transmute, cls, since="3.4")
            if transmute:
                cls.__call__ = transmute
                return

            __call__ = cls.__call__

            @_api.delete_parameter("3.4", "mutation_aspect")
            def call_wrapper(
                    self, x0, y0, width, height, mutation_size,
                    mutation_aspect=_api.deprecation._deprecated_parameter):
                if mutation_aspect is _api.deprecation._deprecated_parameter:
                    # Don't trigger deprecation warning internally.
                    return __call__(self, x0, y0, width, height, mutation_size)
                else:
                    # Squeeze the given height by the aspect_ratio.
                    y0, height = y0 / mutation_aspect, height / mutation_aspect
                    path = self(x0, y0, width, height, mutation_size,
                                mutation_aspect)
                    vertices, codes = path.vertices, path.codes
                    # Restore the height.
                    vertices[:, 1] = vertices[:, 1] * mutation_aspect
                    return Path(vertices, codes)

            cls.__call__ = call_wrapper

        def __call__(self, x0, y0, width, height, mutation_size):
            """
            Given the location and size of the box, return the path of
            the box around it.

            Parameters
            ----------
            x0, y0, width, height : float
                Location and size of the box.
            mutation_size : float
                A reference scale for the mutation.

            Returns
            -------
            `~matplotlib.path.Path`
            """
            raise NotImplementedError('Derived must override')
