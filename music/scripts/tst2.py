from pathlib import Path
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("musicFolder")
args = parser.parse_args()

musicFolder = args.musicFolder

ext = lambda p: str(os.path.splitext(os.path.basename(p))[1])

extensions = [".PDF", ".chopro", ".cho", ".mscz", ".url"]
allFiles = []
for p in Path(musicFolder).rglob('*'):
  if ext(p).upper() in (extension.upper() for extension in extensions):
    print(p)
