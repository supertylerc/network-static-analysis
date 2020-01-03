import colorama

from nsa.plugin import base


class TextOutput(base.OutputBase):
    def print_(self, color, s, **kwargs):
        print(self.colors[color] + s, **kwargs)

    def setup(self):
        colorama.init(autoreset=True)
        self.colors = {
            "red": colorama.Fore.RED,
            "yellow": colorama.Fore.YELLOW,
            "green": colorama.Fore.GREEN,
        }

    def write(self, results):
        for device, result in results.items():
            self.write_msg(device, result)

    def write_msg(self, device, msg):
        self.print_(
            "yellow", f"Found one or more matches for device: {device}!"
        )
        for match in msg:
            self._write_msg(match)

    def _write_msg(self, match):
        print("Title: ", end="")
        self.print_("green", match["title"])
        self.print_("green", "Configuration Matched:", end="\n\n")
        print("\n".join(match["previous_lines"]))
        self.print_("red", match["match"])
        print("\n".join(match["next_lines"]), end="\n\n")
        print("Reason: ", end="")
        self.print_("green", match["reason"])
        print(f"Platform(s): {','.join(match['platforms'])}")
        print(f"CVE: {match['cve']}")
        print(f"Link: {match['link']}")
        print(f"Score: {match['score']}")
        print(f"Ticket: {match['ticket']}")
        print(f"Wiki/KB: {match['wiki']}")
        print("=" * 79)
