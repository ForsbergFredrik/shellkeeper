from setuptools import setup, find_packages

setup(
    name="shellkeeper",  # The name of your package
    version="0.1.0",  # Version of the package
    description="A CLI tool to manage shell commands",
    author="Fredrik",
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[
        "colorama",
        "inquirer",
    ],
    entry_points={
        'console_scripts': [
            'shellkeeper=shellkeeper.shellkeeper:main',  # CLI entry point
        ],
    },
    include_package_data=True,  # Include non-Python files (like README, etc.)
)
