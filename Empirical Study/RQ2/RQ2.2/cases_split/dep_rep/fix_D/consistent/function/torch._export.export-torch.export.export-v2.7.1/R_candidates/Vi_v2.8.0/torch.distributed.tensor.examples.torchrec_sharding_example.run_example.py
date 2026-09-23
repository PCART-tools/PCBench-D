def run_example(rank, world_size, example_name):
    # the dict that stores example code
    name_to_example_code = {
        "row-wise-even": run_torchrec_row_wise_even_sharding_example,
        "row-wise-uneven": run_torchrec_row_wise_uneven_sharding_example,
        "table-wise": run_torchrec_table_wise_sharding_example,
    }
    if example_name not in name_to_example_code:
        print(f"example for {example_name} does not exist!")
        return

    # the example to run
    example_func = name_to_example_code[example_name]

    # set manual seed
    torch.manual_seed(0)

    # run the example
    example_func(rank, world_size)
