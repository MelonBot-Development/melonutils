import pathlib

from setuptools import setup, find_packages

ROOT = pathlib.Path(__file__).parent

with open(ROOT / "README.md", "r", encoding="utf-8") as f:
    _long_description = f.read()
    
setup(
    name="melonutils",
    version="0.1.0",
    # if you want a cleaner versioning use the things below
    # setup_requires=['setuptools_scm'],
    # intall_requires=['setuptools_scm'],
    # use_scm_version={'write_to': 'melonutils/version.txt'},
    description="A collection of utilities for redbots, specially melon",
    long_description=_long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MelonBot-Development/melonutils",
    project_urls={
        "Code": "https://github.com/MelonBot-Development/melonutils",
        "Issue tracker": "https://github.com/MelonBot-Development/melonutils/issues"
    },
    author="Lemon Rose",
    author_email="support@melonbot.io",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Utilities",
    ],
    test_suite="tests",
    # include_package_data: to install data from MANIFEST.in
    include_package_data=True,
    zip_safe=False,
)
