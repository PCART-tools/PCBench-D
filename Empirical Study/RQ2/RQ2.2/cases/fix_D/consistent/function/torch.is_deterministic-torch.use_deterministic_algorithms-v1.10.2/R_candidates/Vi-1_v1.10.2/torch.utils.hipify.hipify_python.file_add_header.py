def file_add_header(filepath, header):
    with openf(filepath, "r+") as f:
        contents = f.read()
        if header[0] != "<" and header[-1] != ">":
            header = '"{0}"'.format(header)
        contents = ('#include {0} \n'.format(header)) + contents
        f.seek(0)
        f.write(contents)
        f.truncate()
