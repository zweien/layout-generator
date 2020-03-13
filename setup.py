from setuptools import setup, find_packages

setup(
    name="layout-generator",
    version="0.1",
    author='Zweien',
    description='Layout dataset generator.',
    packages=find_packages(),
    install_requires=[
        'tqdm'
        'scipy',
        'configargparse==1.0'
        ]
    )