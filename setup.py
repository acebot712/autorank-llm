from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

# Read the contents of your requirements.txt file
with open('requirements.txt', encoding='utf-8') as f:
    required_packages = [
        line.strip() for line in f
        if line.strip() and not line.startswith('#')
    ]

setup(
    name='autorank-llm',
    version='0.2.0',
    author='Abhijoy Sarkar',
    author_email='abhijoy.sar@gmail.com',
    description='Automated ranking of Language Learning Models (LLMs) '
                'through recursive peer evaluation.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/acebot712/autorank-llm',
    project_urls={
        'Bug Tracker': 'https://github.com/acebot712/autorank-llm/issues',
        'Source Code': 'https://github.com/acebot712/autorank-llm',
    },
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=required_packages,
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
        ],
        'ollama': ['langchain-community>=0.0.38'],
        'openai': ['langchain-openai>=0.0.5'],
        'huggingface': ['langchain-huggingface>=0.0.1'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.8',
    keywords='llm evaluation ranking benchmarking ai machine-learning',
    license='Apache License 2.0',
)
