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
        return Path(self.cfg['root_dir']).resolve()

    @property
    def translations(self):
        return self.cfg['translations']

    @property
    def dirs(self):
        return [
            Path(self.root_dir, d) for d in self.cfg.get('dirs', ['content'])
        ]

    def is_excluded(self, path, lang=None):
        patterns = []
        if lang is not None:
            patterns = self.cfg.get(lang, {}).get('exclude', [])
        patterns = patterns or self.cfg.get('exclude')
        return any(path.match(p) for p in patterns)


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
