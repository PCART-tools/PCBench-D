def _package_exported_programs(
    archive_writer: PT2ArchiveWriter,
    exported_programs: Optional[Union[ExportedProgram, dict[str, ExportedProgram]]],
    opset_version: Optional[dict[str, int]] = None,
    pickle_protocol: int = DEFAULT_PICKLE_PROTOCOL,
) -> None:
    if exported_programs is None:
        return

    if isinstance(exported_programs, ExportedProgram):
        exported_programs = {"model", exported_programs}  # type: ignore[assignment]

    assert isinstance(exported_programs, dict)

    for model_name, ep in exported_programs.items():
        artifact: SerializedArtifact = serialize(ep, opset_version, pickle_protocol)

        archive_writer.write_bytes(
            MODELS_FILENAME_FORMAT.format(model_name), artifact.exported_program
        )
        # TODO:Consider dedup this with the weights saved in package_aoti_files
        archive_writer.write_bytes(f"{WEIGHTS_DIR}{model_name}.pt", artifact.state_dict)
        archive_writer.write_bytes(
            f"{CONSTANTS_DIR}{model_name}.pt", artifact.constants
        )
        archive_writer.write_bytes(
            SAMPLE_INPUTS_FILENAME_FORMAT.format(model_name),
            artifact.example_inputs,
        )
