def gen_differentiable_outputs(fn: NativeFunctionWithDifferentiabilityInfo) -> List[DifferentiableOutput]:
    f = fn.func
    info = fn.info
    outputs: List[DifferentiableOutput] = [
        DifferentiableOutput(name=name, type=ret.type, cpp_type=cpp.return_type(ret).cpp_type())
        for name, ret in zip(cpp.return_names(f), f.func.returns)]
    output_differentiability = info.output_differentiability if info else None
    if output_differentiability is not None:
        differentiable_outputs: List[DifferentiableOutput] = []
        if False in output_differentiability and f.func.kind() == SchemaKind.inplace:
            raise RuntimeError("output_differentiability=False for inplace operation (version_counter won't get updated)")
        for differentiable, output in zip(output_differentiability, outputs):
            if differentiable:
                differentiable_outputs.append(output)
        return differentiable_outputs
    candidate_differentiable_outputs = list(filter(lambda r: is_differentiable(r.name, r.type, info), outputs))
    if uses_single_grad(info):
        return candidate_differentiable_outputs[:1]
    else:
        return candidate_differentiable_outputs
