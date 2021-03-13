from collections import Counter, defaultdict
from pathlib import Path
import os

def do_list(args):
    if args.lang:
        print(f'Listing for {args.lang}')
    counter = defaultdict(lambda: defaultdict(Counter))
    for d in args.config.dirs:
        for language in [l.lower() for l in args.lang]:
            for dirpath, dirnames, filenames in os.walk(d, followlinks=True):
                dirpath_as_path = Path(dirpath)
                md_files = [f for f in filenames if f.lower().endswith('.md')]
                lang_files = [f for f in filenames if f.lower().endswith(f'.{language}.md')]
                content_files = []
                for file in [dirpath_as_path / Path(f) for f in md_files]:
                    short_file_path = file.relative_to(args.config.root_dir)
                    depth = len(short_file_path.parents) - args.depth - 1
                    if depth < 0:
                        depth = 0
                    if len(file.suffixes) > 1:
                        continue
                    if f'{file.stem}.{language}.md' in lang_files:
                        lang_file = dirpath_as_path / Path(f'{file.stem}.{language}.md')
                        if lang_file.is_symlink():
                            if args.verbose:
                                print(f'{short_file_path} has a symlink for {language}')
                            counter[language][short_file_path.parents[depth].as_posix()]['symlink'] += 1
                        else:
                            if args.verbose:
                                print(f'{short_file_path} has a translation for {language}')
                            counter[language][short_file_path.parents[depth].as_posix()]['translation'] += 1
                    else:
                        if args.verbose:
                            print (f'{short_file_path} is missing a translation or symlink for {language}')
                        counter[language][short_file_path.parents[depth].as_posix()]['missing'] += 1

    spacing = 6
    if not args.verbose:
        print(f'{"T".ljust(spacing)} {"L".ljust(spacing)} {"M".ljust(spacing)} Lang Directory')
        print('------------------------------------')
    for lang, c in counter.items():
        for k,v in c.items():
            if args.verbose:
                print (f'{k} has {v["translation"]} translations, {v["symlink"]} symlinks,  {v["missing"]} missing for {lang}')
            else:
                print (f'{str(v["translation"]).ljust(spacing)} {str(v["symlink"]).ljust(spacing)} {str(v["missing"]).ljust(spacing)} {str(lang.ljust(4))} {k}')
