from setuptools import setup, find_packages

setup(
    name="yandex-book-api",
    version="0.1.2",
    description="Pydantic wrapper for Bookmate API",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="stepan163s",
    author_email="stepan163s@yandex.ru",
    url="https://github.com/stepan163s/yandex-book-api",
    license="MIT",
    packages=find_packages(include=["yandex_book", "yandex_book.*"]),
    install_requires=[
        "pydantic>=2.0",
        "requests>=2.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    zip_safe=False,
)
