def genCppH(hFilePath, cppFilePath, templateGlslPaths, tmpDirPath, env):
    print("hFilePath:{}".format(hFilePath))
    print("cppFilePath:{}".format(cppFilePath))
    h = "#pragma once\n"
    nsbegin = "\nnamespace at { namespace native { namespace vulkan { \n"
    nsend = "\n} } } //namespace at::native::vulkan\n"

    h += nsbegin

    cpp = "#include <ATen/native/vulkan/{}>".format(H_NAME)
    cpp += nsbegin

    for templateGlslPath in templateGlslPaths:
        name = getName(templateGlslPath)
        h += "extern const char* " + name + ";\n"
        cpp += "const char* " + name + " = \n"

        codeTemplate = CodeTemplate.from_file(templateGlslPath)
        srcPath = tmpDirPath + "/" + name + ".glsl"
        content = codeTemplate.substitute(env)

        lines = content.split("\n")
        for l in lines:
            if (len(l) < 1):
                continue
            cpp += "\"" + l + "\\n\"\n"

        cpp += ";\n"

    cpp += nsend
    h += nsend

    with open(hFilePath, "w") as f:
        f.write(h)
    with open(cppFilePath, "w") as f:
        f.write(cpp)
