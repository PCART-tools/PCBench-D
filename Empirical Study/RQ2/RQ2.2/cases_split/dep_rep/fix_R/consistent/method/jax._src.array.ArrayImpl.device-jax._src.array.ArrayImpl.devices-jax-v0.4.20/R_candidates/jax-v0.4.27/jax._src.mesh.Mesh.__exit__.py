  def __exit__(self, exc_type, exc_value, traceback):
    thread_resources.stack.pop()
    thread_resources.env = thread_resources.stack[-1]
    jax_config.update_thread_local_jit_state(
        mesh_context_manager=tuple(t.physical_mesh for t in thread_resources.stack
                                   if not t.physical_mesh.empty))
    return False
