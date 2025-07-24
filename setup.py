from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="media-processor",
    version="1.0.0",
    author="ebowwa",
    description="A unified tool for video and image processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ebowwa/media-processor",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.21.0",
        "opencv-python-headless>=4.5.0",
        "onnxruntime>=1.22.0",
        "Pillow>=9.0.0",
    ],
    entry_points={
        "console_scripts": [
            "media-processor=cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["models/*.ort"],
    },
)