from setuptools import setup, find_packages

setup(
    name="velocicode",
    version="0.6.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "pyyaml",
        "rich>=13.0.0",
        "psutil",
        "py-cpuinfo",
    ],
    entry_points={
        "console_scripts": [
            "velocicode=velocicode.main:main",
        ],
    },
)
