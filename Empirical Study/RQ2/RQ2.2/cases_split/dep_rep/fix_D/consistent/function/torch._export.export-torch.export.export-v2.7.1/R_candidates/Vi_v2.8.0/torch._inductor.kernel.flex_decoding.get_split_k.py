def get_split_k(B: int, H: int, Mk: int) -> int:
    num_SM = torch.cuda.get_device_properties("cuda").multi_processor_count
    bh = max(B * H, 1)  # NOTE: Handle B*h=0 case
    assert isinstance(bh, (int, sympy.Integer)), "B and H must be concrete integers"
    split_k = num_SM // bh * 2  # Each SM should at least get one block.
    # TODO: workload evening at runtime for splits fully masked out.
    # Before we have runtime workload evening, assign 2 splits per SM.
    split_k = max(split_k, 1)

    return split_k
