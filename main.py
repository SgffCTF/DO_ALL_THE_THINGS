import argparse
from pathlib import Path
from scenarios.init.init_funcs import init_services
from scenarios.sast.sast import sast_scan


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("-d", "--dir", required=True)
    
    scan_parser = subparsers.add_parser("scan")
    scan_parser.add_argument("-d", "--dir", required=True)

    args = parser.parse_args()

    if args.cmd == "init":
        
        if not Path(args.dir).exists():
            raise FileNotFoundError(args.dir)
        
        init_services(Path(args.dir))

    elif args.cmd == "scan":

        if not Path(args.dir).exists():
            raise FileNotFoundError(args.dir)

        sast_scan(Path(args.dir))

if __name__ == "__main__":
    main()