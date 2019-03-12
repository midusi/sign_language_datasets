from setuptools import find_packages, setup

setup(
    name='sign-language-datasets',
    version='0.0.1',
    author='pablo kepes',
    description=(
        'A single library to (down)load all existing sign language video datasets.'),
    license='BSD',
    keywords='sign-language',
    url='',
    packages=find_packages(),

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Manager'
    ]
)
