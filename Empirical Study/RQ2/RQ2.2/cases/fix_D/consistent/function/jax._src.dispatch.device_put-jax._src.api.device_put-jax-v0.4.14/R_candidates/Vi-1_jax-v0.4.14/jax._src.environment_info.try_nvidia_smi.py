def try_nvidia_smi() -> Optional[str]:
  try:
    return subprocess.check_output(['nvidia-smi']).decode()
  except Exception:
    return None
