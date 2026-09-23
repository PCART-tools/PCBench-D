def main():
    world_size = 2
    epochs = 120

    # resnet50 model facts:
    # total_param_count = 161
    # total_elements = 25557032 ~= 24.37M
    # param_max_elements = 2359296 ~= 2.25M
    # Try different bucket sizes.
    buffer_size_in_mbs = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
    print("buffer_size_in_mbs: " + str(buffer_size_in_mbs))
    for buffer_size_in_M in buffer_size_in_mbs:
        print("\n\n=== NEW EXPERIMENT: buffer_size={}M, {} epochs, world_size={} ===".format(
            buffer_size_in_M, epochs, world_size))
        options = [
            DDPOption.DDP_CPP_CORE,
            DDPOption.PYTHON_DDP_ASYNC_REDUCTION,
            DDPOption.PYTHON_DDP_SYNC_REDUCTION
        ]
        for option in options:
            print("Measuring option: {} ... ".format(option))
            mp.spawn(run_ddp,
                     args=(world_size, epochs, option, buffer_size_in_M),
                     nprocs=world_size,
                     join=True)

    print("\n Generating summaries ... ")
    buffer_size_to_metrics = load_detailed_metrics(data_dir="./tmp", ext="ddpraw")
    print_summary(buffer_size_to_metrics)
