def run_torchbench(pytorch_path: str, torchbench_path: str, output_dir: str) -> None:
    # Copy system environment so that we will not override
    env = dict(os.environ)
    command = ["python", "bisection.py", "--work-dir", output_dir,
               "--pytorch-src", pytorch_path, "--torchbench-src", torchbench_path,
               "--config", os.path.join(output_dir, "config.yaml"),
               "--output", os.path.join(output_dir, "result.txt")]
    subprocess.check_call(command, cwd=torchbench_path, env=env)
