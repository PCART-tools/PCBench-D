def aot_eager(
    gm,
    fake_tensor_inputs,
    fw_compiler=None,
    bw_compiler=None,
    **kwargs,
):
    return aot_autograd(
        fw_compiler=fw_compiler or boxed_nop,
        bw_compiler=bw_compiler or boxed_nop,
        partition_fn=min_cut_rematerialization_partition,
        keep_inference_input_mutations=True,
    )(gm, fake_tensor_inputs, **kwargs)
