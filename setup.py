import os
from setuptools import setup, find_packages
import layout_generator.about as about


here = os.path.abspath(os.path.dirname(__file__))

def load_requirements(path_dir=here, comment_char='#'):
    with open(os.path.join(path_dir, 'requirements.txt'), 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    requirements = []
    for line in lines:
        # filer all comments
        if comment_char in line:
            line = line[:line.index(comment_char)]
        if line:  # if requirement is not empty
            requirements.append(line)
    return requirements

setup(
    name="layout-generator",
    version=about.__version__,
    author=about.__author__,
    description='Layout dataset generator.',
    packages=find_packages(),
    install_requires=load_requirements(),
    extras_require={
        'doc': ['sphinx', 'recommonmark', 'sphinx-rtd-theme']
    },
    include_package_data=True,
    python_requires='>=3.6',
    entry_points={
        "console_scripts": ["layout_generator = layout_generator.print_cli:generate_from_cli"]},
)
