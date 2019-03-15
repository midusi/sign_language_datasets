from setuptools import find_packages, setup

REQUIRED_PACKAGES =[
    'scikit-video',
    'matplotlib',
    'gdown',
    'pathlib',
    'opencv-python',
    'tensorflow',
]

project_urls={
    "Bug Tracker": "'https://github.com/midusi/sign_language_datasets/',issues",
    "Documentation": "'https://github.com/midusi/sign_language_datasets/wiki',",
    "Source Code": "'https://github.com/midusi/sign_language_datasets",
}

setup(
    name='sldatasets',
    version='0.0.1',
    author='Pablo Kepes and Facundo Quiroga',
    author_email="signlanguagedatasets@gmail.com",
    description=(
        'A single library to (down)load all existing sign language video datasets.'),
    license='GNU',
    keywords='sign-language sign language dataset download load video',
    project_urls=project_urls,
    packages=find_packages(),
    install_requires=REQUIRED_PACKAGES,
    #zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
