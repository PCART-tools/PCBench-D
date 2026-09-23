def move_constructors_to_gpu(graph: fx.Graph) -> None:
    """
    Moves intermediary tensors which are constructed on the cpu to gpu when safe
    """
    ConstructorMoverPass(get_gpu_type())(graph)
