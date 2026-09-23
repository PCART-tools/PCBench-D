@register_op_strategy(aten._grouped_mm.default)
def grouped_mm_strategy(op_schema: OpSchema) -> OpStrategy:
    mesh = op_schema.get_mesh_from_args()

    mat1_strategy = op_schema.args_schema[0]
    assert isinstance(mat1_strategy, OpStrategy)
    mat2_strategy = op_schema.args_schema[1]
    assert isinstance(mat2_strategy, OpStrategy)
    if len(op_schema.args_schema) > 3:
        bias_strategy = op_schema.args_schema[3]
        assert bias_strategy is None, "grouped_mm doesn't support bias yet"

    single_mesh_dim_strategies = []

    offs_placement = None
    if len(op_schema.args_schema) > 2 and op_schema.args_schema[2] is not None:
        offs_placement = Replicate()  # offs should always be replicated

    all_replicate: PlacementList = [
        Replicate(),
        Replicate(),  # mat1
        Replicate(),  # mat2
        offs_placement,  # offs
        None,  # bias
    ]
    partial_replicate: PlacementList = [
        Partial(),
        Partial(),  # mat1
        Replicate(),  # mat2
        offs_placement,  # offs
        None,  # bias
    ]
    replicate_partial: PlacementList = [
        Partial(),
        Replicate(),  # mat1
        Partial(),  # mat2
        offs_placement,  # offs
        None,  # bias
    ]
    single_mesh_dim_strategies = [all_replicate, partial_replicate, replicate_partial]

    if mat1_strategy.ndim == 2 and mat2_strategy.ndim == 3:
        # rowwise_replicate for 2dx3d not supported
        replicate_colwise_2x3: PlacementList = [
            Shard(1),
            Replicate(),  # mat1
            Shard(2),  # mat2
            offs_placement,  # offs
            None,  # bias
        ]
        colwise_rowwise_2x3: PlacementList = [
            Partial(),
            Shard(1),  # mat1
            Shard(1),  # mat2
            offs_placement,  # offs
            None,  # bias
        ]
        single_mesh_dim_strategies.extend([replicate_colwise_2x3, colwise_rowwise_2x3])

    if mat1_strategy.ndim == 3 and mat2_strategy.ndim == 2:
        # replicate_colwise for 3dx2d not supported
        colwise_rowwise_3x2: PlacementList = [
            Partial(),
            Shard(2),  # mat1
            Shard(0),  # mat2
            offs_placement,  # offs
            None,  # bias
        ]
        rowwise_replicate_3x2: PlacementList = [
            Shard(0),
            Shard(1),  # mat1
            Replicate(),  # mat2
            offs_placement,  # offs
            None,  # bias
        ]
        single_mesh_dim_strategies.extend([colwise_rowwise_3x2, rowwise_replicate_3x2])

    if mat1_strategy.ndim == 2 and mat2_strategy.ndim == 2:
        # colwise_rowwise for 2dx2d not supported
        replicate_colwise_2x2: PlacementList = [
            Shard(2),
            Replicate(),  # mat1
            Shard(1),  # mat2
            offs_placement,  # offs
            None,  # bias
        ]
        rowwise_replicate_2x2: PlacementList = [
            Shard(1),
            Shard(0),  # mat1
            Replicate(),  # mat2
            offs_placement,  # offs
            None,  # bias
        ]
        single_mesh_dim_strategies.extend(
            [replicate_colwise_2x2, rowwise_replicate_2x2]
        )

    if mat1_strategy.ndim == 3 and mat2_strategy.ndim == 3:
        replicate_colwise_3x3: PlacementList = [
            Shard(2),
            Replicate(),  # mat1
            Shard(2),  # mat2
            offs_placement,  # offs
            None,  # bias
        ]
        rowwise_replicate_3x3: PlacementList = [
            Shard(1),
            Shard(1),  # mat1
            Replicate(),  # mat2
            offs_placement,  # offs
            None,  # bias
        ]
        colwise_rowwise_3x3: PlacementList = [
            Partial(),
            Shard(2),  # mat1
            Shard(1),  # mat2
            offs_placement,  # offs
            None,  # bias
        ]
        batch_dim_sharding: PlacementList = [
            Shard(0),
            Shard(0),  # mat1
            Shard(0),  # mat2
            offs_placement,  # offs
            None,  # bias
        ]
        single_mesh_dim_strategies.extend(
            [
                replicate_colwise_3x3,
                rowwise_replicate_3x3,
                colwise_rowwise_3x3,
                batch_dim_sharding,
            ]
        )

    return expand_to_full_mesh_op_strategy(
        mesh, op_schema, single_mesh_dim_strategies, input_index=1
    )
