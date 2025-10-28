# Deployment Guide for AutoRank-LLM

## Pre-Deployment Checklist

- [x] All 23 tests passing
- [x] Dependencies reduced from 130 to 2
- [x] Modern packaging with pyproject.toml
- [x] GitHub Actions CI/CD configured
- [x] Documentation complete and accurate
- [x] CHANGELOG.md updated
- [x] CONTRIBUTING.md created

## Publishing to PyPI

### 1. Test Build Locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install build twine
python -m build
```

This will create:
- `dist/autorank_llm-0.2.0-py3-none-any.whl`
- `dist/autorank-llm-0.2.0.tar.gz`

### 2. Test Upload to Test PyPI (Optional but Recommended)

```bash
python -m twine upload --repository testpypi dist/*
```

Test installation:
```bash
pip install --index-url https://test.pypi.org/simple/ autorank-llm
```

### 3. Upload to PyPI

```bash
python -m twine upload dist/*
```

You'll need your PyPI API token. Set it in `~/.pypirc`:

```ini
[pypi]
username = __token__
password = pypi-...your-token-here...
```

### 4. Create GitHub Release

```bash
git add .
git commit -m "Release v0.2.0: Production-ready HN launch

- Reduced dependencies from 130 to 2 core packages
- Fixed all broken tests (23/23 passing)
- Updated to modern langchain structure
- Added comprehensive CI/CD
- Honest documentation without vaporware features"

git tag -a v0.2.0 -m "Version 0.2.0: Production-ready"
git push origin main --tags
```

Then create a GitHub release at:
https://github.com/acebot712/autorank-llm/releases/new

Use tag `v0.2.0` and copy content from CHANGELOG.md

### 5. Verify Installation

```bash
pip install autorank-llm
python -c "from autorank_llm import LLMEvaluator; print('Success!')"
```

## Post-Deployment

### Monitor CI/CD

Check that GitHub Actions are running:
https://github.com/acebot712/autorank-llm/actions

### Update Documentation

Once on PyPI, update README to show:
```bash
pip install autorank-llm
```

### Social Media / HN Post

**Suggested HN Title:**
"AutoRank-LLM: Rank LLMs through recursive peer evaluation"

**Suggested HN Post:**
```
Hi HN! I built AutoRank-LLM, a Python package that automatically ranks LLMs using recursive peer evaluation.

Instead of human benchmarks, models evaluate each other's responses. Evaluations are weighted by each model's current skill level, creating a dynamic ranking that converges over multiple rounds.

Key features:
- Works with Ollama, OpenAI, HuggingFace
- Complete audit trail of all evaluations
- Extensible plugin system
- 23/23 tests passing, 2 core dependencies

GitHub: https://github.com/acebot712/autorank-llm
PyPI: pip install autorank-llm

I'd love feedback on the approach! The idea is that models can identify quality responses better than static benchmarks capture.
```

## Troubleshooting

### Build fails
```bash
rm -rf dist build *.egg-info
python -m build
```

### Import errors after install
Verify dependencies:
```bash
pip list | grep langchain
```

### Tests fail in CI
Check Python version matrix in `.github/workflows/ci.yml`

## Next Steps After Launch

1. Monitor GitHub issues and respond within 24 hours
2. Watch PyPI download statistics
3. Collect feedback for v0.3.0 features
4. Consider implementing roadmap items based on demand
