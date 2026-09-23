def _postprocess_serialized_shapes(
    dynamic_shapes: Union[dict[str, Any], tuple[Any], list[Any], None],
    dims: dict[str, dict[str, Union[int, list[str], None]]],
    to_dict: Optional[bool] = False,
) -> Union[DynamicShapesSpec, dict[str, Any]]:
    """
    Sorts dims and dumps to dictionary format.
    """
    from torch.utils._sympy.numbers import int_oo

    dims = {
        k: RootDim(
            min=v["min"],  # type: ignore[arg-type]
            max=None if v["max"] is int_oo else v["max"],  # type: ignore[arg-type]
            derived=sorted(v["derived"]),  # type: ignore[arg-type]
        )
        for k, v in sorted(dims.items())
    }
    spec = DynamicShapesSpec(dynamic_shapes=dynamic_shapes, dims=dims)
    if to_dict:
        return _dataclass_to_dict(spec)
    else:
        return spec
