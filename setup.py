from setuptools import find_packages, setup


setup(
    name="nsa",
    version="0.0.1",
    description="Network Static Analysis",
    author="Tyler Christiansen",
    author_email="code@tylerc.me",
    url="https://github.com/supertylerc/network-static-analysis",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
    ],
    platforms=["Any"],
    scripts=[],
    provides=["nsa"],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "nsa.plugin.default": [
            "glob = nsa.plugin.input:GlobInput",
            "lineregex = nsa.plugin.parser:LineRegexParser",
            "text = nsa.plugin.output:TextOutput",
        ],
        "console_scripts": ["nsa = nsa.cli.main:main"],
    },
    zip_safe=False,
)
