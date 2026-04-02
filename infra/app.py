#!/usr/bin/env python3
"""
Generic Website CDK App Template

Environment-variable-driven CDK app for deploying static websites.
Works for ANY client without modification - pipeline-factory passes
the right environment variables per website entry through CodeBuild.

Environment Variables (set by pipeline-factory via CodeBuild):
- SITE_NAME: Unique identifier for the website (REQUIRED)
- DOMAIN_NAME: Custom domain (REQUIRED, e.g., "clientdomain.com")
- HOSTED_ZONE_ID: Route 53 hosted zone ID (REQUIRED)
- HOSTED_ZONE_NAME: Route 53 hosted zone name (defaults to DOMAIN_NAME)
- DNS_PROVIDER: "route53" (default) or "external" for external DNS providers
- ACM_CERTIFICATE_ARN: Pre-created certificate ARN for external DNS mode
- ALT_DOMAIN_NAMES: Optional comma-separated alternate domain names (e.g., "www.example.com")
- MENU_PDF_ENABLED: "true" or "false" (default) for menu PDF hosting

External DNS Flow:
- When DNS_PROVIDER="external": Uses existing ACM certificate, skips Route 53 records
- When DNS_PROVIDER="route53": Creates ACM certificate with DNS validation, creates Route 53 records
"""

import os
import sys
import aws_cdk as cdk
from shared_website_constructs import WebsiteStack

# Guard: Check for required environment variables
required_vars = ["SITE_NAME", "DOMAIN_NAME", "HOSTED_ZONE_ID"]
missing_vars = [var for var in required_vars if not os.environ.get(var)]

if missing_vars:
    print("ERROR: Missing required environment variables:")
    for var in missing_vars:
        print(f"  - {var}")
    print("\nThis app requires environment variables to be set by the CI/CD pipeline.")
    print("If running locally, set these variables in your environment.")
    sys.exit(1)

app = cdk.App()

# Read environment variables (injected by CodeBuild via pipeline-factory)
site_name = os.environ.get("SITE_NAME")  # Required: unique website identifier
domain_name = os.environ.get("DOMAIN_NAME")  # Required: client's custom domain
hosted_zone_id = os.environ.get("HOSTED_ZONE_ID")  # Required: Route 53 zone ID
hosted_zone_name = os.environ.get("HOSTED_ZONE_NAME", domain_name)  # Defaults to domain_name

# DNS provider mode determines how DNS and certificates are handled
dns_provider = os.environ.get("DNS_PROVIDER", "route53").strip().lower()
external_dns = (dns_provider == "external")  # True when DNS is managed externally (e.g., GoDaddy)

# ACM certificate configuration
certificate_arn = os.environ.get("ACM_CERTIFICATE_ARN", "").strip() or None

# ALT_DOMAIN_NAMES: comma-separated alternate domains for CloudFront aliases
alt_domain_names_raw = os.environ.get("ALT_DOMAIN_NAMES", "").strip()
alt_domain_names = [
    d.strip() for d in alt_domain_names_raw.split(",") if d.strip()
] if alt_domain_names_raw else []
domain_names = (
    [domain_name] + [d for d in alt_domain_names if d != domain_name]
    if domain_name
    else []
)

# Menu PDF configuration (optional feature)
menu_pdf_enabled = os.environ.get("MENU_PDF_ENABLED", "false").strip().lower() == "true"

# Debug: Print configuration (helpful for troubleshooting deployments)
print(f"DEBUG: SITE_NAME={site_name}")
print(f"DEBUG: DOMAIN_NAME={domain_name}")
print(f"DEBUG: ALT_DOMAIN_NAMES={alt_domain_names}")
print(f"DEBUG: DOMAIN_NAMES (combined)={domain_names}")
print(f"DEBUG: HOSTED_ZONE_ID={hosted_zone_id}")
print(f"DEBUG: HOSTED_ZONE_NAME={hosted_zone_name}")
print(f"DEBUG: DNS_PROVIDER={dns_provider} (external_dns={external_dns})")
print(f"DEBUG: ACM_CERTIFICATE_ARN={certificate_arn or '(none - will create new)'}")
print(f"DEBUG: MENU_PDF_ENABLED={menu_pdf_enabled}")

# Build paths relative to this file
infra_dir = os.path.dirname(os.path.abspath(__file__))
content_path = os.path.join(infra_dir, "..", "site", "out")

# Create the main website stack with environment-driven configuration
WebsiteStack(
    app,
    f"{site_name.title().replace('-', '')}Stack",  # e.g., "ClientWebsiteStack"
    site_name=site_name,
    domain_name=domain_name,
    domain_names=domain_names or None,  # Apex + alternates for CloudFront
    hosted_zone_id=hosted_zone_id if not external_dns else None,  # Skip hosted zone for external DNS
    hosted_zone_name=hosted_zone_name if not external_dns else None,  # Skip hosted zone for external DNS
    certificate_arn=certificate_arn if external_dns else None,  # Use existing cert for external DNS
    create_route53_records=not external_dns,  # Skip Route 53 records for external DNS
    content_path=content_path,
    env=cdk.Environment(
        account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
        region=os.environ.get("CDK_DEFAULT_REGION", "us-east-1"),
    ),
    description=f"{site_name} - Static Website on AWS ({'External DNS' if external_dns else 'Route 53 DNS'})",
)

app.synth()