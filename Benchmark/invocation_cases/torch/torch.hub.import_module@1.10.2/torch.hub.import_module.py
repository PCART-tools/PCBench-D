import torch
import tempfile
import textwrap
import os
import inspect

def main():
    with tempfile.TemporaryDirectory() as tmpdir:
        module_path = os.path.join(tmpdir, "mymodule.py")

        with open(module_path, "w") as f:
            f.write(textwrap.dedent("""
                def hello():
                    return "hello from torch.hub.import_module"
            """))
        mod = torch.hub.import_module("mymodule", module_path)
        print(mod)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(torch.hub.import_module))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()