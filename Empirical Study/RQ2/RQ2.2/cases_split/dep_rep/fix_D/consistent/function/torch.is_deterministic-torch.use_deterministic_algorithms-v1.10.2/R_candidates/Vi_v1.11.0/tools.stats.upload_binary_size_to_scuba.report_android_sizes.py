def report_android_sizes(file_dir: str) -> None:
    def gen_sizes() -> Generator[List[Any], None, None]:
        # we should only expect one file, if no, something is wrong
        aar_files = list(pathlib.Path(file_dir).rglob("pytorch_android-*.aar"))
        if len(aar_files) != 1:
            logging.exception(f"error getting aar files from: {file_dir} / {aar_files}")
            return

        aar_file = aar_files[0]
        zf = zipfile.ZipFile(aar_file)
        for info in zf.infolist():
            # Scan ".so" libs in `jni` folder. Examples:
            # jni/arm64-v8a/libfbjni.so
            # jni/arm64-v8a/libpytorch_jni.so
            m = re.match(r"^jni/([^/]+)/(.*\.so)$", info.filename)
            if not m:
                continue
            arch, lib = m.groups()
            # report per architecture library size
            yield [arch, lib, info.compress_size, info.file_size]

        # report whole package size
        yield ["aar", aar_file.name, os.stat(aar_file).st_size, 0]

    def gen_messages() -> Generator[Dict[str, Any], None, None]:
        android_build_type = os.environ.get("ANDROID_BUILD_TYPE")
        for arch, lib, comp_size, uncomp_size in gen_sizes():
            print(android_build_type, arch, lib, comp_size, uncomp_size)
            yield {
                "normal": {
                    "os": "android",
                    # TODO: create dedicated columns
                    "pkg_type": "{}/{}/{}".format(android_build_type, arch, lib),
                    "cu_ver": "",  # dummy value for derived field `build_name`
                    "py_ver": "",  # dummy value for derived field `build_name`
                    "pr": os.environ.get("PR_NUMBER", os.environ.get("CIRCLE_PR_NUMBER")),
                    # This is the only place where we use directly CIRCLE_BUILD_NUM, everywhere else CIRCLE_* vars
                    # are used as fallback, there seems to be no direct analogy between circle build number and GHA IDs
                    "build_num": os.environ.get("CIRCLE_BUILD_NUM"),
                    "sha1": os.environ.get("SHA1", os.environ.get("CIRCLE_SHA1")),
                    "branch": os.environ.get("BRANCH", os.environ.get("CIRCLE_BRANCH")),
                    "workflow_id": os.environ.get("WORKFLOW_ID", os.environ.get("CIRCLE_WORKFLOW_ID")),
                },
                "int": {
                    "time": int(time.time()),
                    "commit_time": int(os.environ.get("COMMIT_TIME", "0")),
                    "run_duration": int(
                        time.time() - os.path.getmtime(os.path.realpath(__file__))
                    ),
                    "size": comp_size,
                    "raw_size": uncomp_size,
                },
            }

    send_message(list(gen_messages()))
