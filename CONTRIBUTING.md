# Contributing to KDD

First of all, a big thank you for considering to contribute to this repository!

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [I Have a Question](#i-have-a-question)
- [I Want To Contribute](#i-want-to-contribute)
  - [Legal Notice](#legal-notice)
  - [Reporting Errors](#reporting-errors)
  - [Fixing Errors](#fixing-errors)
  - [Suggesting Enhancements](#suggesting-enhancements)
- [Styleguides](#styleguides)
  - [Commit Messages](#commit-messages)

## Code of Conduct

This project and everyone participating in it is governed by the
[Code of Conduct](CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code. Please report unacceptable behavior
to Melanie Bianca Sigl or Dominik Probst. Contact information can be found on the
[homepage of the Chair of Computer Science 6][cs6-homepage]

## I Have a Question

> Before asking a question, make sure that you have read all available documentation.

For example, answers to your questions may be contained in the [README](README.org), in existing
[Issues](/issues), or in our [StudOn][studon] course (access only for enrolled students at the
Friedrich-Alexander-Universität Erlangen-Nürnberg).

If you then still feel the need to ask a question or need clarification, we recommend the following:

- Open an [Issue](/issues/new).
- Provide as much context as you can about what your problem.

We will then take care of the issue as soon as possible.

## I Want To Contribute

### Legal Notice

When contributing to this project, you must agree that you have authored 100% of the content, that
you have the necessary rights to the content and that the content you contribute may be provided
under the project license.

### Reporting Errors

We are grateful for any information about errors in our documents. However, uncharacteristically for
a GitHub project, we would ask that errors be reported via our [StudOn][studon] course, as that is
where students report bugs who are not familiar with GitHub. This way we have a central collection
point for bugs. If you are not a registered student at the Friedrich-Alexander-Universität
Erlangen-Nürnberg and therefore do not have access to StudOn, we will of course also accept reports
via a new [Issue](/issues/new).

#### Before Reporting an Error

A good bug report shouldn't leave others needing to chase you up for more information. Therefore,
we ask you to investigate carefully, collect information and describe the issue in detail in your
report. Please complete the following steps in advance to reporting an error:

- Make sure that you are looking at the latest version.
- Take a look at the existing [Issues](/issues/new) and check if a corresponding report already exists.
- Collect sources to prove that it is an error (e.g. dictionary entry for a spelling mistake or
scientific source for a content error)

#### Reporting an Error

To report an error via GitHub, please follow these steps:

- Open a new [Issue](/issues/new).
- Describe the error in detail by providing information on:
  - Name of the document containing the error.
  - Description of the error.
  - Proof of it being an error (see previous section).
  - _Optional:_ Suggestion for improvement
- Label the issue as `error-report` and depending on the scope as `lecture`, `exercise` or `documentation`.
- _Optional:_ Assign the person responsible for files you found the error in (see [README](README.org))

### Fixing Errors

Besides reporting errors, there is also the possibility to correct errors yourself. Even if we are
very grateful about reported errors, the independent correction of errors is of course preferred.

#### Before Fixing an Error

Preparation is essential for independent correction. Please complete the following steps in
advance:

- Take a look at the open [Pull Requests](/pulls) and check that there is no fix for the error already pending.
- Collect sources to prove that the error is an error (e.g. dictionary entry for a spelling mistake or
scientific source for a content error).
- Read the [Styleguides](#styleguides).

#### Fixing an Error

To fix an error, please follow these steps:

- Fork our repository.
- Make sure that your fork is on the latest version of our `dev` branch.
- Commit your fixes based on your fork of the `dev` branch while complying to the [Styleguides](#styleguides) (we recommend using a feature branch).
- Ideally, your PR contains only *one commit*.
- Open a new [Pull Requests](/pulls) (PR) requesting to merge your fixes into our `dev` branch.
- Make sure that there are no merge commits included in your PR.
- _Optional:_ Request a review by the person responsible for files you changed (see [README](README.org))

### Suggesting Enhancements

In addition to tips or fixes regarding errors, we are also happy to receive suggestions for enhancement.
We primarily collect these tips via our [StudOn][studon] course, although people without access
to the course are also welcome to use GitHub [Issues](/issues/new).

#### Before Submitting an Enhancement Suggestion

- Make sure that you are looking at the latest version.
- Take a look at the existing [Issues](/issues/new) and check if a corresponding suggestion already exists.
- Collect related sources if the suggestion is content based

#### Submitting an Enhancement Suggestion

To submit an enhancement suggestion via GitHub, please follow these steps:

- Open a new [Issue](/issues/new).
- Describe the suggestion in detail.
- Label the issue as `enhancement-suggestion` and depending on the scope as `lecture`, `exercise` or `documentation`.
- _Optional:_ Assign the person responsible for the topics that your proposed change concerns (see [README](README.org))

## Styleguides
### Commit Messages
When committing to this repository, make sure that commit messages follow these guidelines:

- Commit messages should follow our prefix scheme
_(e.g. "lecture-[xxx]: [description of the changes]" or "exercise-[xxx]: [description of the changes]")_
- Commit messages should clearly describe what has been changed
_(e.g. "lecture-prologue: fixed two typos on slide 15" instead of "lecture: fixed some stuff")_

## Attribution
This guide is very vaguely based on a CONTRIBUTING.md generated with the [contributing-gen][cg].

[cs6-homepage]: https://www.cs6.tf.fau.eu/chair/staff/
[studon]: https://www.studon.fau.de/
[cg]: https://bttger.github.io/contributing-gen-web/#
