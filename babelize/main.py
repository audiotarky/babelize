#!/usr/bin/env python3
# -*- coding: utf-8; mode:python -*-

import argparse
import logging

from . import cfg

logger = logging.getLogger(__name__)


def config_from_arg(path):
    try:
        return cfg.load(path)
    except FileNotFoundError:
        error = f"file '{path}' not found"
    except ValueError:
        error = (
            f"file '{path}' has an invalid content. "
            "Please check content is valid JSON."
        )
    raise argparse.ArgumentTypeError(error)


def do_link(args):
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        '--config',
        type=config_from_arg,
        default='.babelize.json',
        help='path to config file. Default %(default)s',
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='enable verbose output'
    )

    subparsers = parser.add_subparsers()
    subparsers.required = True
    subparsers.dest = 'command'

    link = subparsers.add_parser('link', aliases=['ln'])
    link.set_defaults(run=do_link)

    args = parser.parse_args()
    cfg.init_logging(logging.DEBUG if args.verbose else logging.INFO)

    if 'run' not in args:
        print(args)

    return args.run(args)
