from .main import parse_args

if __name__ == "__main__":
    import sys
    args = parse_args(sys.argv[1:])
    print(args)
