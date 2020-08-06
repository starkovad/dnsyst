from setuptools import setup, find_packages

with open('requirements.txt') as fp:
    install_requires = fp.read()

setup(
    name="dnsyst",
    version="0.0.1",
    packages=find_packages(),
    install_requires=install_requires,
)