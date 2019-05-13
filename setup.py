from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='metaqc',
    version='1.2',
    description='Benchmarking for m6A-seq data analysis and quality control',
    long_description=readme(),
    classifiers = [
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: Academic Free License (AFL)',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python 3',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    url='https://github.com/Epigenomics-Lab/metaqc',
    author='Guoshi Chai',
    author_email='chaigsh@mail2.sysu.edu.cn',
    license='Academic Free License (AFL)',
    packages=find_packages(),
    scripts=['bin/metaqc'],
    include_package_data=True,
    zip_safe=False
    )

