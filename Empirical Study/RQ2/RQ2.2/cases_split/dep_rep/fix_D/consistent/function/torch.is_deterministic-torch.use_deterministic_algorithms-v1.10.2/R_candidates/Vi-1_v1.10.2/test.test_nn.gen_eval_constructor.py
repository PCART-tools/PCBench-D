        def gen_eval_constructor(constructor):
            def eval_constructor(*args, **kwargs):
                cons = constructor(*args, **kwargs)
                cons.training = False
                return cons
            eval_constructor.__name__ = constructor.__name__
            return eval_constructor
