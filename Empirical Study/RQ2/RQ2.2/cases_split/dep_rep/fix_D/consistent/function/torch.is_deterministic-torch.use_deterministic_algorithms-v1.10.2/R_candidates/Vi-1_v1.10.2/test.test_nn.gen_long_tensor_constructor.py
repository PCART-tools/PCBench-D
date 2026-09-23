        def gen_long_tensor_constructor(constructor):
            def long_tensor_constructor(*args, **kwargs):
                cons = constructor(*args, **kwargs)
                cons._apply(apply_to_cons)
                return cons
            long_tensor_constructor.__name__ = constructor.__name__
            return long_tensor_constructor
