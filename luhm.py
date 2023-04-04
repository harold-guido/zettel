#!/usr/bin/enb python3

import argparse
from modules.system_init import init

parser = argparse.ArgumentParser(description="")
subparser = parser.add_subparsers(dest="command")

init_parser = subparser.add_parser("init", help="")

args = parser.parse_args()

if args.command == "init":
    init()
elif args.command == "update":
    update_bibliographies()
elif args.command == "add":
    add_file(args.file)
elif args.command == "stat":
    display_stats()
else:
    parser.print_help()
