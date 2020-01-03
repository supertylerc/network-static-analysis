import re

from nsa.settings import Settings


class PlatformDetectionError(BaseException):
    pass


def detect_platform(contents):
    # TC: I don't love the `break` implementation in this function, but
    #     it does the job for now.
    for line in contents:
        platform = _detect_platform(line, "default")
        if platform:
            break
        try:
            platform = _detect_platform(line, "custom")
            if platform:
                break
        except AttributeError:
            pass
    if platform is None:
        raise PlatformDetectionError
    return platform


def _detect_platform(line, pattern_type):
    platform_patterns = getattr(
        Settings(), pattern_type + "_platform_patterns"
    )
    for platform, patterns in platform_patterns.items():
        for pattern in patterns:
            if re.search(pattern, line):
                return platform
    return None
