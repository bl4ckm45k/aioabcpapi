import sys

from setuptools import setup

#with open("README.md") as f:
#    long_description = f.read()
if sys.version_info < (3, 7):
    raise RuntimeError('Your Python version {0} is not supported, please install '
                       'Python 3.7+'.format('.'.join(map(str, sys.version_info[:3]))))
requirements = ["aiohttp>=3.8.1", "certifi>=2022.6.15", "ujson>=5.3.0", "pytz", "pyrfc3339"]

setup(
    name='aioabcpapi',
    version='1.0.3',
    author='bl4ckm45k',
    author_email='nonpowa@gmail.com',
    description='Async library for ABCP API',
    long_description_content_type="text/markdown",
    url="https://github.com/bl4ckm45k/aioabcpapi",
    license="MIT",
    packages=['aioabcpapi', 'aioabcpapi/cp', 'aioabcpapi/ts', 'aioabcpapi/utils'],
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Application Frameworks',

    ],
    python_requires='>=3.7'
)
