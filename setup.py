import os
import os.path

from setuptools import find_packages, setup

classifiers = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Topic :: Scientific/Engineering",
    "Topic :: Software Development",
]


def run_setup():
    """Get version from git, then install."""
    # load long description from README.md
    readme_file = "README.md"
    if os.path.exists(readme_file):
        long_description = open(readme_file, encoding="utf-8", errors="ignore").read()
    else:
        print("Could not find readme file to extract long_description.")
        long_description = ""
    setup(
        name="mobile_robotics_python",
        version="1.0.0",
        install_requires=[
            "PyYAML",
            "pandas",
            "numpy",
            "matplotlib",
            "pytransform3d",
            "pitop",
        ],
        author="Ocean Perception - University of Southampton",
        author_email="miquel.massot-campos@soton.ac.uk",
        description="Base code for mobile robotics",  # noqa
        long_description=long_description,
        url="https://github.com/ocean-perception/mobile_robotics_python",
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        classifiers=classifiers,
        license="BSD",
        entry_points={  # Optional
            "console_scripts": [
                "mobile_robotics_python = mobile_robotics_python.cli:main",
            ],
        },
        include_package_data=True,
        package_data={
            "mobile_robotics_python": [
                "src/mobile_robotics_python/configuration/*.yaml",
            ]
        },
    )


if __name__ == "__main__":
    run_setup()
