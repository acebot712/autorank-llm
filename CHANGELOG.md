# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2024-01-XX

### Changed
- **BREAKING**: Updated to modern langchain structure (langchain-community, langchain-openai, langchain-huggingface)
- Drastically reduced dependencies from 130 to ~2 core packages
- Improved test coverage from 57% to 100% with properly mocked tests
- Made stub features raise NotImplementedError instead of returning fake data
- Updated setup.py with proper classifiers and extras_require
- Fixed API inconsistencies between test.py and README examples

### Added
- GitHub Actions CI/CD pipeline for automated testing
- CONTRIBUTING.md with detailed contribution guidelines
- MANIFEST.in for proper package distribution
- Comprehensive test suite with 23 passing tests
- Badges in README for CI status, Python version, and license
- Support for Python 3.8-3.12

### Fixed
- All 23 unit tests now pass (previously 6 failing)
- Removed misleading documentation about unimplemented features
- Fixed line-too-long PEP 8 violations
- Corrected python_requires from 3.6 to 3.8
- Fixed README examples to match actual API

### Removed
- 120+ unnecessary dependencies (jupyter, cohere, gpt4all, etc.)
- Misleading "implemented" stubs for distributed evaluation, bias analysis, etc.

## [0.1.0] - 2023-12-XX

### Added
- Initial release
- Basic recursive peer evaluation system
- Support for Ollama, OpenAI, and HuggingFace backends
- Plugin system for custom metrics
- Explainability logging

[0.2.0]: https://github.com/acebot712/autorank-llm/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/acebot712/autorank-llm/releases/tag/v0.1.0
