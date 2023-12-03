from setuptools import setup, find_packages

# Read the contents of your requirements.txt file
with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

setup(
    name='autorank-llm',
    version='0.1.0',
    author='Abhijoy Sarkar',
    author_email='abhijoy.sar@gmail.com',
    description='Automated ranking of Language Learning Models (LLMs).',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/acebot712/autorank-llm.git',
    packages=find_packages(),
    install_requires=required_packages,
    classifiers=[
        # Choose the appropriate classifiers from https://pypi.org/classifiers/
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',  # Specify the Python versions you support here
)
