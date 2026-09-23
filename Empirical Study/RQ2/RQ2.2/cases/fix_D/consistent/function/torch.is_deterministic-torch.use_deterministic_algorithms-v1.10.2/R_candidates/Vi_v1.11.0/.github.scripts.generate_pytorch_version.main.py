def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate pytorch version for binary builds"
    )
    parser.add_argument(
        "--no-build-suffix",
        action="store_true",
        help="Whether or not to add a build suffix typically (+cpu)",
        default=strtobool(os.environ.get("NO_BUILD_SUFFIX", "False"))
    )
    parser.add_argument(
        "--gpu-arch-type",
        type=str,
        help="GPU arch you are building for, typically (cpu, cuda, rocm)",
        default=os.environ.get("GPU_ARCH_TYPE", "cpu")
    )
    parser.add_argument(
        "--gpu-arch-version",
        type=str,
        help="GPU arch version, typically (10.2, 4.0), leave blank for CPU",
        default=os.environ.get("GPU_ARCH_VERSION", "")
    )
    args = parser.parse_args()
    version_obj = PytorchVersion(
        args.gpu_arch_type,
        args.gpu_arch_version,
        args.no_build_suffix
    )
    try:
        print(version_obj.get_release_version())
    except NoGitTagException:
        print(version_obj.get_nightly_version())
