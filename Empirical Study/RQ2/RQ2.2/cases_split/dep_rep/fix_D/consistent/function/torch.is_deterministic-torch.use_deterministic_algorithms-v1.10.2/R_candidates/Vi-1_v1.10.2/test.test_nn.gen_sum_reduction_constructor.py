        def gen_sum_reduction_constructor(constructor):
            def sum_reduction_constructor(*args, **kwargs):
                cons = constructor(*args, reduction='sum', **kwargs)
                return cons
            sum_reduction_constructor.__name__ = constructor.__name__
            return sum_reduction_constructor
