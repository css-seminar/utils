from setuptools import setup

setup(
    name='syscourseutils',
    version='1.0.8',
    py_modules=['csssem',
                ],
    install_requires=[
        'Click', 'pandas', 'lxml','pyyaml', 'numpy','requests','html5lib'
    ],
    entry_points={
        'console_scripts': [
            'csssem = csssem.cli:csssem_util',
        ],
    },
)
