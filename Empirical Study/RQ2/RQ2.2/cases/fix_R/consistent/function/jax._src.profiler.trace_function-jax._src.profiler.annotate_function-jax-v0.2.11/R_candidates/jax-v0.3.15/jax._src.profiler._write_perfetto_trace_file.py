def _write_perfetto_trace_file(log_dir):
  # Navigate to folder with the latest trace dump to find `trace.json.jz`
  curr_path = os.path.abspath(log_dir)
  root_trace_folder = os.path.join(curr_path, "plugins", "profile")
  trace_folders = [os.path.join(root_trace_folder, trace_folder) for
      trace_folder in os.listdir(root_trace_folder)]
  latest_folder = max(trace_folders, key=os.path.getmtime)
  trace_jsons = glob.glob(os.path.join(latest_folder, "*.trace.json.gz"))
  if len(trace_jsons) != 1:
    raise ValueError(f"Invalid trace folder: {latest_folder}")
  trace_json, = trace_jsons

  logging.info("Loading trace.json.gz and removing its metadata...")
  # Perfetto doesn't like the `metadata` field in `trace.json` so we remove
  # it.
  # TODO(sharadmv): speed this up by updating the generated `trace.json`
  # to not include metadata if possible.
  with gzip.open(trace_json, "rb") as fp:
    trace = json.load(fp)
    del trace["metadata"]
  filename = "perfetto_trace.json.gz"
  perfetto_trace = os.path.join(latest_folder, filename)
  logging.info("Writing perfetto_trace.json.gz...")
  with gzip.open(perfetto_trace, "w") as fp:
    fp.write(json.dumps(trace).encode("utf-8"))
  return perfetto_trace
