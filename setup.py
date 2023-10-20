from setuptools import setup, find_packages

from arc import __version__

package_name = 'arc'

setup(
    name=package_name,
    version=__version__,
    author='Arc Team',
    author_email='afonso@onarc.io',
    description='Python SDK for Arc',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'coincurve',
        'click',
        'ecdsa',
        'keyring',
        'mpmath',
        'pysha3',
        'sympy',
        'tabulate',
        'web3',
    ],
    entry_points={
        'console_scripts': [
            'arc-cli = arc.cli.__main__:cli',
        ],
    },
)
