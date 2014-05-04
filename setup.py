from setuptools import setup, find_packages
setup(
    name = "rivalctl",
    version = "0.1",
    packages = find_packages(),
    scripts = ['bin/rivalctl'],

    # metadata for upload to PyPI
    author = "Andre P. LeBlanc",
    author_email = "andrepleblanc@gmail.com",
    description = "A tool to configure the SteelSeries Rival Gaming Mouse",
    license = "GPL2",
    keywords = "steelseries rival",
    url = "https://github.com/andrepl/rivalctl/",
    install_requires=[
        'ioctl-opt>=1.2',
        'pyudev>=0.16',
        'webcolors>=1.4'
    ],
)