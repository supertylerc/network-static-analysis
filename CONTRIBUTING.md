# Contributing

There are a few ways to contribute!  This section is broken up into
two major parts: issues and pull requests.

Before that, though, the following applies to all contributions:

0: Please follow the Code of Conduct.
1: Ensure you're up-to-date and check the list of open issues and open
   pull requests.
2: I will attempt to respond to issues and pull requests in a timely
   (within 2-3 business days) manner.
3: Sometimes, an issue or pull request may be closed and/or rejected.
   When this happens, I will attempt to explain the reasoning
   adequately.  In all cases, please understand that it's never
   personal.

## Issues

"Issues" is a pretty generic category and applies to any of the
following (and more):

* A bug
* A security issue (see `SECURITY.md` first, please!)
* A feature request
* A question
* An RFC

When creating an issue, please ensure you're following the rules above
as well as the following issue-specific information.

### Bugs

During the alpha, before filing a bug report, please ensure you're
running the latest version (installed from the `master` branch).  Once
you've verified that, please open an issue describing your problem and
include any output that you received when you encountered the issue.

If you can, please provide a sample network device configuration file
(please sanitize it either manually or using a tool such as `netconan`)
as well as your `nsa.yml` file for `nsa`.

### Security Issues

Please see `SECURITY.md`.

### Feature Request

Please check both the open _and_ closed issues.  Sometimes, a feature
request will be made and, after some discussion, rejected.  Before
opening a feature request for a previously rejected feature, please
ensure that you understand the reasoning behind the previous rejection
and provide data explaining why it needs re-evaluation in your request.

### Questions and Inquiries

Just ask your question.  :)  Eventually, an FAQ may exist; however, for
now, just open an issue to ask your question, whatever it is.  Check the
open _and_ closed issues to see if your question has already been asked,
though, if you want to save yourself a little time.

Please include any information that may be relevant.

## Pull Requests

1: Any pull request must also have an issue associated with it.  This
   helps make it clear why the pull request is being submitted, what it
   solves, and provides contextual information for maintainers,
   contributors, and others six months after the PR was merged/closed.
2: If you want to potentially save yourself some time, if you're making
   a significant change, please submit an issue as an RFC before writing
   any code.  This will help the community collaborate on significant
   changes together while saving you from writing code that may
   ultimately not be accepted due to implementation concerns or
   different ideologies.
3: Understand and accept the License of this project.

> If you make contributions (investigated, written, or submitted) while
> on your employer's time, please be resonsible and understand the
> stance of that employer on Intellectual Property and contributions to
> open source projects, particularly regarding this project's License.
> It would be a serious bummer for the project and the community to be
> faced with IP infringement notices and have to try to remove code and
> functionality that belongs to another entity.

### Documentation

Experience Level: Beginner
Target Audience: End Users, Everyone

You can either submit documentation updates as pull requests or you can
write blogs about using the project.  Spread the word on Twitter (or
your social media platform of choice).

### Rules

Experience Level: Intermediate
Target Audience: End Users, Developers

One of the biggest areas that will help this project is contributing
rules for the default parser plugin\*.  To contribute a rule, it is
helpful to know the basics of YAML and regular expressions; however,
anyone who can copy and paste enough to get something working is welcome
to contribute!

> \*: If the community grows, this may change to be whatever parser
> plugin ends up being the "best" or "most common."

To contribute a rule, you'll need to do two things in addition to the
Common Contribution Guidelines:

1: Write the rule
2: Provide a configuration snippet that can be used to ensure the rule
   works as intended

### Code

Experience Level: Some Experience Writing Python
Target Audience: End Users, Developers

This is mostly a catch-all for anything that isn't documentation or
a rule.  See the Requirements for Beta in the README to see the areas in
most need of your contributions.  However, all contributions are
welcome, even if they aren't in direct support of the beta goals.
