from setuptools import find_packages, setup, Command

with open("src/mcpypanel/__version__.py", "r") as f:
    exec(f.read())
    
with open('requirements.txt') as f:
    required = f.read().splitlines()


##     packages=["mcpypanel","mcpypanel.*"],
## Packaes are managed by the src/ directory.

setup(
    name='McPyPanel',
    version=__version__,
    description="A panel for minecraft servers and proxy, doc at https://github.com/aGoatdev/mcpypanel",
    license='CC BY-SA',
    author="aGoatdev",
    author_email="crazytekno.py@gmail.com",
    long_description=open('README.md').read(),
    url="https://github.com/aGoatdev/mcpypanel", # Project Url
        entry_points={
        'console_scripts': [
            'mcpypanel = mcpypanel:main',
        ]
    }, # Start Script
    install_requires=required, # Requirements
    platforms="linux",
)