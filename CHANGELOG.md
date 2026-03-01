# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-28

### Added
- Initial website template implementation
- Thin `infra/app.py` that imports shared-website-constructs
- `infra/buildspec.yml` for CodeBuild (Node.js 20 + Python 3.12)
- `infra/requirements.txt` with shared-website-constructs dependency
- `infra/cdk.json` with CDK configuration
- Sample `site/out/index.html` placeholder page
- Environment variable handling for domain configuration
- Environment variable handling for menu PDF configuration
- Comprehensive README with usage instructions
- Support for with-domain and without-domain scenarios
- Support for Next.js static exports
- Menu PDF bucket support

### Features
- Minimal configuration (no CDK code to write)
- CI/CD ready with buildspec.yml
- Custom domain support (optional)
- Menu PDF bucket support (optional)
- Next.js compatible
