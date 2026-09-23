def _raw_frame_to_frame(code: types.CodeType, lasti: int) -> Frame:
  return Frame(file_name=code.co_filename,
               function_name=code.co_name,
               line_num=xla_client.Traceback.code_addr2line(code, lasti))
