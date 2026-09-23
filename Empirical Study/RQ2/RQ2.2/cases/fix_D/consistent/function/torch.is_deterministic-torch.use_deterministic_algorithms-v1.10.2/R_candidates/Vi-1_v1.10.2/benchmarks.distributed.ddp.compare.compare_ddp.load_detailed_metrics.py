def load_detailed_metrics(data_dir="./tmp", ext="ddpraw"):
    assert os.path.exists(data_dir)
    file_pattern = os.path.join(data_dir, f"*.{ext}")
    files = glob.glob(file_pattern)
    print("load_detailed_metrics found {} files".format(len(files)))
    buffer_size_to_metrics = OrderedDict()
    for file_path in files:
        with open(file_path, "rb") as f:
            data = pickle.load(f)
        # Add data to buffer_size_to_metrics
        buffer_size = data.buffer_size_in_M
        if buffer_size not in buffer_size_to_metrics:
            buffer_size_to_metrics[buffer_size] = {}
        metrics = buffer_size_to_metrics.get(buffer_size)
        assert metrics is not None
        metrics[data.ddp_option] = data.metrics
    return buffer_size_to_metrics
