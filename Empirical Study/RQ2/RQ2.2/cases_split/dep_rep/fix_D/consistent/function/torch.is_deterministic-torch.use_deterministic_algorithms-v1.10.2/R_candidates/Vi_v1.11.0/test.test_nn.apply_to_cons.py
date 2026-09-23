        def apply_to_cons(t):
            if t.is_floating_point():
                if isinstance(t, Parameter):
                    return Parameter(double_equivalent_of_long_tensor(t.size()))
                elif isinstance(t, torch.Tensor):
                    return double_equivalent_of_long_tensor(t.size())
            else:
                return t
