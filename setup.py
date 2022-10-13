from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

long_description = 'Calculate SDS and centiles using \
      UK-WHO, Down and Turner reference data. \
          This is official RCPCH software.'

setup(
    name='rcpchgrowth-python-cli',
    version='1.2.0',
    author='Simon Chapman, Marcus Baw',
    author_email='eatyourpeasapps@gmail.com',
    url='https://github.com/rcpch/rcpchgrowth-python-cli',
    description='Command Line Interface for RCPCHGrowth.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    entry_points={
            'console_scripts': [
                'rcpchgrowth=rcpchgrowth_python_cli.__main__:methods'
            ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        "Operating System :: OS Independent",
    ),
    keywords='RCPCHGrowth UK-WHO Down Turner Centile',
    install_requires=requirements,
    zip_safe=False
)
