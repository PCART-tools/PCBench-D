def _pprof_profile(
    profile: dict[tuple[Optional[xla_client.Traceback], core.Primitive], int]
) -> bytes:
  """Converts a profile into a compressed pprof protocol buffer.

  The input profile is a map from (traceback, primitive) pairs to counts.
  """
  s: DefaultDict[str, int]
  func: DefaultDict[types.CodeType, int]
  loc: DefaultDict[tuple[types.CodeType, int], int]

  s = collections.defaultdict(itertools.count(1).__next__)
  func = collections.defaultdict(itertools.count(1).__next__)
  loc = collections.defaultdict(itertools.count(1).__next__)
  s[""] = 0
  primitive_key = s["primitive"]
  samples = []
  for (tb, primitive), count in profile.items():
    if tb is None:
      frames = []
    else:
      raw_frames = zip(*tb.raw_frames())
      frames = [loc[(code, lasti)] for code, lasti in raw_frames
                if source_info_util.is_user_filename(code.co_filename)]  # type: ignore
    samples.append({
       "location_id": frames,
       "value": [count],
       "label": [{
         "key": primitive_key,
         "str": s[primitive.name]
        }]
    })

  locations = [
      {"id": loc_id,
       "line": [{"function_id": func[code],
                 "line": xla_client.Traceback.code_addr2line(code, lasti)}]}
      for (code, lasti), loc_id in loc.items()
  ]
  functions = [
      {"id": func_id,
       "name": s[code.co_name],
       "system_name": s[code.co_name],
       "filename": s[code.co_filename],
       "start_line": code.co_firstlineno}
      for code, func_id in func.items()
  ]
  sample_type = [{"type": s["equations"], "unit": s["count"]}]
  # This is the JSON encoding of a pprof profile protocol buffer. See:
  # https://github.com/google/pprof/blob/master/proto/profile.proto for a
  # description of the format.
  json_profile = json.dumps({
    "string_table": list(s.keys()),
    "location": locations,
    "function": functions,
    "sample_type": sample_type,
    "sample": samples,
  })
  return gzip.compress(xla_client._xla.json_to_pprof_profile(json_profile))
