def set_kernel_post_grad_provenance_tracing(
    node_schedule: Sequence[BaseSchedulerNode], kernel_name: str
) -> None:
    from .codegen.simd_kernel_features import DisableReduction, EnableReduction
    from .virtualized import V

    for node in node_schedule:
        if node not in (EnableReduction, DisableReduction):
            if node.node is not None:
                V.debug._inductor_triton_kernel_to_post_grad_node_info[kernel_name] = [
                    origin.name
                    for origin in node.node.origins  # type: ignore[attr-defined]
                ]
