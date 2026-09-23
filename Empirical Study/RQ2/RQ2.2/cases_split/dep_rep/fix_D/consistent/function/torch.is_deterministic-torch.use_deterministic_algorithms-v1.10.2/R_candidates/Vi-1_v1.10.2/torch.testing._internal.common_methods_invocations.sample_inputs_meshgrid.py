def sample_inputs_meshgrid(op_info: OpInfo, device: torch.device, dtype: torch.dtype,
                           requires_grad: bool,
                           *, variant: str) -> List[SampleInput]:
    if variant == 'variadic':
        def make_inputs(
                tensors: List[torch.Tensor]) -> Tuple[Union[torch.Tensor,
                                                            List[torch.Tensor]],
                                                      Tuple[torch.Tensor, ...]]:
            return tensors[0], tuple(tensors[1:])
    elif variant == 'list':
        def make_inputs(
                tensors: List[torch.Tensor]) -> Tuple[Union[torch.Tensor,
                                                            List[torch.Tensor]],
                                                      Tuple[torch.Tensor, ...]]:
            return tensors, ()
    else:
        raise ValueError(
            'Unsupported variant, must be one of {"variadic", "list"}. '
            f'Got "{variant}".')

    SCALAR = torch.Size([])
    VECTOR = torch.Size([3])
    test_cases: List[List[torch.Size]] = [
        [SCALAR],
        [VECTOR],
        [VECTOR, SCALAR],
        [VECTOR, SCALAR, VECTOR],
        [VECTOR, SCALAR, VECTOR, SCALAR],
    ]

    sample_inputs = []
    for shapes, indexing in itertools.product(test_cases, {'xy', 'ij'}):
        input, args = make_inputs(
            [make_tensor(shape, device, dtype, requires_grad=requires_grad)
             for shape in shapes])
        sample_inputs.append(SampleInput(input=input, args=args,
                                         kwargs=dict(indexing=indexing)))
    return sample_inputs
