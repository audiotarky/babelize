# -*- coding: utf-8; mode:python -*-

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class Config:
    def __init__(self, cfg):
        self.cfg = cfg

    @property
    def root_dir(self):
        return Path(self.cfg["root_dir"])


def load(path):
    p = Path(path).absolute()
    cfg = json.loads(open(p).read())
    cfg.setdefault("root_dir", str(p.parent.resolve()))
    return Config(cfg)


def init_logging(level):
    log = logging.getLogger()
    log.setLevel(level)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    # create formatter and add it to the handler
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    log.addHandler(handler)
