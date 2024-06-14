from setuptools import find_packages, setup, Command

with open("mcpypanel/__version__.py", "r") as f:
    exec(f.read())
    
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='mcpypanel',
    version=__version__,
    description="A panel for minecraft servers and proxy, doc at https://github.com/netgoatfr/mcpypanel",
    license='CC BY-SA',
    author="netgoatfr",
    author_email="netgoatfr@gmail.com",
    packages=find_packages(include=['mcpypanel', 'mcpypanel*']),
    long_description=open('README.md').read(),
    url="https://github.com/netgoatfr/mcpypanel", # Project Url
    entry_points={
        'console_scripts': [
            'mcpypanel = mcpypanel:main',
        ]
    }, # Start Script
    install_requires=required, # Requirements
    platforms="linux",
)
print(BANNER)