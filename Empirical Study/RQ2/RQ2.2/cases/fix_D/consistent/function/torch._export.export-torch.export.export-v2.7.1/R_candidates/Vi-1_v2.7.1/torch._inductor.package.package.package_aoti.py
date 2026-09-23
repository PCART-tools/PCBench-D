def package_aoti(
    archive_file: FileLike,
    aoti_files: Union[list[str], dict[str, list[str]]],
) -> FileLike:
    """
    Saves the AOTInductor generated files to the PT2Archive format.

    Args:
        archive_file: The file name to save the package to.
        aoti_files: This can either be a singular path to a directory containing
        the AOTInductor files, or a dictionary mapping the model name to the
        path to its AOTInductor generated files.
    """
    if isinstance(aoti_files, list):
        aoti_files = {"model": aoti_files}

    assert isinstance(aoti_files, dict), (
        "Please pass a list of AOTI generated files to be packaged or "
        "a dictionary mapping model names to their list of AOTI generated "
        "files. You can get this list of files through calling "
        "`torch._inductor.aot_compile(..., options={aot_inductor.package=True})`"
    )
    assert (
        isinstance(archive_file, (io.IOBase, IO))
        and archive_file.writable()
        and archive_file.seekable()
    ) or (
        isinstance(archive_file, (str, os.PathLike))
        and os.fspath(archive_file).endswith(".pt2")
    ), (
        f"Expect archive file to be a file ending in .pt2, or is a buffer. Instead got {archive_file}"
    )

    # Save using the PT2 packaging format
    # (https://docs.google.com/document/d/1jLPp8MN8Whs0-VW9PmJ93Yg02W85tpujvHrTa1pc5x8/edit#heading=h.v2y2jgnwc56a)

    with PT2ArchiveWriter(archive_file) as archive_writer:
        for model_name, files in aoti_files.items():
            num_so_files = 0
            num_cpp_files = 0

            for file in files:
                if file == "":
                    continue

                if file.endswith(".so"):
                    num_so_files += 1
                    if num_so_files > 1:
                        raise RuntimeError(
                            f"Multiple .so files found in {files}. "
                            "You might need to clear your cache "
                            "directory before calling aoti_compile again."
                        )
                if file.endswith(".cpp"):
                    num_cpp_files += 1
                    if num_so_files > 1:
                        raise RuntimeError(
                            f"Multiple .cpp files found in {files}. "
                            "You might need to clear your cache "
                            "directory before calling aoti_compile again."
                        )

                filename = os.path.basename(file)
                if filename.startswith(CUSTOM_OBJ_FILENAME_PREFIX):
                    new_filepath = os.path.join(CONSTANTS_DIR, filename)
                else:
                    new_filepath = os.path.join(AOTINDUCTOR_DIR, model_name, filename)
                log.debug(
                    "Saving AOTI generated file %s to archive in %s", file, new_filepath
                )
                archive_writer.write_file(
                    str(new_filepath),
                    file,
                )

    if isinstance(archive_file, (io.IOBase, IO)):
        archive_file.seek(0)
    return archive_file
