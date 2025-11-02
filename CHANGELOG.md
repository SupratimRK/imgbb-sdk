# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release preparation

## [1.0.0] - 2025-11-03

### Added
- Initial release of imgbb-sdk
- `imgbb_upload()` function for uploading images to ImgBB API
- Support for multiple input formats:
  - File paths (str)
  - Image URLs (str)
  - Raw bytes
  - File-like objects (BinaryIO)
- Optional parameters:
  - `name`: Custom name for uploaded images
  - `expiration`: Auto-deletion time (60-15552000 seconds)
- Comprehensive error handling with custom exceptions:
  - `ImgBBError`: Base exception class
  - `ImgBBValidationError`: Input validation errors
  - `ImgBBAPIError`: API-related errors
  - `ImgBBTimeoutError`: Timeout errors
- Full type hints support with TypedDict for responses
- Support for all major image formats:
  - JPEG/JPG
  - PNG
  - GIF (including animated)
  - BMP
  - WEBP
- Comprehensive validation:
  - API key validation
  - File size validation (max 32MB)
  - Image format validation
  - Expiration range validation
- 30-second timeout for uploads
- Base64 encoding for image data
- URL passthrough for image URLs
- Complete test suite:
  - Unit tests with mocking
  - Integration tests
  - 100% code coverage
- GitHub Actions CI/CD:
  - Automated testing on Python 3.8-3.12
  - Code quality checks (black, ruff, mypy)
  - Security scanning
  - Automated PyPI publishing on releases
- Comprehensive documentation:
  - README with usage examples
  - API reference
  - Framework integration examples (Flask, Django, FastAPI)
  - CLI script example
  - Contributing guidelines
  - Type stubs for IDE support

### Dependencies
- requests >= 2.25.0
- typing-extensions >= 4.0.0 (Python < 3.11)

### Development Dependencies
- pytest >= 7.0.0
- pytest-cov >= 4.0.0
- pytest-mock >= 3.10.0
- requests-mock >= 1.9.0
- black >= 23.0.0
- mypy >= 1.0.0
- ruff >= 0.1.0
- types-requests >= 2.25.0

## [0.1.0] - 2025-11-02

### Added
- Initial development version
- Basic project structure
- Core upload functionality

---

## Version History

### [1.0.0] - 2025-11-03
First stable release with full functionality, comprehensive testing, and documentation.

### [0.1.0] - 2025-11-02
Initial development version.

---

## Links

- [PyPI Package](https://pypi.org/project/imgbb-sdk/)
- [GitHub Repository](https://github.com/SupratimRK/imgbb-sdk)
- [Issue Tracker](https://github.com/SupratimRK/imgbb-sdk/issues)

---

## Notes

### Semantic Versioning
This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR** version: Incompatible API changes
- **MINOR** version: Backwards-compatible new features
- **PATCH** version: Backwards-compatible bug fixes

### Change Categories
- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Vulnerability fixes
