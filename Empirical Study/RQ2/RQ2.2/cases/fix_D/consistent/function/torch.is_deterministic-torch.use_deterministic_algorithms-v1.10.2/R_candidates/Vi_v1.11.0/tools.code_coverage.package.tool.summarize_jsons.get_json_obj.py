def get_json_obj(json_file: str) -> Tuple[Any, int]:
    """
    Sometimes at the start of file llvm/gcov will complains "fail to find coverage data",
    then we need to skip these lines
      -- success read: 0      -  this json file have the full json coverage information
      -- partial success: 1   -  this json file starts with some error prompt, but still have the coverage information
      -- fail to read: 2      -  this json file doesn't have any coverage information
    """
    read_status = -1
    with open(json_file) as f:
        lines = f.readlines()
        for line in lines:
            try:
                json_obj = json.loads(line)
            except json.JSONDecodeError:
                read_status = 1
                continue
            else:
                if read_status == -1:
                    # not meet jsonDecoderError before, return success
                    read_status = 0
                return (json_obj, read_status)
    return None, 2
