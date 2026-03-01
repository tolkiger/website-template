#!/bin/bash
# Create a new website from template

set -e

echo "Website Template Creator"
echo "========================"

if [ $# -lt 1 ]; then
    echo "Usage: $0 <website-name>"
    echo "Example: $0 my-restaurant"
    exit 1
fi

WEBSITE_NAME="$1"
TEMPLATE_DIR="$(dirname "$0")"

echo "Creating website: $WEBSITE_NAME"
echo ""

# Check if we're in the right directory
if [ ! -d "$TEMPLATE_DIR/site" ] || [ ! -d "$TEMPLATE_DIR/infra" ]; then
    echo "Error: Template files not found. Run this script from the template directory."
    exit 1
fi

# Create new directory
mkdir -p "../../websites/$WEBSITE_NAME"
cd "../../websites/$WEBSITE_NAME"

echo "📁 Creating directory structure..."
mkdir -p site infra

echo "📋 Copying template files..."
cp -r "$TEMPLATE_DIR/site/"* site/
cp -r "$TEMPLATE_DIR/infra/"* infra/

echo "🔗 Copying shared constructs..."
cp -r "../../website-infrastructure/shared-website-constructs/shared_website_constructs" infra/

echo "⚙️  Updating configuration..."
# Update app.py
sed -i '' "s/SITE_NAME = \"my-website\"/SITE_NAME = \"$WEBSITE_NAME\"/g" infra/app.py

# Update package.json
sed -i '' "s/\"name\": \"website-template\"/\"name\": \"$WEBSITE_NAME\"/g" site/package.json

echo "📝 Creating README..."
cat > README.md <<EOF
# $WEBSITE_NAME

Created from website template.

## Quick Start

\`\`\`bash
# Install dependencies
cd site && npm install
cd ../infra && pip install -r requirements.txt

# Build and deploy
cd site && npm run build
cd ../infra && cdk deploy
\`\`\`

## Development

- Local: \`cd site && npm run dev\`
- Build: \`cd site && npm run build\`
- Deploy: \`cd infra && cdk deploy\`
EOF

echo "✅ Website template created!"
echo ""
echo "Next steps:"
echo "1. cd websites/$WEBSITE_NAME"
echo "2. Customize your site in the 'site/' directory"
echo "3. Update infra/app.py with your domain (optional)"
echo "4. Run: cd infra && cdk deploy"
echo ""
echo "To add CI/CD pipeline:"
echo "1. Add to website-infrastructure/pipeline-factory/config/websites.json"
echo "2. Deploy pipeline: cd website-infrastructure/pipeline-factory && cdk deploy"