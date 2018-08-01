# Cloudformation / AWS

Use Cloudformation to build resources into the AWS cloud.
You can change various parameters by editing the template, and you can deploy new AMI to the Auto Scaling Group.


## Test

Let's keep the quality and security level constant by writing test code against Cloudformation source code so that you write test code for your application.

For example, if you create a security group, you can raise the security level by setting a security policy such as unnecessary ports other than ['443', '22'] are free.

```
$ pwd
~/aws/cloudformation

$ pytest tests/test.py
============================================================== test session starts ==============================================================
platform darwin -- Python 3.6.0, pytest-3.7.0, py-1.5.4, pluggy-0.7.1
rootdir: /Users/daisuke/work/aws/cloudformation, inifile:
collected 1 item

tests/test.py .                                                                                                                           [100%]

=========================================================== 1 passed in 0.22 seconds ============================================================
```
