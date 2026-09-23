def serialize(
    exported_program: ep.ExportedProgram,
    opset_version: Optional[dict[str, int]] = None,
    pickle_protocol: int = DEFAULT_PICKLE_PROTOCOL,
) -> SerializedArtifact:
    with _enable_graph_inputs_of_type_nn_module(exported_program.example_inputs):
        serialized_program = ExportedProgramSerializer(opset_version, pickle_protocol).serialize(
            exported_program
        )
    assert isinstance(serialized_program.exported_program, ExportedProgram)

    json_bytes = _to_json_bytes(serialized_program.exported_program)
    artifact = SerializedArtifact(
        json_bytes,
        serialized_program.state_dict,
        serialized_program.constants,
        serialized_program.example_inputs
    )
    return artifact
