    def __call__(self, *args, **kwargs):
        # Detect where the actual inputs are
        if args is not None and len(args) > 0:
            if len(args) == 1:
                inputs = args[0]
            elif len(args) == 2 and {type(el) for el in args} == {str}:
                inputs = [{"question": args[0], "context": args[1]}]
            else:
                inputs = list(args)
        # Generic compatibility with sklearn and Keras
        # Batched data
        elif "X" in kwargs:
            inputs = kwargs["X"]
        elif "data" in kwargs:
            inputs = kwargs["data"]
        elif "question" in kwargs and "context" in kwargs:
            inputs = [{"question": kwargs["question"], "context": kwargs["context"]}]
        else:
            raise ValueError("Unknown arguments {}".format(kwargs))

        # Normalize inputs
        if isinstance(inputs, dict):
            inputs = [inputs]
        elif isinstance(inputs, Iterable):
            # Copy to avoid overriding arguments
            inputs = [i for i in inputs]
        else:
            raise ValueError("Invalid arguments {}".format(inputs))

        for i, item in enumerate(inputs):
            inputs[i] = self.normalize(item)

        return inputs
