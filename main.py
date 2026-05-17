import argparse
from pathlib import Path
from scenarios.init_funcs import init_services


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("-d", "--dir", required=True)

    args = parser.parse_args()

    if args.cmd == "init":
        
        if not Path(args.dir).exists():
            raise FileNotFoundError(args.dir)
        
        init_services(Path(args.dir))

if __name__ == "__main__":
    main()