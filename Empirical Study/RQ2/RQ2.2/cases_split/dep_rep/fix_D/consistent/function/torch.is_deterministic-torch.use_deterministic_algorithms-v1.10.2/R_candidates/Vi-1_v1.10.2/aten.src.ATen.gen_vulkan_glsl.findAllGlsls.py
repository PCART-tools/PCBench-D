def findAllGlsls(path):
    cmd = "find " + path + " -name \"*.glsl\""
    vexs = os.popen(cmd).read().split('\n')
    output = []
    for f in vexs:
        if len(f) > 1:
            output.append(f)
    output.sort()
    return output
