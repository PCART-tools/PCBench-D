def _run_printable(cmd):
    proc = subprocess.run(shlex.split(cmd), capture_output=True)  # type: ignore[call-overload]
    assert proc.returncode == 0

    buffer = io.BytesIO()
    torch.save(proc.stdout.decode("utf-8"), buffer)
    input_tensor = torch.ByteTensor(list(buffer.getvalue()))
    input_length = torch.IntTensor([input_tensor.size(0)])

    output = []
    buffer = io.BytesIO(np.asarray(input_tensor).tobytes())
    output.append(torch.load(buffer))
    return output
