from setuptools import setup, find_packages

def _requires_from_file(filename):
    packages = [p.strip() for p in open(filename).readlines()]
    return packages

setup(
      name='pyTAIL',
      version='0.0',
      packages=find_packages(where='pyTAIL'),
      package_dir={'':'pyTAIL'},
      include_package_data=True,
      install_requires=_requires_from_file('requirements.txt')
)