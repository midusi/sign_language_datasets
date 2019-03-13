from setuptools import find_packages, setup
REQUIRED_PACKAGES =[
    'scikit-video',
    'matplotlib',
    'gdown',
    'pathlib',
    'opencv-python',
    'tensorflow',   
]
setup(
    name='sign-language-datasets',
    version='0.0.1',
    author='pablo kepes',
    description=(
        'A single library to (down)load all existing sign language video datasets.'),
    license='GNU',
    keywords='sign-language',
    url='https://github.com/midusi/sign_language_datasets/',
    download_url='https://github.com/midusi/sign_language_datasets/tarball/0.1',
    packages=find_packages(),
    install_requires=REQUIRED_PACKAGES,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Manager'
    ]
)
