import re
from glob import glob
from pathlib import Path
from typing import NamedTuple

from ruamel.yaml import YAML

from nsa.plugin import base
from nsa.settings import Settings


class LineRegexRule(NamedTuple):
    title: str
    pattern: str
    platforms: list = []
    link: str = ""
    ticket: str = ""
    reason: str = ""
    cve: str = ""
    score: str = ""
    operator: str = "in"
    wiki: str = ""


class LineRegexParser(base.ParserBase):
    def _load_yaml(self, filename):
        """Load a YAML file."""
        yaml = YAML()
        with open(filename) as fhandle:
            return yaml.load(fhandle.read())

    def _load_rules(self):
        """Load rules definitions from rules.d/*.yml"""
        rules = []

        for fname in glob(self.path, recursive=True):
            fname = Path(fname)
            if fname.is_dir():
                continue
            rules.append(self._load_yaml(fname))
        return rules

    def merge_rules(self):
        """Merge all rules definitions."""
        rules = self._load_rules()
        self.rules = [
            LineRegexRule(**r) for rule in rules for r in rule["rules"]
        ]

    def get_previous_lines(self, index, lines):
        if index - self.lines_of_context < 0:
            previous_lines = lines[index - 1 :: -1]
        else:
            previous_lines = lines[
                index - 1 : index - self.lines_of_context : -1
            ]
        previous_lines.reverse()
        return previous_lines

    def get_next_lines(self, index, lines):
        return lines[index + 1 : index + self.lines_of_context]

    def search(self, line, platform):
        for rule in self.rules:
            if platform not in rule.platforms:
                continue
            match = re.search(rule.pattern, line)
            if self._match(rule.operator, match):
                return (rule, match)
        return (rule, None)

    def _match(self, operator, match):
        result = False
        if operator == "in" and match:
            result = True
        elif operator == "not_in" and not match:
            result = True
        return result

    def setup(self):
        self.path = Settings().plugins[self.kind][self.name]["path"]
        self.lines_of_context = 3
        if "context" in Settings().plugins[self.kind][self.name]:
            self.lines_of_context = Settings().plugins[self.kind][self.name][
                "context"
            ]
        self.lines_of_context += 1
        self.merge_rules()

    def parse(self, input_):
        errors = []
        contents = input_["contents"]
        for index, line in enumerate(contents):
            rule, results = self.search(line, input_["platform"])
            if results:
                next_lines = self.get_next_lines(index, contents)
                previous_lines = self.get_previous_lines(index, contents)
                errors.append(
                    {
                        "title": rule.title,
                        "device": input_["device"],
                        "platforms": rule.platforms,
                        "link": rule.link,
                        "ticket": rule.ticket,
                        "reason": rule.reason,
                        "previous_lines": previous_lines,
                        "match": results.string,
                        "next_lines": next_lines,
                        "cve": rule.cve,
                        "score": rule.score,
                        "wiki": rule.wiki,
                    }
                )
        return errors
