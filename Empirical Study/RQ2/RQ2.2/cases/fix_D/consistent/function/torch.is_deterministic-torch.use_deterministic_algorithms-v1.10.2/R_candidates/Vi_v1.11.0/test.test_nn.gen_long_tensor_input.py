        def gen_long_tensor_input(input_size):
            def input_func():
                return double_equivalent_of_long_tensor(input_size)
            return input_func
