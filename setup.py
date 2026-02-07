from setuptools import setup

setup(
    name='semutils',
    version='0.0.1',
    py_modules=['csssem','csssem.cli','csssem.config'
                ],
    install_requires=[
        'Click', 'pandas', 'lxml','pyyaml', 'numpy','requests','html5lib','tabulate'
    ],
    entry_points={
        'console_scripts': [
            'csssem = csssem.cli:csssem_util',
        ],
    },
)
