def _load_exported_programs(
    archive_reader: PT2ArchiveReader,
    file_names: list[str],
    expected_opset_version: Optional[dict[str, int]],
) -> dict[str, ExportedProgram]:
    exported_program_files = [
        file for file in file_names if file.startswith(MODELS_DIR)
    ]
    exported_programs = {}
    for file in exported_program_files:
        prefix, suffix = MODELS_FILENAME_FORMAT.split(
            "{}"
        )  # split "models/{}.json" into "models/" and "json"
        model_name = file[
            len(prefix) : -len(suffix)
        ]  # given "models/foo.json" we can now get "foo"

        weights_file = f"{WEIGHTS_DIR}{model_name}.pt"
        constants_file = f"{CONSTANTS_DIR}{model_name}.pt"
        sample_inputs_file = SAMPLE_INPUTS_FILENAME_FORMAT.format(model_name)

        serialized_exported_program = archive_reader.read_bytes(file)
        serialized_weights = archive_reader.read_bytes(weights_file)
        serialized_constants = archive_reader.read_bytes(constants_file)
        serialized_sample_inputs = archive_reader.read_bytes(sample_inputs_file)

        artifact: SerializedArtifact = SerializedArtifact(
            serialized_exported_program,
            serialized_weights,
            serialized_constants,
            serialized_sample_inputs,
        )

        # Deserialize ExportedProgram
        ep = deserialize(artifact, expected_opset_version)
        exported_programs[model_name] = ep

    return exported_programs
