def set_kernel_post_grad_provenance_tracing(
    node_schedule: Union[Sequence[BaseSchedulerNode], ExternKernelOut],
    kernel_name: str,
    is_extern: bool = False,
) -> None:
    from .codegen.simd_kernel_features import DisableReduction, EnableReduction
    from .ir import ExternKernelOut
    from .virtualized import V

    if is_extern:
        assert isinstance(node_schedule, ExternKernelOut)
        curr_node_info = (
            V.debug._inductor_triton_kernel_to_post_grad_node_info.setdefault(
                kernel_name, []
            )
        )
        curr_node_info.extend(
            origin.name
            for origin in node_schedule.origins
            if origin.name not in curr_node_info
        )
    else:
        assert isinstance(node_schedule, list)
        for snode in node_schedule:
            if snode not in (EnableReduction, DisableReduction):
                if snode.node is not None:
                    curr_node_info = V.debug._inductor_triton_kernel_to_post_grad_node_info.setdefault(
                        kernel_name, []
                    )
                    curr_node_info.extend(
                        origin.name
                        for origin in snode.node.origins
                        if origin.name not in curr_node_info
                    )
