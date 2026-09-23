def run_example(world_size: int, rank: int, example_name: str) -> None:
    # set manual seed
    # intializing class with all of the functions
    instantiated_example = CommDebugModeExample(world_size, rank)
    # dict that stores example code function names
    name_to_example_code: dict[str, Callable[[], None]] = {
        "MLP_distributed_sharding_display": instantiated_example.example_MLP_distributed_sharding_display,
        "MLPStacked_distributed_sharding_display": instantiated_example.example_MLPStacked_distributed_sharding_display,
        "MLP_module_tracing": instantiated_example.example_MLP_module_tracing,
        "transformer_module_tracing": instantiated_example.example_transformer_module_tracing,
        "MLP_operation_tracing": instantiated_example.example_MLP_operation_tracing,
        "transformer_operation_tracing": instantiated_example.example_transformer_operation_tracing,
        "MLP_json_dump": instantiated_example.example_MLP_json_dump,
        "transformer_json_dump": instantiated_example.example_transformer_json_dump,
        "activation_checkpointing": instantiated_example.example_activation_checkpointing,
    }

    name_to_example_code[example_name]()
