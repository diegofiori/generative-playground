from setuptools import setup, find_packages

setup(
    name='code_reviewer',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'openai',
        'pycodestyle',
        'PyGithub',
        'pylama',
        'pylint',
    ],
    entry_points={
        'console_scripts': [
            'code_reviewer=code_reviewer.cli:main',
        ],
    },
)