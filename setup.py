from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='TerraformToAnsibleInventory',
      version='0.2.0',
      description='Generates Ansible inventory in YAML format by parsing the tfstate.',
      url='https://github.com/mrlesmithjr/python-terraform-to-ansible-inventory',
      author='Larry Smith Jr.',
      author_email='mrlesmithjr@gmail.com',
      license='MIT',
      packages=['TerraformToAnsibleInventory'],
      scripts=['bin/TerraformToAnsibleInventory'],
      include_package_data=True,
      install_requires=[
          'argparse', 'ast', 'jinja2', 'PyYaml'
      ],
      zip_safe=False)
