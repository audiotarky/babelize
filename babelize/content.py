# -*- coding: utf-8; mode:python -*-

import logging
import os
import shlex
import subprocess as sp
from functools import lru_cache
from pathlib import Path

logger = logging.getLogger(__name__)


class ContentFile:

    def __init__(self, path, root_dir):
        self.__path = path
        self.__root_dir = root_dir

    @property
    def path(self):
        return self.__path

    @property
    def relative_path(self):
        return self.path.relative_to(self.root_dir)

    @property
    def root_dir(self):
        return self.__root_dir

    @property
    @lru_cache
    def translations(self):
        retval = {}
        for c in self.path.parent.iterdir():
            if c.is_dir():
                continue
            if c.match(f'*{self.path.stem}.??.md'):
                _, lang, _ = c.name.split('.')
                retval[lang] = c
        return retval

    def is_translated(self, lang=None):
        for lng, f in self.translations.items():
            if not f.is_symlink():
                if lang == lng or lang is None:
                    return True
        return False

    @lru_cache
    def needs_update(self, lang=None):
        if not self.is_translated(lang=lang):
            return []

        if lang:
            trns = [self.translations[lang]]
        else:
            trns = list(self.translations.values())

        trns = [self.path] + [t for t in trns]
        git_ls = sp.Popen(
            shlex.split(
                f'git -C {self.root_dir} ls-files '
                f'-z {" ".join(str(t) for t in trns)}'
            ),
            stdout=sp.PIPE
        )
        git_date = shlex.split(
            'xargs -0 -n1 -I{} -- '
            f'git -C {self.root_dir} log -1 --format="%at {{}}" {{}}'
        )
        output = sp.check_output(
            git_date, text=True, stdin=git_ls.stdout
        ).strip().split('\n')
        timestamps = {f: t for t, f in [line.split() for line in output]}
        git_ls.wait()
        my_timestamp = timestamps[str(self.relative_path)]
        return [Path(f) for f, t in timestamps.items() if t < my_timestamp]

    def make_symlink(self, lang):
        f = self.translations.get(lang)
        if f is None:
            target = self.path.with_name(self.path.stem + f'.{lang}.md')
            os.symlink(self.path.name, target)
            return target
        return None

    def __str__(self):
        return str(self.__path)


def make_symlinks(cfg, langs=None):
    retval = []
    if langs is None:
        if not cfg.translations:
            raise ValueError('No language provided')
        langs = cfg.translations

    logger.debug(
        "Symlinks will be created for languages: %s", ', '.join(langs)
    )
    for p in cfg.dirs:
        logger.debug("Directory '%s'", p.relative_to(cfg.root_dir))
        for f in scan_content_at_dir(cfg, p):
            for lang in langs:
                symlink = f.make_symlink(lang)
                if not symlink:
                    continue
                logger.debug(
                    "Symlink created '%s'", symlink.relative_to(cfg.root_dir)
                )
                retval.append(symlink)
    return retval


def scan_content_at_dir(cfg, path):
    for f in path.rglob('*.md'):
        if f.match('*.??.md'):
            continue
        if f.is_symlink():
            continue
        cf = ContentFile(f, cfg.root_dir)
        if cfg.is_excluded(cf.path):
            logger.debug("File excluded: '%s'", cf.relative_path)
            continue
        yield cf


def get_update_needed(cfg):
    for p in cfg.dirs:
        logger.debug("Directory '%s'", p.relative_to(cfg.root_dir))
        for f in scan_content_at_dir(cfg, p):
            if f.needs_update():
                yield f
