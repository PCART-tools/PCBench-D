def findAllGlsls(path):
    vexs = glob.glob(os.path.join(path, '**', '*.glsl'), recursive=True)
    output = []
    for f in vexs:
        if len(f) > 1:
            output.append(f)
    output.sort()
    return output
