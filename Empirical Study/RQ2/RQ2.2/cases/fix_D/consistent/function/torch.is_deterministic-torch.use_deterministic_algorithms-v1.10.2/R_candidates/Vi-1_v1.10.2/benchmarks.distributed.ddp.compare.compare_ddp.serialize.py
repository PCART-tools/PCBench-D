def serialize(buffer_size_in_M, ddp_option, rank, metrics,
              data_dir="./tmp", ext="ddpraw"):
    if not os.path.exists(data_dir):
        print(f'{data_dir} not exist, mkdir {data_dir}')
        os.mkdir(data_dir)
    file_name = "buffer_size_{}M_rank{}_{}.{}".format(
        buffer_size_in_M, rank, ddp_option, ext)
    file_path = os.path.join(data_dir, file_name)
    print("Writing metrics to file: '{}'".format(file_path))
    data = LatencyData(buffer_size_in_M, ddp_option, rank, metrics)
    with open(file_path, "wb") as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
    print(f"Wrote metrics to '{file_path}''")
