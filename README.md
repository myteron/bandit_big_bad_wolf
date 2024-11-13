# Bandit vulnerabilty test plugin template

Template for writing [bandit](https://bandit.readthedocs.io/en/latest/plugins/index.html#writing-tests) test plugins without the need to change the installed bandit module, a step by step guide, and unit-test.

## Introduction

Bandit supports writing plugins based on [stevedore extension manager](https://docs.openstack.org/stevedore/latest/reference/index.html#stevedore.extension.ExtensionManager). It also has some older non-plugin based code artefacts.

There are plugins for:

* namespace=`bandit.formatters`, to create custom reporting formats (not discussed, see [bandit-sarif-formatter](https://github.com/microsoft/bandit-sarif-formatter) for an example)
* namespace=`bandit.plugins`, to create your own vulnerability detection (discussed)

Plugins can either be:

* Created as part of bandit source code (not discussed, slightly different)
* Created as a sepearted module (discussed)

The bandit code also has some other interesting features that will not be discussed here at this moment such as:

* sphinx autodoc to generate the docs from docstring
* tox framework used to automate building and testing the project against different python versions
* AST

## Prerequisites

* Python 3
* bandit installed
* TODO: get full list of required modules

## Steps

1) Clone this repository and `cd` into it
2) pip install .
3) bandit examples/*

Expected outcome is one detected wolf with `test_id` B666. You can uninstall the plugin via `pip uninstall bandit_big_bad_wolf`.

## Files explained

| File| Description |
|:----|:----|
|[examples/big_bad_wolf.py](examples/big_bad_wolf.py)| Code example that we want to detect. In this case a mock up.|
|[bandit_big_bad_wolf/big_bad_wolf.py](bandit_big_bad_wolf/big_bad_wolf.py)| This is the actual test plugin for detecting the vulnerable code. The folder name `bandit_big_bad_wolf` represents the cutom plugin module that will be installed or uninstalled via `pip` as defined in `setup.py`|
|[tests/functional/test_big_bad_wolf.py](bandit_big_bad_wolf/big_bad_wolf.py)|This is to verify that the plugin code can detect the sample vulnerablity code. Setting a breakpoint in `bandit_big_bad_wolf/big_bad_wolf.py` allows to explorer more about how the plugin works.|

### TODO

Get the test to work without installing it
