# History

Originally, some tooling was built using Ansible to attempt to satisfy
this need for network device configuration data.  However, as I was
working through the problem, I found myself discovering new project
goals that were a challenge to implement in Ansible.  So, from that,
I began looking to see if perhaps someone had already done what I
wanted, which ultimately was to grep for regular expressions in a file.
To that end, I found [`graudit`](https://github.com/wireghoul/graudit),
a simple, barebones tool that looks for patterns in files and prints
a message to the terminal when one is found.  However, it didn't have
some of the features I wanted.

I went back to the drawing board and came up with the following features
that I personally wanted in such a tool:

1: Process a configuration file retrieved from disk and search for
   regular expressions line-by-line.  This was the most basic need and
   was supported by `graudit`.
2: Contain minimal dependencies.  `graudit` did this perfectly, and I
   loved it and wanted to stick to that as much as possible.
3: Print reports to the terminal (and, perhaps one day, render them as
   HTML) with additional metadata, such as a score for the violation,
   a link to a Wiki for more details about the violation, and a brief
   reason explaining why it was a problem.  This was a shortcoming of
   `graudit` that I _probably_ could have worked around with quite a bit
   of stitching tools together, but I wanted to avoid that if possible.
4: Ship a "standard library" of checks to which a community could
   contribute while allowing for custom libraries for those that could
   not share certain checks/data.  From my (admittedly brief) time
   evaluating `graudit`, it probably could've managed this "ok-ish", but
   not in a way I was particularly thrilled with.  Especially when
   needing support for #3 above.

So, I set out to build this tool.  I did a quick prototype in ~185 lines
of Python, including imports, blank lines, line breaks for readability,
and so on.  This implementation also only had two dependencies, and
neither dependency had any additional dependencies.  In fact, I could
have removed one of them without increasing complexity or introducing
bugs.  Once I had a working prototype, though, I knew I wanted more.

> I considered writing all of this with `py.test` in mind.  However, I
> ultimately feel like the amount of wiring and extra work required to
> appeal to developers and non-developers alike was just too much.  That
> said, I'll likely be looking into a way to integrate `py.test` at some
> point.

### Current Design

`nsa` is broken into three stages that run sequentially:

1: **Input**: Obtain configuration data and detect the OS
2: **Parser**: Go through the configuration data and look for violations
3: **Output**: Transform the results from the **Parser** stage in to
   something else

In Bash, this could be visualized as a pretty simple series of pipes:
`input | parser | output`.

Once I was able to break these pieces out and appropriately visualize
them, I considered what it meant to have either a terminal outputter or
an HTML outputter.  I had written plugins for other software before, and
I've even written plugin systems from scratch for other projects in the
past, so this seemed like a logical solution.  Not wanting to roll my
own plugin architecture, I looked to see what was out there and found
two primary contenders: `yapsy` and `stevedore`.  Both projects have
plenty of adoption.  I had never used either project.  I picked one
(`stevedore`) and started prototyping.  I honestly intended to come back
to `yapsy` and give it a go to see which I liked better, but I honestly
enjoyed `stevedore` so much that I decided to stick with it.  With the
backing of the OpenStack community, I also knew I could count on it to
be rock-solid.

After deciding that my output stage needed to be a plugin, I evaluated
the value of making the input and parser stages plugin-based.
Ultimately, I determined that, as an open source project developed in my
spare time, it was pretty likely that _something_ wasn't going to fit
someone's needs -- and that someone might even be me in the future!  I
wanted to build something simple and stable that non-developers could
use but that developers could extend if necessary.  For example, my
personal use case is to obtain the configuration data from disc.
However, I could also see a use case for retrieving the configuration
data directly from the device on every run.  I didn't want to write the
code to do that for a lot of reasons (primarily due to having to support
a potentially complex feature with many dependencies that I wouldn't
even use).  So I decided that the input stage should be plugin-based,
too.

Why not the parser stage too, then?  There's a pretty cool package
called `ciscoconfparse` that I could definitely see as a parser
implementation, and it's one I really want to write and use, too!  With
a parser plugin based on that, I could actually determine more granular
data than my reference parser, such as "Do all BGP neighbors have
authentication configured?"  That would be difficult to implement with a
simple line-by-line regex implementation, but it would be much easier
with `ciscoconfparse`.  However, I believe that a regex-based parser
will be the easiest to contribute to, and I think it will be able to
cover the vast majority of the use cases.  Of course, if I determine
that to be false, I can easily swap in for a different plugin!

With a basic skeleton wired up with a lot of static information, I knew
I needed to implement a way to configure a given run.  For this, I
turned to YAML.  I picked `ruamel.yaml` as my YAML parser; `pyyaml` is
a highly popular library used by many projects (such as Ansible);
however, I have some personal reasons for not using it, and on the
technical side, it is behind `ruamel.yaml` in terms of standards
support.

### Plugin API and Data Validation

With a plugin-based architecture that was open for third-party plugins,
I knew I needed a few things.  First, I needed to define the plugin API.
That is, what methods were required to be implemented by plugin authors,
and what information did they need to accept and return?

To help me here, I decided to look for a tool like `jsonschema` or
`yamale` but simpler.  For one, I didn't want to constantly serialize
data between the plugins\*; for another, I didn't want to bring in the
dependencies of either of those projects (for example, `yamale` uses
`pyyaml`, and I had already decided to use `ruamel.yaml`).

> \*: Serializing the data would have allowed me to take an Ansible-like
> approach, allowing plugins to be written in any language; however, I
> didn't really see this as a huge draw for such a niche tool.
> Additionally, a future goal is to de-couple the plugin chain such that
> plugins could be called individually, getting their required inputs
> from stdin, which would allow for a `stdin` and/or `stdout` plugin to
> handle serializing the data for such a (perceived) edge case.

This lead me to `schema`.  `schema` allows you to write a schema in
Python for native Python data structures and code without serializing to
an alternate format (such as JSON or YAML).  It's not as nice as the
YAML and JSON alternatives, but it does the job well enough for it to be
useful.  So, each plugin must return its data according to the
established schema.  This data is validated against the schema after
it's returned without the plugin author having to implement this logic.
This makes it easier for multiple plugins from multiple authors to work
together seamlessly, with each author (as well as end users!) knowing
that they are completely compatible with each other since they're all
constrained by the same schemas (depending on the stage).
