from cli import parse_args
import sys

if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    print(args)
