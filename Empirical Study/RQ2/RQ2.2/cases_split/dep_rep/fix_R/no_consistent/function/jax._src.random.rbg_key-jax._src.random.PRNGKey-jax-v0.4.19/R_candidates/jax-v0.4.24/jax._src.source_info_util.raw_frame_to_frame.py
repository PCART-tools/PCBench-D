  def raw_frame_to_frame(code: types.CodeType, lasti: int) -> Frame:
    # pre-3.11 co_qualname does not exist, use co_name
    return Frame(file_name=code.co_filename,
                function_name=code.co_name,
                start_line=xla_client.Traceback.code_addr2line(code, lasti),
                start_column=0, end_line=0, end_column=0)
