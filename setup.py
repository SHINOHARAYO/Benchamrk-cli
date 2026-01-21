from setuptools import setup, find_packages

setup(
    name="benchmark-cli",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "benchmark-cli=benchmark_cli.main:main",
        ],
    },
)
