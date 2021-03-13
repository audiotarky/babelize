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

    args = parser.parse_args()
    cfg.init_logging(logging.DEBUG if args.verbose else logging.INFO)
    return 0
