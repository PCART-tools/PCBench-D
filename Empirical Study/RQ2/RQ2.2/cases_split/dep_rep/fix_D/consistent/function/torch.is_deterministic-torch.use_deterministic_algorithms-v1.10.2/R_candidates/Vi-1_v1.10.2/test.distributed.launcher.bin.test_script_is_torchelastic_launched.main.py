def main():
    args = parse_args()
    with open(args.out_file, "w") as out:
        out.write(f"{dist.is_torchelastic_launched()}")
