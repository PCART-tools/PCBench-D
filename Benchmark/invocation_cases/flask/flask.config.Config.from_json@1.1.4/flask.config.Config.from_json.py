from flask import Flask, Config
import inspect
import json
import os
import tempfile

def main():
    app = Flask(__name__)
    config = Config(root_path=app.root_path)

    data = {"DEBUG": True, "SECRET_KEY": "supersecret"}

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(data, f)
        json_path = f.name

    try:
        config.from_json(json_path)
        print("Config values:", config["DEBUG"], config["SECRET_KEY"])
    finally:
        os.remove(json_path)

    print("-----getsource_output-----")
    try:
        print(inspect.getsource(Config.from_json))
    except Exception as e:
        print(type(e).__name__)

if __name__ == "__main__":
    main()
