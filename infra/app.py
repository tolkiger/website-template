#!/usr/bin/env python3
"""
CDK Entry Point -- Thin wrapper that imports the shared website construct.

All infrastructure logic lives in the shared-website-constructs package.
Environment variables are injected by CodeBuild from the pipeline factory.
"""
import os
import aws_cdk as cdk
from shared_website_constructs import WebsiteStack

app = cdk.App()

# Read environment variables (injected by CodeBuild)
site_name = os.environ.get("SITE_NAME", "my-website")
domain_name = os.environ.get("DOMAIN_NAME", "") or None
hosted_zone_id = os.environ.get("HOSTED_ZONE_ID", "") or None
hosted_zone_name = os.environ.get("HOSTED_ZONE_NAME", "") or None
menu_pdf_enabled = os.environ.get("MENU_PDF_ENABLED", "false").lower() == "true"
menu_pdf_bucket_name = os.environ.get("MENU_PDF_BUCKET_NAME", "") or None
menu_pdf_filename = os.environ.get("MENU_PDF_FILENAME", "") or None

# Build paths relative to this file
infra_dir = os.path.dirname(os.path.abspath(__file__))
content_path = os.path.join(infra_dir, "..", "site", "out")

# Only pass menu PDF path if enabled
menu_pdf_path = infra_dir if menu_pdf_enabled else None

WebsiteStack(
    app,
    "WebsiteStack",
    site_name=site_name,
    domain_name=domain_name,
    hosted_zone_id=hosted_zone_id,
    hosted_zone_name=hosted_zone_name,
    content_path=content_path,
    menu_pdf_enabled=menu_pdf_enabled,
    menu_pdf_bucket_name=menu_pdf_bucket_name,
    menu_pdf_filename=menu_pdf_filename,
    menu_pdf_path=menu_pdf_path,
    env=cdk.Environment(
        account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
        region=os.environ.get("CDK_DEFAULT_REGION", "us-east-1"),
    ),
)

app.synth()
