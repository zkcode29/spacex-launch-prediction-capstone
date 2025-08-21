from setuptools import setup, find_packages

def get_requirements(file_path):
    """Reads the requirements from a given file."""
    with open(file_path, 'r') as f:
        requirements = f.read().splitlines()
    return requirements

setup(
    name='spacex_landing_prediction',
    version='0.1.0',
    description='A data science project to predict SpaceX Falcon 9 first stage landing success.',
    author='[Your Name]',
    author_email='[your.email@example.com]',
    url='https://github.com/[your-username]/spacex-landing-capstone',  # URL to your repository
    packages=find_packages(),  # Automatically find all packages in the project (i.e., 'src')
    install_requires=get_requirements('requirements/base.txt'),
    extras_require={
        'dev': get_requirements('requirements/dev.txt')
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)```
**Note:** Remember to replace the placeholder values: `[Your Name]`, `[your.email@example.com]`, and `[your-username]`. This `setup.py` file is configured to read your dependencies directly from your `requirements/` files, keeping everything consistent.

---

You have now populated every single file in your comprehensive project structure. Congratulations on building a professional, end-to-end data science project