# -*- coding: utf-8; mode:python -*-

import logging
import os

logger = logging.getLogger(__name__)


class ContentFile:

    def __init__(self, path):
        self.__path = path

    @property
    def path(self):
        return self.__path

    @property
    def translations(self):
        # TODO - this might need caching as it could be very expensive
        # for large amount of files.
        retval = {}
        for c in self.path.parent.iterdir():
            if c.is_dir():
                continue
            if c.match(f'*{self.path.stem}.??.md'):
                _, lang, _ = c.name.split('.')
                retval[lang] = c
        return retval

    def make_symlink(self, lang):
        f = self.translations.get(lang)
        if f is None:
            target = self.path.with_name(self.path.stem + f'.{lang}.md')
            os.symlink(self.path.name, target)
            return target
        return None

    def __str__(self):
        return str(self.__path)


def make_symlinks(cfg):
    retval = []
    for p in cfg.dirs:
        logger.debug("Directory '%s'", p.relative_to(cfg.root_dir))
        for f in scan_content_at_dir(p):
            if cfg.is_excluded(f.path):
                logger.debug(
                    "File excluded: '%s'", f.path.relative_to(cfg.root_dir)
                )
                continue
            for lang in cfg.translations:
                symlink = f.make_symlink(lang)
                if not symlink:
                    continue
                logger.debug(
                    "Symlink created '%s'", symlink.relative_to(cfg.root_dir)
                )
                retval.append(symlink)
    return retval


def scan_content_at_dir(path):
    for f in path.rglob('*.md'):
        if f.match('*.??.md'):
            continue
        if f.is_symlink():
            continue
        yield ContentFile(f)