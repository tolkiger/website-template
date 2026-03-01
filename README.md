# Website Template

Minimal template for creating new websites using the shared-website-constructs library.

## Overview

This template provides a thin wrapper around the `shared-website-constructs` package, allowing you to deploy static websites to AWS with minimal configuration. All infrastructure logic is handled by the shared construct library.

## Features

- **Minimal Configuration**: Just environment variables, no CDK code to write
- **Shared Infrastructure**: Uses battle-tested `shared-website-constructs` library
- **CI/CD Ready**: Includes `buildspec.yml` for AWS CodeBuild
- **Custom Domains**: Optional Route 53 + ACM certificate support
- **Menu PDF Support**: Optional public S3 bucket for PDF files
- **Next.js Compatible**: Build and deploy Next.js static exports

## Structure

```
website-template/
├── site/
│   └── out/
│       └── index.html          # Sample placeholder (replace with your content)
├── infra/
│   ├── app.py                  # Thin CDK entry point
│   ├── cdk.json                # CDK configuration
│   ├── buildspec.yml           # CodeBuild instructions
│   └── requirements.txt        # Python dependencies
└── README.md
```

## Quick Start

### 1. Copy This Template

```bash
# Create new website from template
cp -r website-template my-new-website
cd my-new-website
```

### 2. Add Your Content

Replace `site/out/index.html` with your website content:

**Option A: Static HTML**
```bash
# Just replace the placeholder HTML
echo "<h1>My Website</h1>" > site/out/index.html
```

**Option B: Next.js Application**
```bash
# Create Next.js app in site/ directory
cd site
npx create-next-app@latest . --typescript --tailwind --app --no-src-dir
# Configure next.config.ts for static export
# Run npm run build to generate site/out/
```

### 3. Deploy Locally (Optional)

```bash
# Set environment variables
export SITE_NAME="my-website"
export DOMAIN_NAME=""  # Empty for no custom domain
export HOSTED_ZONE_ID=""
export HOSTED_ZONE_NAME=""
export MENU_PDF_ENABLED="false"
export MENU_PDF_BUCKET_NAME=""
export MENU_PDF_FILENAME=""

# Install dependencies and deploy
cd infra
pip install -r requirements.txt
cdk bootstrap  # First time only
cdk deploy
```

### 4. Push to GitHub

```bash
# Initialize git and push
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_ORG/my-new-website.git
git push -u origin main
```

### 5. Add to Pipeline Factory

Edit `pipeline-factory/config/websites.json`:

```json
{
  "websites": [
    {
      "siteName": "my-new-website",
      "githubRepo": "my-new-website",
      "domainName": "www.example.com",
      "hostedZoneId": "Z1234567890ABC",
      "hostedZoneName": "example.com",
      "menuPdfEnabled": false,
      "menuPdfBucketName": "",
      "menuPdfFilename": ""
    }
  ]
}
```

Deploy the pipeline:

```bash
cd pipeline-factory
cdk deploy my-new-website-pipeline
```

## Environment Variables

The `infra/app.py` reads these environment variables (injected by CodeBuild):

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `SITE_NAME` | Yes | Unique identifier for the website | `my-website` |
| `DOMAIN_NAME` | No | Custom domain (empty string for none) | `www.example.com` or `""` |
| `HOSTED_ZONE_ID` | No | Route 53 hosted zone ID | `Z1234567890ABC` or `""` |
| `HOSTED_ZONE_NAME` | No | Route 53 hosted zone name | `example.com` or `""` |
| `MENU_PDF_ENABLED` | No | Enable menu PDF bucket | `"true"` or `"false"` |
| `MENU_PDF_BUCKET_NAME` | No | Custom menu bucket name | `my-menu-files` or `""` |
| `MENU_PDF_FILENAME` | No | Menu PDF filename | `menu.pdf` or `""` |

## Domain Configuration

### With Custom Domain

Set these environment variables:
```bash
export DOMAIN_NAME="www.example.com"
export HOSTED_ZONE_ID="Z1234567890ABC"
export HOSTED_ZONE_NAME="example.com"
```

The shared construct will:
- Create ACM certificate (DNS-validated)
- Configure CloudFront with custom domain
- Create Route 53 A-record alias

### Without Custom Domain

Set empty strings:
```bash
export DOMAIN_NAME=""
export HOSTED_ZONE_ID=""
export HOSTED_ZONE_NAME=""
```

The shared construct will:
- Skip ACM certificate
- Skip Route 53 configuration
- Use CloudFront default `*.cloudfront.net` domain

## Menu PDF Support

Some websites need a separate public S3 bucket for PDF files (e.g., restaurant menus).

### Enable Menu PDF Bucket

1. Place your PDF file in `infra/` directory (e.g., `infra/menu.pdf`)
2. Set environment variables:
```bash
export MENU_PDF_ENABLED="true"
export MENU_PDF_BUCKET_NAME="my-menu-files"
export MENU_PDF_FILENAME="menu.pdf"
```

The shared construct will:
- Create public S3 bucket with the specified name
- Deploy the PDF file
- Configure public read access
- Output the PDF URL

### Disable Menu PDF Bucket

```bash
export MENU_PDF_ENABLED="false"
export MENU_PDF_BUCKET_NAME=""
export MENU_PDF_FILENAME=""
```

## Next.js Configuration

If using Next.js, configure static export in `site/next.config.ts`:

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",  // Enable static export
  images: {
    unoptimized: true,  // Required for static export
  },
};

export default nextConfig;
```

Then build:
```bash
cd site
npm run build  # Generates site/out/
```

## CodeBuild Process

The `buildspec.yml` handles the full build and deploy:

1. **Install Phase**: Node.js 20 + Python 3.12
2. **Pre-Build Phase**: `npm ci` (install dependencies)
3. **Build Phase**:
   - `npm run build` (builds Next.js site)
   - `pip install -r requirements.txt`
   - `cdk deploy --all --require-approval never`

## Infrastructure Details

The `infra/app.py` is a thin wrapper that:

1. Reads environment variables
2. Converts empty strings to `None`
3. Converts `MENU_PDF_ENABLED` string to boolean
4. Calculates paths relative to the repo structure
5. Passes everything to `WebsiteStack` from `shared-website-constructs`

All infrastructure logic (CloudFront, S3, Route 53, ACM, etc.) lives in the shared construct library.

## Troubleshooting

### Build Fails: "Module not found: shared_website_constructs"

The shared construct library needs to be published or installed locally:

```bash
# Option 1: Install from local path (development)
cd ../shared-website-constructs
pip install -e .

# Option 2: Install from PyPI (production)
pip install shared-website-constructs
```

### Deployment Fails: "No such file or directory: site/out"

Make sure you've built your website:

```bash
cd site
npm run build  # For Next.js
# OR
# Create site/out/index.html manually
```

### Custom Domain Not Working

Verify:
- Route 53 hosted zone exists
- Domain name matches hosted zone
- ACM certificate is in `us-east-1` region (required for CloudFront)
- DNS propagation can take up to 48 hours

### Menu PDF Not Accessible

Verify:
- PDF file exists in `infra/` directory
- Filename matches `MENU_PDF_FILENAME` exactly
- Bucket name is globally unique
- Public read access is configured (handled by shared construct)

## Requirements

- Python >= 3.12
- Node.js >= 20 (if using Next.js)
- AWS CDK >= 2.0.0
- shared-website-constructs >= 0.1.0

## License

MIT

## Support

For issues with the template, open an issue on GitHub.
For issues with infrastructure, check the `shared-website-constructs` repository.
