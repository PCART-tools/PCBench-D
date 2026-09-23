def get_model_info(
        path_or_file,
        title=None,
        extra_file_size_limit=DEFAULT_EXTRA_FILE_SIZE_LIMIT):
    """Get JSON-friendly information about a model.

    The result is suitable for being saved as model_info.json,
    or passed to burn_in_info.
    """

    if isinstance(path_or_file, os.PathLike):
        default_title = os.fspath(path_or_file)
        file_size = path_or_file.stat().st_size  # type: ignore[attr-defined]
    elif isinstance(path_or_file, str):
        default_title = path_or_file
        file_size = pathlib.Path(path_or_file).stat().st_size
    else:
        default_title = "buffer"
        path_or_file.seek(0, io.SEEK_END)
        file_size = path_or_file.tell()
        path_or_file.seek(0)

    title = title or default_title

    with zipfile.ZipFile(path_or_file) as zf:
        path_prefix = None
        zip_files = []
        for zi in zf.infolist():
            prefix = re.sub("/.*", "", zi.filename)
            if path_prefix is None:
                path_prefix = prefix
            elif prefix != path_prefix:
                raise Exception(f"Mismatched prefixes: {path_prefix} != {prefix}")
            zip_files.append(dict(
                filename=zi.filename,
                compression=zi.compress_type,
                compressed_size=zi.compress_size,
                file_size=zi.file_size,
            ))

        assert path_prefix is not None
        version = zf.read(path_prefix + "/version").decode("utf-8").strip()

        def get_pickle(name):
            assert path_prefix is not None
            with zf.open(path_prefix + f"/{name}.pkl") as handle:
                raw = torch.utils.show_pickle.DumpUnpickler(handle, catch_invalid_utf8=True).load()
                return hierarchical_pickle(raw)

        model_data = get_pickle("data")
        constants = get_pickle("constants")

        # Intern strings that are likely to be re-used.
        # Pickle automatically detects shared structure,
        # so re-used strings are stored efficiently.
        # However, JSON has no way of representing this,
        # so we have to do it manually.
        interned_strings : Dict[str, int] = {}

        def ist(s):
            if s not in interned_strings:
                interned_strings[s] = len(interned_strings)
            return interned_strings[s]

        code_files = {}
        for zi in zf.infolist():
            if not zi.filename.endswith(".py"):
                continue
            with zf.open(zi) as handle:
                raw_code = handle.read()
            with zf.open(zi.filename + ".debug_pkl") as handle:
                raw_debug = handle.read()

            # Parse debug info and add begin/end markers if not present
            # to ensure that we cover the entire source code.
            debug_info_t = pickle.loads(raw_debug)
            assert isinstance(debug_info_t, tuple)
            debug_info = list(debug_info_t)
            if not debug_info:
                debug_info.append((0, (('', '', 0), 0, 0)))
            if debug_info[-1][0] != len(raw_code):
                debug_info.append((len(raw_code), (('', '', 0), 0, 0)))

            code_parts = []
            for di, di_next in zip(debug_info, debug_info[1:]):
                start, source_range, *_ = di
                end = di_next[0]
                assert end > start
                source, s_start, s_end = source_range
                s_text, s_file, s_line = source
                # TODO: Handle this case better.  TorchScript ranges are in bytes,
                # but JS doesn't really handle byte strings.
                # if bytes and chars are not equivalent for this string,
                # zero out the ranges so we don't highlight the wrong thing.
                if len(s_text) != len(s_text.encode("utf-8")):
                    s_start = 0
                    s_end = 0
                text = raw_code[start:end]
                code_parts.append([text.decode("utf-8"), ist(s_file), s_line, ist(s_text), s_start, s_end])
            code_files[zi.filename] = code_parts

        extra_files_json_pattern = re.compile(re.escape(path_prefix) + "/extra/.*\\.json")
        extra_files_jsons = {}
        for zi in zf.infolist():
            if not extra_files_json_pattern.fullmatch(zi.filename):
                continue
            if zi.file_size > extra_file_size_limit:
                continue
            with zf.open(zi) as handle:
                try:
                    json_content = json.load(handle)
                    extra_files_jsons[zi.filename] = json_content
                except json.JSONDecodeError:
                    extra_files_jsons[zi.filename] = "INVALID JSON"

        always_render_pickles = {
            "bytecode.pkl",
        }
        extra_pickles = {}
        for zi in zf.infolist():
            if not zi.filename.endswith(".pkl"):
                continue
            with zf.open(zi) as handle:
                # TODO: handle errors here and just ignore the file?
                # NOTE: For a lot of these files (like bytecode),
                # we could get away with just unpickling, but this should be safer.
                obj = torch.utils.show_pickle.DumpUnpickler(handle, catch_invalid_utf8=True).load()
            buf = io.StringIO()
            pprint.pprint(obj, buf)
            contents = buf.getvalue()
            # Checked the rendered length instead of the file size
            # because pickles with shared structure can explode in size during rendering.
            if os.path.basename(zi.filename) not in always_render_pickles and \
                    len(contents) > extra_file_size_limit:
                continue
            extra_pickles[zi.filename] = contents

    return {"model": dict(
        title=title,
        file_size=file_size,
        version=version,
        zip_files=zip_files,
        interned_strings=list(interned_strings),
        code_files=code_files,
        model_data=model_data,
        constants=constants,
        extra_files_jsons=extra_files_jsons,
        extra_pickles=extra_pickles,
    )}
