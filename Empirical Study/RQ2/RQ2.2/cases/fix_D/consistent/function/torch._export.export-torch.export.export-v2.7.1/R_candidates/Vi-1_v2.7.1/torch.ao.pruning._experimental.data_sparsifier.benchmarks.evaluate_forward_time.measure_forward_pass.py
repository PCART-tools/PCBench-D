def measure_forward_pass(sparse_model_metadata, device, sparse_dlrm, **batch):
    """Measures and tracks the forward pass of the model for all the sparsity levels, block shapes and norms
    available in sparse_model_metadata file.
    If sparse_dlrm=True, then the SparseDLRM model is loaded, otherwise the standard one is.
    """
    time_taken_dict: dict[str, list] = {
        "norm": [],
        "sparse_block_shape": [],
        "sparsity_level": [],
        "time_taken": [],
    }

    metadata = pd.read_csv(sparse_model_metadata)

    for _, row in metadata.iterrows():
        norm, sbs, sl = row["norm"], row["sparse_block_shape"], row["sparsity_level"]
        model_path = row["path"]
        model = fetch_model(model_path, device, sparse_dlrm=sparse_dlrm)
        time_taken = run_forward(model, **batch)
        out_str = f"{norm}_{sbs}_{sl}={time_taken}"
        print(out_str)
        time_taken_dict["norm"].append(norm)
        time_taken_dict["sparse_block_shape"].append(sbs)
        time_taken_dict["sparsity_level"].append(sl)
        time_taken_dict["time_taken"].append(time_taken)

    time_df = pd.DataFrame(time_taken_dict)

    if sparse_dlrm:
        time_df["dlrm_type"] = "with_torch_sparse"
    else:
        time_df["dlrm_type"] = "without_torch_sparse"

    return time_df
