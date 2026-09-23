def main(argv):
    struct_members = []
    load_functions = []
    define_checks = []

    for ret, name, args in NNAPI_FUNCTIONS:
        short_name = name.replace("ANeuralNetworks", "", 1)

        struct_members.append(f"  {ret}(*{short_name})({args});")

        load_functions.append(f'    *(void**)&nnapi_.{short_name} = dlsym(handle, "{name}");')
        load_functions.append(f'    check_nnapi_.{short_name} = check_{short_name};')

        call_args = "".join(re.findall(r"\w+(?:,|$)", args))
        if ret == "void":
            define_checks.append(textwrap.dedent(f"""\
                {ret} check_{short_name}({args}) {{
                  CAFFE_ENFORCE(nnapi_.{short_name});
                  nnapi_.{short_name}({call_args});
                }}"""))
        if ret == "int":
            define_checks.append(textwrap.dedent(f"""\
                {ret} check_{short_name}({args}) {{
                  CAFFE_ENFORCE(nnapi_.{short_name});
                  int ret = nnapi_.{short_name}({call_args});
                  // TODO: Maybe add better logging here.
                  CAFFE_ENFORCE(
                    ret == ANEURALNETWORKS_NO_ERROR,
                    "{short_name}", "failed with error ", ret
                  );
                  return ret;
                }}"""))

    out_dir = pathlib.Path(__file__).parent

    (out_dir / "nnapi_wrapper.h").write_text(
        PREFIX +
        textwrap.dedent("""\
            #ifndef NNAPI_WRAPPER_H_
            #define NNAPI_WRAPPER_H_
            #include <stddef.h>
            #include <stdint.h>
            #include <ATen/nnapi/NeuralNetworks.h>
            struct nnapi_wrapper {
            __STRUCT_MEMBERS__
            };
            #ifdef __cplusplus
            void nnapi_wrapper_load(struct nnapi_wrapper** nnapi, struct nnapi_wrapper** check_nnapi);
            #endif
            #endif
            """)
        .replace("__STRUCT_MEMBERS__", "\n".join(struct_members))
    )

    (out_dir / "nnapi_wrapper.cpp").write_text(
        PREFIX +
        textwrap.dedent("""\
            #ifndef _WIN32
            #include <dlfcn.h>
            #endif
            #include <ATen/nnapi/nnapi_wrapper.h>
            #include <c10/util/Logging.h>
            // NOLINTNEXTLINE(cppcoreguidelines-avoid-non-const-global-variables)
            static int loaded = 0;
            // NOLINTNEXTLINE(cppcoreguidelines-avoid-non-const-global-variables)
            static struct nnapi_wrapper nnapi_;
            // NOLINTNEXTLINE(cppcoreguidelines-avoid-non-const-global-variables)
            static struct nnapi_wrapper check_nnapi_;
            __DEFINE_CHECK_FUNCTIONS__
            void nnapi_wrapper_load(struct nnapi_wrapper** nnapi, struct nnapi_wrapper** check_nnapi) {
            #ifdef _WIN32
              TORCH_CHECK(false, "Running NNAPI models is not supported on Windows.");
            #else
              if (!loaded) {
                // Clear error flag.
                dlerror();
                void* handle = dlopen("libneuralnetworks.so", RTLD_LAZY | RTLD_LOCAL);
                CAFFE_ENFORCE(handle, "Failed to load libneuralnetworks.so ", dlerror());
            __LOAD_FUNCTIONS__
                loaded = 1;
              }
              *nnapi = &nnapi_;
              *check_nnapi = &check_nnapi_;
            #endif
            }
            """)
        .replace("__DEFINE_CHECK_FUNCTIONS__", "\n".join(define_checks))
        .replace("__LOAD_FUNCTIONS__", "\n".join(load_functions))
    )
