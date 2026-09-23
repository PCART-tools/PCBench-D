def _get_sym_node_fn(name):
    def fn(self):
        return getattr(self, f"_sym_{name}")()

    return fn
