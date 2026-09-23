def pt_repeat_n_times(niters):
    for _ in range(niters):
        for input_tensor, repeat in zip(input_tensors, repeats):
            pt_repeat(input_tensor, repeat)
