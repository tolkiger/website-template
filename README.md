# Website Template

A complete template for deploying static websites with AWS CDK.

## Quick Start

```bash
# Create a new website project
npx cdk init app --language=python --generate-only
# Then copy template files
```

## Project Structure

```
my-website/
├── site/                    # Next.js website
│   ├── app/                 # Next.js app directory
│   ├── public/              # Static assets
│   ├── package.json
│   └── next.config.js
├── infra/                   # CDK infrastructure
│   ├── app.py              # CDK app entry point
│   ├── requirements.txt     # Python dependencies
│   ├── cdk.json            # CDK configuration
│   └── shared_website_constructs/  # Shared constructs
└── .github/workflows/       # CI/CD workflows
```

## Getting Started

1. **Initialize a new project:**
   ```bash
   mkdir my-website && cd my-website
   npx cdk init app --language=python
   ```

2. **Copy template files:**
   - Copy the `site/` directory for Next.js app
   - Copy the `infra/` directory for CDK infrastructure
   - Copy shared constructs

3. **Configure your website:**
   - Update `infra/app.py` with your site name
   - Update `site/` with your Next.js app
   - Update `infra/cdk.json` with your AWS account info

4. **Deploy:**
   ```bash
   cd infra
   pip install -r requirements.txt
   cdk bootstrap
   cdk deploy
   ```

## Features

- ✅ Static website hosting with CloudFront + S3
- ✅ Custom domain support (Route 53 + ACM)
- ✅ CI/CD pipeline with GitHub Actions
- ✅ Menu PDF hosting (optional)
- ✅ Shared constructs for consistency
- ✅ Automated deployments

## Customization

1. **Domain Name:** Update `infra/app.py` with your domain
2. **Menu PDF:** Enable/disable menu PDF hosting
3. **Environment Variables:** Set in GitHub Secrets
4. **Custom Build:** Modify `site/package.json` for custom build steps

## Deployment

The template includes GitHub Actions for CI/CD. Push to main branch to deploy.

## License

MIT License