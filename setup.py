import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
        name="py-grammark",
        version="0.0.2",
        author="Thomas Osterland",
        author_email="highway.ita07@web.de",
        description="Checks to improve scientific writing. See https://github.com/markfullmer/grammark for more information.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/highkite/py-grammark",
        project_urls={
            },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            ],
        package_dir={"": "src"},
        include_package_data=True,
        packages=setuptools.find_packages(where="src"),
        python_requires=">=3.6",
        )
