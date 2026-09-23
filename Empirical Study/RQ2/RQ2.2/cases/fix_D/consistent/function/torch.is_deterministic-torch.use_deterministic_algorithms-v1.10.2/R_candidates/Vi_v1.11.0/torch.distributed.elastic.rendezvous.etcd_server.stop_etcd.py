def stop_etcd(subprocess, data_dir: Optional[str] = None):
    if subprocess and subprocess.poll() is None:
        log.info("stopping etcd server")
        subprocess.terminate()
        subprocess.wait()

    if data_dir:
        log.info(f"deleting etcd data dir: {data_dir}")
        shutil.rmtree(data_dir, ignore_errors=True)
