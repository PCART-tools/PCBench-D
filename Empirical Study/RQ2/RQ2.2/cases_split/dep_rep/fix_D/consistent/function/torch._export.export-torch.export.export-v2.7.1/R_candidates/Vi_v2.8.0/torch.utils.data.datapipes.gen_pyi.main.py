def main() -> None:
    """
    # Inject file into template datapipe.pyi.in.

    TODO: The current implementation of this script only generates interfaces for built-in methods. To generate
          interface for user-defined DataPipes, consider changing `IterDataPipe.register_datapipe_as_function`.
    """
    iter_method_definitions = get_method_definitions(
        iterDP_file_path,
        iterDP_files_to_exclude,
        iterDP_deprecated_files,
        "IterDataPipe",
        iterDP_method_to_special_output_type,
    )

    map_method_definitions = get_method_definitions(
        mapDP_file_path,
        mapDP_files_to_exclude,
        mapDP_deprecated_files,
        "MapDataPipe",
        mapDP_method_to_special_output_type,
    )

    path = Path(__file__).absolute().parent
    fm = FileManager(install_dir=path, template_dir=path, dry_run=False)
    fm.write_with_template(
        "datapipe.pyi",
        "datapipe.pyi.in",
        lambda: {
            "IterDataPipeMethods": iter_method_definitions,
            "MapDataPipeMethods": map_method_definitions,
        },
    )
