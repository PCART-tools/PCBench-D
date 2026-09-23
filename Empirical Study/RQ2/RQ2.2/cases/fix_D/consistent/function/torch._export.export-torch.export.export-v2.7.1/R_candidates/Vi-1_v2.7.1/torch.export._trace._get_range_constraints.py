def _get_range_constraints(
    export_artifact: ExportArtifact, combined_args: dict[str, Any], dynamic_shapes
):
    gm: torch.fx.GraphModule = export_artifact.aten.gm
    export_graph_signature: ExportGraphSignature = export_artifact.aten.sig
    fake_mode: FakeTensorMode = export_artifact.fake_mode
    num_lifted = next(
        (
            i
            for i, s in enumerate(export_graph_signature.input_specs)
            if s.kind == InputKind.USER_INPUT
        ),
        len(export_graph_signature.input_specs),
    )
    range_constraints = make_constraints(
        fake_mode,
        gm,
        combined_args,
        dynamic_shapes,
        num_lifted,
    )
    return range_constraints
