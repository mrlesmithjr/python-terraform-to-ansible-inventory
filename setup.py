from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='TerraformToAnsibleInventory',
      version='0.2.3',
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
