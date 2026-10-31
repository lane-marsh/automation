from pathlib import Path

from setuptools import find_packages, setup


setup(
    name="lane-automation",
    version="0.1.0",
    description="Practical automation tools and utilities",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    packages=find_packages(include=["lane_automation", "lane_automation.*"]),
    py_modules=["dataCrunch", "ml_objects", "poker"],
    install_requires=["openpyxl>=3.0"],
    entry_points={
        "console_scripts": [
            "lane-tools=lane_automation.cli:main",
        ],
    },
)
