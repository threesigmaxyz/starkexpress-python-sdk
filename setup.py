from setuptools import setup, find_packages

from starkexpress import __version__

setup(
    name='starkexpress',
    version=__version__,
    author='StarkExpress Team',
    author_email='afonso@threesigma.xyz',
    description='Python SDK for StarkExpress',
    packages=find_packages(),
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
            'starkexpress-cli = starkexpress.cli.__main__:cli',
        ],
    },
)
