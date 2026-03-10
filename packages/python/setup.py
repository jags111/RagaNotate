"""
RagaNotate — Python Package Setup
github.com/jags111/RagaNotate
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="raganotate",
    version="0.1.1",
    author="Jags",
    author_email="info@revsmartasia.com",
    description="Full-Stack Carnatic Music Notation Engine — Lyrics to Playable Audio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jags111/RagaNotate",
    project_urls={
        "Bug Tracker": "https://github.com/jags111/RagaNotate/issues",
        "Changelog":   "https://github.com/jags111/RagaNotate/blob/main/CHANGELOG.md",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio :: MIDI",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.24",
        "scipy>=1.10",
    ],
    extras_require={
        "midi":    ["midiutil>=1.2"],
        "audio":   ["numpy>=1.24", "scipy>=1.10", "soundfile>=0.12"],
        "ai":      ["transformers>=4.30", "datasets>=2.14"],
        "dev":     ["pytest>=7.0", "ruff>=0.1", "mypy>=1.0"],
        "all":     ["midiutil>=1.2", "soundfile>=0.12",
                    "transformers>=4.30", "datasets>=2.14"],
    },
    entry_points={
        "console_scripts": [
            "raganotate=raganotate.__main__:main",
        ],
    },
)
