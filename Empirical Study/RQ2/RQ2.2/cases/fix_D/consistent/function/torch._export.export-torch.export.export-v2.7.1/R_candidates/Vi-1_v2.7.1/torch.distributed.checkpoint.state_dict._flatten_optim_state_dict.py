def _flatten_optim_state_dict(state_dict: OptimizerStateType) -> dict[str, ValueType]:
    """
    This API flattens the optimizer state_dict to support optimizer resharding for
    MPMD, e.g., pipeline parallelism.

    Without the API, the original optimizer state_dict looks like:
    {
        "state": {
            "layer1.weight": {
                "step": 10, "exp_avg": SomeTensor, "exp_avg_sq": SomeTensor
            },
            "layer2.weight": {
                "step": 10, "exp_avg": SomeTensor, "exp_avg_sq": SomeTensor
            },
        },
        "param_group": [
            {
                "lr": 0.0,
                "betas": (0.9, 0.95), ...,
                "params": ["layer1.weight", "layer2.weight"]
            }
        ]
    }

    With this API, the optimizer state_dict looks like:
    {
        "state.layer1.weight.step": 10,
        "state.layer2.weight.step": 10,
        "state.layer1.weight.exp_avg": SomeTensor,
        "state.layer2.weight.exp_avg": SomeTensor,
        "state.layer1.weight.exp_avg_sq": SomeTensor,
        "state.layer2.weight.exp_avg_sq": SomeTensor,
        "param_group.layer1.weight.lr" : 0.1,
        "param_group.layer2.weight.lr" : 0.1,
        "param_group.layer1.weight.betas" : (0.9, 0.95),
        "param_group.layer2.weight.betas" : (0.9, 0.95),
    }

    Note that if any of the value is a container, like the betas in the example,
    this API won't flattent it.
    """

    def _raise_if_type_not_supported(v):
        if not isinstance(v, (torch.Tensor, int, float)):
            raise NotImplementedError(
                "Flattening optimizer state_dict only supports "
                "tensor, int, float states now. "
                f"Type is {type(v)}."
            )

    ret: dict[str, ValueType] = {}
    for fqn, state in cast(DictValueType, state_dict[_STATE]).items():
        for k, v in cast(DictValueType, state).items():
            _raise_if_type_not_supported(v)
            ret[f"{_STATE}.{fqn}.{k}"] = v

    for param_group in cast(ListDictValueType, state_dict[_PG]):
        fqns = param_group.pop(_PARAMS)
        for fqn in cast(list[str], fqns):
            for k, v in param_group.items():
                ret[f"{_PG}.{fqn}.{k}"] = v
    return ret
