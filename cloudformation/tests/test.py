#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import ruamel.yaml

# Define a YAML reader for parsing Cloudformation to handle !Functions like Ref
def general_constructor(loader, tag_suffix, node):
    return node.value


ruamel.yaml.SafeLoader.add_multi_constructor(u'!', general_constructor)

# Define basic security globals
SECURE_PORTS = ['443', '22', '80']
# Define my ip
MY_IP = ['126.209.222.211/32', '126.236.39.24/32']

# Our DevSecOps Logic
base = os.path.dirname(os.path.abspath(__file__))
name = os.path.normpath(os.path.join(base, '../template.yaml'))
print(name)
yaml = open(name, "r+")
cfn = ruamel.yaml.safe_load(yaml)
print(cfn)


def test_default():
    """Test for default rule"""
    assert cfn["AWSTemplateFormatVersion"] == '2010-09-09'


def test_security_groups():
    """Test for security groups"""
    for resource in cfn['Resources']:
        # Test for Security Groups
        if cfn['Resources'][resource]['Type'] == '''AWS::EC2::SecurityGroup''':
            if 'SecurityGroupIngress' in cfn['Resources'][resource]['Properties']:
                for rule in cfn['Resources'][resource]['Properties']['SecurityGroupIngress']:

                    if 'CidrIp' in rule:
                        # Test that Security Group ports are only 22 or 443 or 80 if open to /0
                        if rule['FromPort'] == rule['ToPort']:
                            # If open to the public then FromPort in SECURE_PORTS
                            if rule['CidrIp'] == '0.0.0.0/0':
                                assert rule['FromPort'] in SECURE_PORTS
                                assert rule['ToPort'] in SECURE_PORTS
                            else:
                                assert rule['CidrIp'] in MY_IP


def test_assert_write_description():
    """Test for description. Is there an explanation written?"""
    for resource in cfn['Resources']:
        # Test for Security Groups
        if cfn['Resources'][resource]['Type'] == '''AWS::EC2::SecurityGroup''':
            if 'SecurityGroupIngress' in cfn['Resources'][resource]['Properties']:
                for rule in cfn['Resources'][resource]['Properties']['SecurityGroupIngress']:
                    assert 'Description' in rule
                    assert len(rule['Description']) > 0


def test_iam_policy_statement():
    """Test for IAM policy"""
    for resource in cfn['Resources']:
        if cfn['Resources'][resource]['Type'] == '''AWS::IAM::User''':
            if 'Properties' in cfn['Resources'][resource]:
                if 'Policies' in cfn['Resources'][resource]['Properties']:
                    for rule in cfn['Resources'][resource]['Properties']['Policies']:

                        for iam in rule['PolicyDocument']['Statement']:

                            if iam['Effect'] == 'Allow':
                                assert 'organizations:' not in iam['Action']
                                assert 'iam:' not in iam['Action']
                                assert '*' not in iam['Action'][0]



