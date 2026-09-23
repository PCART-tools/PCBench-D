def html_oriented_report() -> None:
    # use lcov to generate the coverage report
    build_folder = os.path.join(get_pytorch_folder(), "build")
    coverage_info_file = os.path.join(SUMMARY_FOLDER_DIR, "coverage.info")
    # generage coverage report -- coverage.info in build folder
    subprocess.check_call(
        [
            "lcov",
            "--capture",
            "--directory",
            build_folder,
            "--output-file",
            coverage_info_file,
        ]
    )
    # remove files that are unrelated
    cmd_array = (
        ["lcov", "--remove", coverage_info_file]
        + get_html_ignored_pattern()
        + ["--output-file", coverage_info_file]
    )
    subprocess.check_call(
        # ["lcov", "--remove", coverage_info_file, "--output-file", coverage_info_file]
        cmd_array
    )
    # generate beautiful html page
    subprocess.check_call(
        [
            "genhtml",
            coverage_info_file,
            "--output-directory",
            os.path.join(SUMMARY_FOLDER_DIR, "html_report"),
        ]
    )
