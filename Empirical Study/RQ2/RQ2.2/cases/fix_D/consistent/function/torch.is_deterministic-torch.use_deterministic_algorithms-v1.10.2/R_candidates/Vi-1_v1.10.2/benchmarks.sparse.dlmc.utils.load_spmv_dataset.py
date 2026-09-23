def load_spmv_dataset(dataset_path, hidden_size, sparsity, device, n_limit=math.inf):
    """load_spmv_dataset loads a DLMC dataset for a sparse matrix-vector multiplication (SPMV) performance test.
    Args:
        dataset_path:
            path of the dataset from DLMC collection.
        hidden_size
            This value allows tensors of varying sizes.
        sparsity:
            This value allows tensors of varying sparsities.
        device:
            Whether to place the Tensor on a GPU or CPU.
        n_limit:
            This value allows a dataset with some limit size.
    """
    current_folder_path = f"{dataset_path}/{sparsity}"
    path = Path(current_folder_path)
    files = path.glob('**/*.smtx')
    print(dataset_path, hidden_size, sparsity)
    index = 0
    x_files, y_files = [], []
    for f in files:
        if index >= n_limit:
            break
        print('.', end='')
        size, nnz = read_matrix_params(f.as_posix())
        if size[1] == hidden_size:
            x_files.append(f.as_posix())
        if size[0] == hidden_size:
            y_files.append(f.as_posix())
        index += 1
    print()

    for fx, fy in zip(x_files, y_files):
        x = load_sparse_matrix(fx, device)
        y = gen_vector(fy, device)
        yield (x, y)
