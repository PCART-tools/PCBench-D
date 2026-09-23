def deserialize(
    artifact: SerializedArtifact,
    expected_opset_version: Optional[dict[str, int]] = None,
    *,
    _unsafe_skip_version_check=False,
) -> ep.ExportedProgram:
    assert isinstance(artifact.exported_program, bytes)
    exported_program_str = artifact.exported_program.decode("utf-8")
    exported_program_dict = json.loads(exported_program_str)
    serialized_exported_program = _dict_to_dataclass(ExportedProgram, exported_program_dict)
    return (
        ExportedProgramDeserializer(expected_opset_version)
        .deserialize(
            serialized_exported_program,
            artifact.state_dict,
            artifact.constants,
            artifact.example_inputs,
            _unsafe_skip_version_check=_unsafe_skip_version_check,
        )
    )
