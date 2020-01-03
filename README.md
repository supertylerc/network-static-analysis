# network-security-analysis

`nsa` is a static configuration analysis tool for ensuring network
device configuration compliance.  The software is currently in an
**ALPHA** state.  This is what it means for this project:

- the default CLI tool should always work, but it might break from one
  commit to another
- the internal APIs and external plugin APIs are subject to frequent
  and rapid change
- the configuration file schemas may change during development, but
  backwards compatability will be maintained until the project is
  promoted to beta
- there is little to no test coverage
- there is not much documentation

This translates to:

If you're an **end user**, you should be able to use this throughout the
entirety of the Alpha without worrying about new releases fundamentally
breaking your usage.  Once the project is promoted to **beta**, you may
need to update your configuration file(s) as all previous alpha APIs
will be removed prior to beta promotion.

If you're a **developer**, expect naming and other API changes with
little to no backwards compatibility guarantees.  Expect the
documentation to be the source code itself.  Expect a lack of tests to
cause internal breakage and unexpected failures.

## Quick Start

During the Alpha, this project primarily uses and supports installation
with `pipenv`.  Instructions are provided for use if you don't have
`pipenv`, but the resulting installation may have slight differences in
dependency versions.  The instructions without `pipenv` also do not
include details for creating a virtual environment.

If you have `pipenv`:

```bash
$ git clone https://github.com/supertylerc/network-static-analysis.git
$ cd network-static-analysis
$ pipenv sync
$ pipenv run pip install -e .
```

If you don't have `pipenv`:

```bash
$ git clone https://github.com/supertylerc/network-static-analysis.git
$ cd network-static-analysis
$ pip install -r requirements.txt
$ pip install -e .
```

Create a default configuration in your current directory:

```bash
$ nsa init
```

This will create a file, `nsa.yml`, in your current directory.  This
file contains a default configuration, but you'll need to update it to
contain paths to your configuration files and your rules definitions.

> Note that running `nsa init` multiple times will overwrite the
> `nsa.yml` file and all of the default rules names without
> confirmation.  Only run the command more than once if you are sure
> this is what you want.

The default path for config files is `/etc/nsa-py/files.d/**/*`, while
the default path for rules files is `/etc/nsa-py/rules.d/**/*`.  Once
you've updated those paths (or placed your files and rules there), you
can run `nsa` with the following command:

```bash
$ nsa scan
```

## Customizing nsa

`nsa` looks for its configuration file (`nsa.yml`) in the following
places, in order of preference:

* a location specified by the `NSA_FILE` environment variable
* `$(pwd)/nsa.yml`
* `$HOME/.nsa.yml`
* `$(pwd)/nsa.yaml`
* `$HOME/.nsa.yaml`

> `nsa` does not merge the contents of these files and will use the
> first file it can find and then stop looking for other locations.

`nsa` can be customized by defining unique profiles in `nsa.yaml`.

## Guiding Principles

This project started from a desire to have tooling similar to other
systems and programming languages that provide static analysis of the
code and/or configuration.  Some examples of tools in this vein are:

- shellcheck
- bandit
- ansible-lint

For some context and history, see `HISTORY.md`.

### Goals

* Simple tool for static analysis of network configuration files
* A standard library of checks that is maintained
  (preferably by a community)
* Usable as-shipped for many people, but flexible and extensible enough
  for those inclined to do so to enable more powerful features and tests

### Non-Goals

"Non-goals" sometimes deserve a little bit of explanation, so that is
below if you're interested.  Otherwise, the tl;dr is:

* Support everything!
* GUI/Web UI/HTTP API/\<Other "modern web" Thing Here\>
* Abstract composability

One of the biggest "non-goals" with this project is `providing and/or
supporting everything.`  While it does aim to be pluggable and
extendable, it does not try to provide every possible plugin, nor does
it try to go to the extreme of making every single item of the plugin
configurable.

Another non-goal was providing a web UI.  One might eventually be made
as another package, but one will likely never be provided directly in
this package.  I wanted to build a building block.

Finally, although I wanted something composable, I didn't really want to
deal with the complexity of abstracting that composability.  In other
words, the default CLI tool has a very static pipeline of `input |
parser | output`, but I also wanted it to be very easy for someone else
to change how that works, adding in extra bits where necessary to
achieve the desired effect while still providing some of the plumbing
and a standard library of rules.

## Design Overview

`nsa` runs in three stages, and each stage is plugin-based.

1: **Input**: Obtain configuration data and detect the OS

2: **Parser**: Go through the configuration data and look for violations

3: **Output**: Transform the results from the **Parser** stage in to
   something else

In Bash, this could be visualized as a pretty simple series of pipes:
`input | parser | output`.  However, unlike Bash, these stages are
fixed.  In other words, it's currently not possible to run stages in
a custom order or to create new, custom stages to do additional things
with the data.  There's a use case for being able to do that, and it may
become a feature in the future, but for now, this is sufficient.


### Default Plugins

This project ships three default (or reference) plugins, one for each
stage in a job.

#### glob

The `glob` plugin is an input plugin that reads all configuration files
it can find in a given path.  It then attempts to determine the
operating system based first on some (ostensibly sane) default patterns.
Custom patterns for detecting the OS are also permitted and can be
configured via YAML.  OS detection is important as some violations will
only affect certain operating systems (such as the optional NX-OS AES
encryption feature).

#### lineregex

The `lineregex` plugin is a parser that reads a list of regex-based rules
from files in a specified directory and iterates through every line of
every device's configuration to find violations.

#### text

The `text` plugin is an output plugin that takes the data from any
parser plugin and prints the results in a more human-readable format on
the terminal.

## Ideas for Plugins

There are quite a few plugins that I imagine working well.  This is an
unstructured dump of thoughts and ideas that may not even work or make
sense.

1: A `ciscoconfparse` parser plugin.  This could be useful for answering
   questions like "do all BGP peers have a password configured?"

2: A `batfish` parser plugin.  This can be useful for myriad questions.
   One potential issue here is that the way `nsa` currently works is
   one file at a time, and if you wanted to ask questions that involved
   multiple devices, then `nsa` would need some updates to its plugin
   API.

3: A `git` input plugin.  This would let someone get the configuration
   files directly from a Git repository (such as an `oxidized` backup).

4: An `ssh` input plugin.  This would allow someone to retrieve device
   configurations directly from devices, ensuring the latest copy is
   being analyzed.

5: An HTML output plugin.  This would allow someone to present a web
   page with pretty output.

6: A JSON output plugin.  This could allow someone to run `nsa` as a
   service with an API and web app in front of it, allowing on-demand
   analysis and results in a nice and pretty web UI.

7: An alternate RegEx-based parser (similar to `lineregex`) that instead
   stores and retrieves its rules in a database.  This could be useful
   when using `nsa` to build out a more fleshed out web app.

Finally, `nsa` isn't limited by just plugins.  The default
implementation is a CLI tool with a fixed data processing pipeline, but
it would be fairly trivial to extend and customize the implementation
while still taking advantage of existing plugins and libraries of
matches.

## Roadmap

A "roadmap" (in loosest terms possible) is presented below.  Really,
it's just a TODO list.  There are no dates associated.

### General

- update documentation with links to projects mentioned

### Requirements for Beta

- published to pypi
- change Settings() calls to a variable in nsa.settings
- ci pipeline
- >=75% test coverage
- fully documented code
- documentation on developing and using plugins
- logging
- support for warnings
- defined lifecycles
- GitHub projects, milestones, etc.
- `lineregex` plugin: support ignored device name patterns
