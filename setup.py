import sys

from setuptools import setup, find_packages

if sys.version_info < (3, 8):
    raise RuntimeError('Your Python version {0} is not supported, please install '
                       'Python 3.8+'.format('.'.join(map(str, sys.version_info[:3]))))

requirements = [
    "aiohttp>=3.10.11,<4.0.0",
    "certifi>=2023.7.22",
    "ujson>=5.7.0",
    "pytz>=2022.7.1",
    "pyRFC3339>=1.1",
    "wheel>=0.38.4"
]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='aioabcpapi',
    version='2.2.0',
    author='bl4ckm45k',
    author_email='nonpowa@gmail.com',
    description='Асинхронная библиотека для ABCP API',
    long_description=long_description,
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
        'Programming Language :: Python :: 3.12',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    python_requires='>=3.10',
    keywords=['abcp', 'api', 'asyncio', 'aiohttp', 'async', 'wrapper'],
    project_urls={
        "Documentation": "https://www.abcp.ru/wiki/ABCP.API",
        "Issue Tracker": "https://github.com/bl4ckm45k/aioabcpapi/issues",
    },
)
