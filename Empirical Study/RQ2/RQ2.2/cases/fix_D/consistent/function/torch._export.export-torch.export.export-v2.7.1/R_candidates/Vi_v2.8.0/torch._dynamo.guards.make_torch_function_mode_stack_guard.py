def make_torch_function_mode_stack_guard(initial_stack):
    types = [type(x) for x in initial_stack]

    def check_torch_function_mode_stack():
        cur_stack = get_torch_function_mode_stack()

        if len(cur_stack) != len(types):
            return False

        for ty, mode in zip(types, cur_stack):
            if ty != type(mode):
                return False

        return True

    return check_torch_function_mode_stack
