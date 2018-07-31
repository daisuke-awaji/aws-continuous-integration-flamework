#!/usr/bin/python
# -*- coding: utf-8 -*-

import yaml
import ruamel.yaml
import json
import base64
from urllib.parse import urljoin
from urllib.parse import urlencode
import urllib.request as urlrequest
import random
import os
import pytest


# Define a YAML reader for parsing Cloudformation to handle !Functions like Ref
def general_constructor(loader, tag_suffix, node):
    return node.value


ruamel.yaml.SafeLoader.add_multi_constructor(u'!', general_constructor)

# Define basic security globals
SECURE_PORTS = ['443', '22']

# Our DevSecOps Logic
yaml = open("template.yaml", "r+")
cfn = ruamel.yaml.safe_load(yaml)
print(cfn)


def test_default():
    assert cfn["AWSTemplateFormatVersion"] == '2010-09-09'