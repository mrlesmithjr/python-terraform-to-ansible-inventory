from setuptools import setup
from setuptools import find_packages
import re

VERSIONFILE = "TerraformToAnsibleInventory/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='TerraformToAnsibleInventory',
      version=verstr,
      description='Consumes Terraform State and generates Ansible inventory.',
      url='https://github.com/mrlesmithjr/python-terraform-to-ansible-inventory',
      author='Larry Smith Jr.',
      author_email='mrlesmithjr@gmail.com',
      license='MIT',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=find_packages(),
      scripts=['bin/TerraformToAnsibleInventory'],
      include_package_data=True,
      install_requires=[
          'argparse', 'ast', 'python-consul', 'jinja2', 'PyYaml'
      ],
      classifiers=(
          "Programming Language :: Python :: 2",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ),
      zip_safe=False)
