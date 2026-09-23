def register_buffer_assignment_hook(mod, assigned_buffers):
    """
    Register a hook that intercepts buffer assignments.
    This is used to detect when a buffer is assigned to, and then we can
    map that buffer to the corresponding proxy node in the graph.
    """

    def _map_assigned_buffer_to_proxy(_mod, name, buffer):
        # We intercept buffer assignments on the root module through this hook.
        if _mod._buffers is mod._buffers:
            # either buffer is a functional tensor, which wraps a fake tensor
            if isinstance(buffer, FunctionalTensor):
                buffer = buffer.from_functional()
            # or buffer is a fake tensor
            assert isinstance(buffer, FakeTensor)
            # The fake tensor in turn is associated with a proxy node.
            proxy_mode = torch.fx.experimental.proxy_tensor.get_proxy_mode()
            assert proxy_mode is not None
            proxy = torch.fx.experimental.proxy_tensor.get_proxy_slot(
                buffer, proxy_mode.tracer
            ).proxy.node
            # We map the assigned buffer to this proxy node.
            assigned_buffers[name] = proxy.name
        return buffer

    return torch.nn.modules.module.register_module_buffer_registration_hook(
        _map_assigned_buffer_to_proxy
    )
