@functools.lru_cache(None)
def get_dummy_aot_autograd_config():
    from torch._functorch._aot_autograd.schemas import AOTConfig

    return AOTConfig(
        fw_compiler=None,
        bw_compiler=None,
        inference_compiler=None,
        partition_fn=None,
        decompositions={},
        num_params_buffers=0,
        aot_id=0,
        keep_inference_input_mutations=False,
        dynamic_shapes=True,
        aot_autograd_arg_pos_to_source=None,
        is_export=False,
        no_tangents=False,
        enable_log=False,
    )
