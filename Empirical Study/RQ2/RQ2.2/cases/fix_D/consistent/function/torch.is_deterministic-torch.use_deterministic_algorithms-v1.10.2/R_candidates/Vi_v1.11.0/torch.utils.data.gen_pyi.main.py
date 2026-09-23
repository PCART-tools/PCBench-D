def main() -> None:
    """
    # Inject file into template dataset.pyi.in
    TODO: The current implementation of this script only generates interfaces for built-in methods. To generate
          interface for user-defined DataPipes, consider changing `IterDataPipe.register_datapipe_as_function`.
    """

    iterDP_file_path: str = "datapipes/iter"
    iterDP_files_to_exclude: Set[str] = {"__init__.py", "utils.py"}
    iterDP_deprecated_files: Set[str] = set()
    iterDP_method_to_special_output_type: Dict[str, str] = {"demux": "List[IterDataPipe]", "fork": "List[IterDataPipe]"}

    iter_method_definitions = get_method_definitions(iterDP_file_path, iterDP_files_to_exclude, iterDP_deprecated_files,
                                                     "IterDataPipe", iterDP_method_to_special_output_type)
    mapDP_file_path: str = "datapipes/map"
    mapDP_files_to_exclude: Set[str] = {"__init__.py", "utils.py"}
    mapDP_deprecated_files: Set[str] = set()
    mapDP_method_to_special_output_type: Dict[str, str] = {}

    map_method_definitions = get_method_definitions(mapDP_file_path, mapDP_files_to_exclude, mapDP_deprecated_files,
                                                    "MapDataPipe", mapDP_method_to_special_output_type)

    fm = FileManager(install_dir='.', template_dir='.', dry_run=False)
    fm.write_with_template(filename="dataset.pyi",
                           template_fn="dataset.pyi.in",
                           env_callable=lambda: {'IterDataPipeMethods': iter_method_definitions,
                                                 'MapDataPipeMethods': map_method_definitions})
