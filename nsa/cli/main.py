import argparse
from glob import glob
from pathlib import Path
from shutil import copy2

from ruamel.yaml import YAML
from stevedore import driver

from nsa.api import INPUT_SCHEMA, VIOLATION_SCHEMA
from nsa.settings import Settings


def get_plugin(profile, kind):
    return driver.DriverManager(
        namespace=profile["plugins"][kind]["namespace"],
        name=profile["plugins"][kind]["name"],
        invoke_on_load=True,
    )


def get_plugins(profile):
    input_mgr = get_plugin(profile, "input")
    parser_mgr = get_plugin(profile, "parser")
    output_mgr = get_plugin(profile, "output")
    return {
        "input": input_mgr.driver,
        "parser": parser_mgr.driver,
        "output": output_mgr.driver,
    }


def initialize_plugins(plugins):
    for plugin in plugins:
        plugins[plugin].setup()


def teardown_plugin(plugin):
    plugin.teardown()


def validate(kind, data):
    mapping = {"input": INPUT_SCHEMA, "parser": VIOLATION_SCHEMA}
    for k, v in data.items():
        mapping[kind].validate(v)


def get_profile(name):
    return Settings().profiles[name]


def get_input_data(plugin):
    data = plugin.read()
    teardown_plugin(plugin)
    validate("input", data)
    return data


def get_violations(plugin, data):
    results = {device: plugin.parse(data[device]) for device in data}
    validate("parser", results)
    teardown_plugin(plugin)
    return results


def output(plugin, violations):
    plugin.write(violations)
    teardown_plugin(plugin)


def mkdir(path):
    try:
        path.mkdir(parents=True, exist_ok=True)
    except IOError:
        print(f"Unable to create directory at {path}")
        print("Check destination directory permissions and copy manually.")
        raise


def copy(src, dest):
    try:
        copy2(src, dest)
    except IOError:
        print(f"Unable to write {src} to {dest}")
        print("Check destination directory permissions and copy manually.")


def scan(args):
    profile = get_profile(args.profile)
    plugins = get_plugins(profile)

    initialize_plugins(plugins)

    data = get_input_data(plugins["input"])
    results = get_violations(plugins["parser"], data)

    output(plugins["output"], results)


def init(args):
    yaml = YAML()
    pwd = Path(__file__).parent
    with open(pwd.absolute() / "nsa.yml", "r") as fname:
        defaults = yaml.load(fname)
    defaults["plugins"]["input"]["glob"]["path"] = f"{args.path}/files.d/**/*"
    defaults["plugins"]["parser"]["lineregex"][
        "path"
    ] = f"{args.path}/rules.d/**/*"
    with open(args.filename, "w") as fname:
        yaml.dump(defaults, fname)
    mkdir(Path(f"{args.path}/rules.d/default/"))
    our_rules_dir = pwd.parent.absolute() / "rules"

    for fname in our_rules_dir.glob("*.yml"):
        if fname.is_dir():
            continue
        copy(fname, Path(f"{args.path}/rules.d/default/"))


def main():
    parser = argparse.ArgumentParser(
        description="Analyze network configuration files"
    )
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers()

    init_parser = subcommands.add_parser("init")
    init_parser.add_argument("-f", "--filename", default="nsa.yml")
    init_parser.add_argument("-p", "--path", default="/etc/nsa-py")
    init_parser.set_defaults(func=init)

    scan_parser = subcommands.add_parser("scan")
    scan_parser.add_argument("-p", "--profile", default="default")
    scan_parser.set_defaults(func=scan)

    args = parser.parse_args()
    args.func(args)
