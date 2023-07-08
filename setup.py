from setuptools import setup, find_packages

setup(
    name="tetris-app",
    version="1.0.1",
    license="MIT",
    author="kinburrr",
    author_email="kinburrr@gmail.com",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "kintetris=tetris:__main__",
        ],
    },
    setup_requires=[
        "PyQt5~=5.15.7",
    ],
    include_package_data=True,
)
