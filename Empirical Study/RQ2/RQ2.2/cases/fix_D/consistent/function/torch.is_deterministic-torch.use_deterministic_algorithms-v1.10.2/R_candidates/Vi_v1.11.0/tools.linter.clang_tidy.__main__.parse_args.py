def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="clang-tidy wrapper script")
    parser.add_argument(
        "-e",
        "--clang-tidy-exe",
        default=DEFAULTS["clang-tidy-exe"],
        help="Path to clang-tidy executable",
    )
    parser.add_argument(
        "-g",
        "--glob",
        action="append",
        default=DEFAULTS["glob"],
        help="Only lint files that match these glob patterns "
        "(see documentation for `fnmatch` for supported syntax)."
        "If a pattern starts with a - the search is negated for that pattern.",
    )
    parser.add_argument(
        "-x",
        "--regex",
        action="append",
        default=[],
        help="Only lint files that match these regular expressions (from the start of the filename). "
        "If a pattern starts with a - the search is negated for that pattern.",
    )
    parser.add_argument(
        "-c",
        "--compile-commands-dir",
        default=DEFAULTS["compile-commands-dir"],
        help="Path to the folder containing compile_commands.json",
    )
    parser.add_argument(
        "--diff-file",
        help="File containing diff to use for determining files to lint and line filters",
    )
    parser.add_argument(
        "-p",
        "--paths",
        nargs="+",
        default=DEFAULTS["paths"],
        help="Lint only the given paths (recursively)",
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Only show the command to be executed, without running it",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-q", "--quiet", action="store_true", help="Don't print output")
    parser.add_argument(
        "--config-file",
        default=DEFAULTS["config-file"],
        help="Path to a clang-tidy config file. Defaults to '.clang-tidy'.",
    )
    parser.add_argument(
        "--print-include-paths",
        action="store_true",
        help="Print the search paths used for include directives",
    )
    parser.add_argument(
        "-I",
        "--include-dir",
        action="append",
        default=DEFAULTS["include-dir"],
        help="Add the specified directory to the search path for include files",
    )
    parser.add_argument(
        "-s",
        "--suppress-diagnostics",
        action="store_true",
        help="Add NOLINT to suppress clang-tidy violations",
    )
    parser.add_argument(
        "--disable-progress-bar",
        action="store_true",
        default=DEFAULTS["disable-progress-bar"],
        help="Disable the progress bar",
    )
    parser.add_argument(
        "extra_args", nargs="*", help="Extra arguments to forward to clang-tidy"
    )
    return parser.parse_args()
