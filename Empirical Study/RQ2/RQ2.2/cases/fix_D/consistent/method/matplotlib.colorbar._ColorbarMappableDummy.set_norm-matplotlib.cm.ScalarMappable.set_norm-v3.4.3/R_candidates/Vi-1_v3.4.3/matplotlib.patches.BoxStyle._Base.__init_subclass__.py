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
