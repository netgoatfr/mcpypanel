from setuptools import find_packages, setup, Command

with open("mcpypanel/__version__.py", "r") as f:
    exec(f.read())

setup(
    name='McPyPanel',
    version=__version__,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    license='',
    long_description=open('README.md').read(),
    include_package_data=True,
    scripts=["bin/mcwrapper"]
)