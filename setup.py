import sys
from setuptools import setup

if sys.version_info < (3, 8):
    raise RuntimeError('Your Python version {0} is not supported, please install '
                       'Python 3.8+'.format('.'.join(map(str, sys.version_info[:3]))))
requirements = ["wheel", "aiohttp>=3.8.5", "certifi>=2023.7.22", "ujson>=5.8.0", "pytz>=2023.3", "pyrfc3339"]
setup(
    name='aioabcpapi',
    version='2.0.7',
    author='bl4ckm45k',
    author_email='nonpowa@gmail.com',
    description='Async library for ABCP API',
    long_description_content_type="text/markdown",
    url="https://github.com/bl4ckm45k/aioabcpapi",
    license="MIT",
    packages=['aioabcpapi', 'aioabcpapi/cp', 'aioabcpapi/ts', 'aioabcpapi/utils'],
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Application Frameworks',

    ],
    python_requires='>=3.8'
)
