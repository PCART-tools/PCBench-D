def get_inputs(input_data_path):
    """
    Return a random input for the given inputs meta generated from _save_fx_default.
    """
    inputs = []
    with open(input_data_path, "rb") as f:
        inputs_meta = pickle.load(f)
        inputs = []
        for meta in inputs_meta:
            if len(meta) == 1:
                type = meta
                input = type(random.rand())
            else:
                type, shape, _stride, dtype, device = meta
                if dtype in {
                    torch.int,
                    torch.int32,
                    torch.int64,
                    torch.bool,
                    torch.int,
                    torch.uint8,
                    int,
                    float,
                }:
                    input = torch.randint(0, 1, shape, dtype=dtype, device=device)
                else:
                    input = torch.rand(shape, dtype=dtype, device=device)
            inputs.append(input)
    return inputs
