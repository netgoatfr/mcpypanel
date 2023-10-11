from setuptools import find_packages, setup, Command

with open("mcpypanel/__version__.py", "r") as f:
    exec(f.read())
    
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='McPyPanel',
    version=__version__,
    description="A panel for minecraft servers and proxy, doc at https://github.com/aGoatdev/mcpypanel",
    packages=["mcpypanel"],
    license='CC BY-SA',
    author="aGoatdev",
    author_emaik="crazytekno.py@gmail.com",
    long_description=open('README.md').read(),
    url="https://github.com/aGoatdev/mcpypanel", # Project Url
    scripts=["bin/mcpypanel"], # Start Script
    install_requires=required, # Requirements
    platforms="linux",
)