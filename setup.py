from setuptools import setup

setup(
    name='GameSelect',
    packages=['src'],
    include_package_data=True,
    install_requires=[
        'flask',
        'requests',
        'numpy',
    ],
)
