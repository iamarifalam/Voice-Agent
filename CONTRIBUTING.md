# Contributing to CallPilot Voice Ops

Thank you for your interest in contributing to CallPilot Voice Ops! This document provides guidelines and information for contributors.

## 🚀 Quick Start for Contributors

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
   ```bash
   git clone https://github.com/your-username/Voice-Agent.git
   cd Voice-Agent
   ```
3. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e .
   pip install pytest ruff httpx  # Development dependencies
   ```
4. **Run tests** to ensure everything works
   ```bash
   pytest tests/
   ```

## 🛠️ Development Workflow

### 1. Choose an Issue
- Check [GitHub Issues](https://github.com/iamarifalam/Voice-Agent/issues) for open tasks
- Look for issues labeled `good first issue` or `help wanted`
- Comment on the issue to indicate you're working on it

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description
```

### 3. Make Your Changes
- Follow the existing code style and architecture
- Add type hints for all new functions
- Write comprehensive tests for new functionality
- Update documentation as needed

### 4. Code Quality Checks
```bash
# Run tests
pytest tests/ -v

# Check code quality
ruff check src/ tests/

# Format code
ruff format src/ tests/

# Type checking (if mypy is available)
mypy src/
```

### 5. Commit Your Changes
```bash
git add .
git commit -m "feat: Add amazing new feature

- Detailed description of changes
- Reference to issue if applicable
- Breaking changes noted"
```

### 6. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```
Then create a Pull Request on GitHub with a clear description.

## 📝 Coding Standards

### Python Style
- Follow [PEP 8](https://pep8.org/) guidelines
- Use type hints for all function parameters and return values
- Maximum line length: 100 characters
- Use descriptive variable and function names

### Code Structure
- Keep functions small and focused (single responsibility)
- Use dataclasses for data models
- Separate business logic from API endpoints
- Add docstrings for complex functions

### Testing
- Write tests for all new functionality
- Aim for high test coverage (>90%)
- Use descriptive test names
- Test both happy path and error cases

## 🏗️ Architecture Guidelines

### Component Structure
- **API Layer** (`main.py`): FastAPI routes and request/response handling
- **Business Logic** (`orchestrator.py`): Core conversation and decision logic
- **Data Models** (`models.py`): Pydantic models and dataclasses
- **Knowledge Base** (`knowledge.py`): FAQ indexing and search
- **Telephony** (`telephony.py`): Twilio integration and TwiML generation
- **Monitoring** (`monitoring.py`): Metrics and health checks

### Adding New Features
1. **API First**: Design the API endpoints first
2. **Test Driven**: Write tests before implementation
3. **Modular**: Keep components loosely coupled
4. **Documented**: Update README and docstrings

## 🔧 Development Tools

### Required Tools
- Python 3.11+
- pip
- Git

### Recommended Tools
- **VS Code** with Python extension
- **Docker** for container testing
- **Postman** or **curl** for API testing

### Testing Tools
- **pytest**: Test framework
- **ruff**: Linting and formatting
- **mypy**: Type checking (optional)

## 🚨 Issue Reporting

When reporting bugs or requesting features:

1. **Check existing issues** first
2. **Use issue templates** when available
3. **Provide detailed information**:
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details
   - Error messages/logs

## 📚 Documentation

- **README.md**: Main project documentation
- **Code comments**: Explain complex logic
- **Docstrings**: Document function purpose and parameters
- **API docs**: Auto-generated from FastAPI

## 🎯 Areas for Contribution

### High Priority
- Multi-language support
- Advanced NLP model integration
- CRM system integrations
- Voice analytics and reporting

### Medium Priority
- Performance optimizations
- Additional test coverage
- Documentation improvements
- UI/UX enhancements

### Good for Beginners
- Bug fixes
- Test improvements
- Documentation updates
- Small feature enhancements

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Code Review**: All PRs receive detailed feedback

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the same MIT License that covers the project.

---

Thank you for contributing to CallPilot Voice Ops! Your efforts help make voice support automation better for everyone. 🚀