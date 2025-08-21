from setuptools import setup, find_packages

def get_requirements(file_path: str) -> list[str]:
    """
    Reads a requirements file and returns a list of dependencies.
    This version correctly ignores comments and recursive requirements.
    """
    requirements = []
    with open(file_path, 'r') as f:
        for line in f:
            # Strip whitespace and ignore lines that are comments or empty
            line = line.strip()
            if line and not line.startswith('#'):
                # Ignore recursive requirements (like -r base.txt)
                if not line.startswith('-r'):
                    requirements.append(line)
    return requirements

# --- Project Metadata ---
NAME = 'spacex_landing_prediction'
VERSION = '0.1.0'
DESCRIPTION = 'An end-to-end data science project to predict SpaceX Falcon 9 first stage landing success.'
AUTHOR = 'Izaz khan'  
EMAIL = 'izaz10455@gmail.com' 
URL = 'https://github.com/zkcode29/spacex-launch-prediction-capstone' # This is correct

# --- Read the README for the long description ---
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# --- Setup Configuration ---
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    
    # Automatically find all packages (directories with __init__.py)
    packages=find_packages(),
    
    # Core dependencies for the project to run
    install_requires=get_requirements('requirements/base.txt'),
    
    # Extra dependencies for development (e.g., pip install .[dev])
    extras_require={
        'dev': get_requirements('requirements/dev.txt')
    },
    
    # Classifiers to help users find your project
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    
    python_requires='>=3.8',
)