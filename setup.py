import os
import pathlib
from setuptools import setup, find_packages
import layout_generator.about as about


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")


def load_requirements(path_dir=here, comment_char="#"):
    with open(os.path.join(path_dir, "requirements.txt"), "r") as file:
        lines = [line.strip() for line in file.readlines()]
    requirements = []
    for line in lines:
        # filer all comments
        if comment_char in line:
            line = line[: line.index(comment_char)]
        if line:  # if requirement is not empty
            requirements.append(line)
    return requirements


setup(
    name="layout-generator",
    version=about.__version__,
    author=about.__author__,
    author_email="weienzhou@outlook.com",
    url="http://github.com/zweien/layout-generator",
    license=about.__licence__,
    description=about.__desp__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=load_requirements(),
    extras_require={
        "doc": ["sphinx", "recommonmark", "sphinx-rtd-theme"],
        "dev": [
            "pytest>=3.6",
            "pytest-shell",
            "pytest-cov",
            "codecov",
            "bump2version",
        ],
    },
    include_package_data=True,
    python_requires=">=3.6",
    entry_points={
        "console_scripts": ["layout_generator = layout_generator.cli:main",]
    },
)
