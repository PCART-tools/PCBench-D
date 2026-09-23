def run(cmd, cuda_visible_devices=""):
    return subprocess.run(
        cmd,
        env={
            "CUDA_VISIBLE_DEVICES": str(cuda_visible_devices),
            "PATH": os.getenv("PATH", ""),
        },
        stdout=subprocess.PIPE,
        shell=True
    )
