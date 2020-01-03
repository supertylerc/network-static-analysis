from glob import glob
from pathlib import Path

import nsa.utils
from nsa.plugin import base
from nsa.settings import Settings
from nsa.utils import PlatformDetectionError


class GlobInput(base.InputBase):
    def setup(self):
        self.path = Settings().plugins[self.kind][self.name]["path"]

    def read(self):
        mapping = {}
        for fname in glob(self.path, recursive=True):
            fname = Path(fname)
            if fname.is_dir():
                continue
            with open(fname) as fhandle:
                contents = [x.rstrip("\n") for x in fhandle.readlines()]
                try:
                    platform = nsa.utils.detect_platform(contents)
                except PlatformDetectionError:
                    # TC: add logging to indicate we couldn't detect a platform
                    continue
            mapping[fname.name] = {
                "device": fname.name,
                "contents": contents,
                "platform": platform,
            }
        return mapping
