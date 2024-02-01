from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name="gestureflow",  # Required
    version="0.0.3",  # Required

    description="A library for simplifying the development of gesture based application development",  # Optional

    long_description=long_description,  # Optional

    long_description_content_type="text/markdown",  # Optional (see note above)

    url="https://github.com/Jay7221/gestureflow",  # Optional

    author="Jay Shirgupe",  # optional
    author_email="jns29072003@gmail.com",  # optional

    classifiers=[  # optional
        # how mature is this project? common values are
        #   3 - alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 1 - Planning",

        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics :: 3D Modeling",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Scientific/Engineering :: Image Recognition",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="gesture detection, rapid gesture application development, mediapipe",  # Optional
    package_dir={"": "src"},  # Optional

    packages=find_packages(where="src"),  # Required

    python_requires=">=3.7, <4",
    install_requires=['opencv-python', 'mediapipe'],  # Optional

    extras_require={  # Optional
        "dev": ["check-manifest"],
        "test": ["coverage"],
    },
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    package_data={  # Optional
    },
    # Entry points. The following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={  # Optional
        "console_scripts": [
        ],
    },

    project_urls={  # Optional
        "Bug Reports": "https://github.com/Jay7221/gestureflow/issues",
        "Say Thanks!": "https://saythanks.io/to/jns29072003",
        "Source": "https://github.com/Jay7221/gestureflow",
    },
)
