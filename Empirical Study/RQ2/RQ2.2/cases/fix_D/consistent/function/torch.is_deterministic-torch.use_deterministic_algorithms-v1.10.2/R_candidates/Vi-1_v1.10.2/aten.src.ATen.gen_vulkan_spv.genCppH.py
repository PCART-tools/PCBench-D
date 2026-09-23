def genCppH(hFilePath, cppFilePath, srcDirPath, glslcPath, tmpDirPath, env):
    print("hFilePath:{} cppFilePath:{} srcDirPath:{} glslcPath:{} tmpDirPath:{}".format(
        hFilePath, cppFilePath, srcDirPath, glslcPath, tmpDirPath))

    cmd = "find " + srcDirPath + " -name \"*.glsl\""
    vexs = os.popen(cmd).read().split('\n')
    templateSrcPaths = []
    for f in vexs:
        if len(f) > 1:
            templateSrcPaths.append(f)
            templateSrcPaths.sort()
    print("templateSrcPaths:{}".format(templateSrcPaths))

    spvPaths = []
    for templateSrcPath in templateSrcPaths:
        print("templateSrcPath {}".format(templateSrcPath))
        name = getName(templateSrcPath).replace("_glsl", "")
        print("name {}".format(name))

        codeTemplate = CodeTemplate.from_file(templateSrcPath)
        srcPath = tmpDirPath + "/" + name + ".glsl"
        content = codeTemplate.substitute(env)
        with open(srcPath, 'w') as f:
            f.write(content)

        spvPath = tmpDirPath + "/" + name + ".spv"
        print("spvPath {}".format(spvPath))

        cmd = [
            glslcPath, "-fshader-stage=compute", "-Os",
            srcPath, "-o", spvPath,
            "--target-env=vulkan1.0",
            "-Werror"
        ]

        print("\nglslc cmd:", cmd)

        subprocess.check_call(cmd)
        spvPaths.append(spvPath)

    h = "#pragma once\n"
    h += "#include <stdint.h>\n"
    nsbegin = "\nnamespace at { namespace native { namespace vulkan { \n"
    nsend = "\n} } } //namespace at::native::vulkan\n"

    h += nsbegin

    cpp = "#include <ATen/native/vulkan/{}>".format(H_NAME)
    cpp += nsbegin

    for spvPath in spvPaths:
        name = getName(spvPath)
        name_len = name + "_len"
        h += "extern const uint32_t {}[];\n".format(name)
        h += "extern const uint32_t {};\n".format(name_len)

        cpp += "const uint32_t " + name + "[] = {\n"
        sizeBytes = 0
        print("spvPath:{}".format(spvPath))
        with open(spvPath, 'rb') as f:
            for word in array.array('I', f.read()):
                cpp += "{},\n".format(word)
                sizeBytes += 4
            cpp += "};\n"
        cpp += "const uint32_t {} = {};\n".format(name_len, sizeBytes)

    cpp += nsend
    h += nsend

    with open(hFilePath, "w") as f:
        f.write(h)
    with open(cppFilePath, "w") as f:
        f.write(cpp)
