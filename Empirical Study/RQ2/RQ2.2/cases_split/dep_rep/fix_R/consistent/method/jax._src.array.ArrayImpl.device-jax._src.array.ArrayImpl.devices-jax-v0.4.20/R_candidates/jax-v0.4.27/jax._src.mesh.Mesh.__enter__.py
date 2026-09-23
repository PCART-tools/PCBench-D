  def __enter__(self):
    new_env = thread_resources.stack[-1].with_mesh(self)
    thread_resources.stack.append(new_env)
    thread_resources.env = new_env
    jax_config.update_thread_local_jit_state(
        mesh_context_manager=tuple(t.physical_mesh for t in thread_resources.stack
                                   if not t.physical_mesh.empty))
    return self
