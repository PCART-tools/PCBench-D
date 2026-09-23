def restore_vmap(func, in_dims, batch_size, randomness):
    def inner(*args, **kwargs):
        with vmap_increment_nesting(batch_size, randomness) as vmap_level:
            batched_inputs = wrap_batched(args, in_dims, vmap_level)
            batched_outputs = func(*batched_inputs, **kwargs)
            return unwrap_batched(batched_outputs, vmap_level)

    return inner
