#!/usr/bin/env python3
"""
Website CDK App Template

A complete template for deploying static websites with AWS CDK.
Uses shared-website-constructs for consistent infrastructure.

Usage:
1. Copy this template to your new website project
2. Update site_name and domain_name variables
3. Run: cdk deploy
"""

import os
import aws_cdk as cdk
from shared_website_constructs import WebsiteStack
from aws_cdk import (
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_iam as iam,
    CfnOutput,
    RemovalPolicy,
)

app = cdk.App()

# ============================================
# CONFIGURATION - UPDATE THESE VALUES
# ============================================
SITE_NAME = "my-website"  # Change to your website name
DOMAIN_NAME = ""  # Leave empty for CloudFront default domain, or set to your domain
HOSTED_ZONE_ID = ""  # Route 53 hosted zone ID (if using custom domain)
HOSTED_ZONE_NAME = ""  # Route 53 hosted zone name (if using custom domain)
MENU_PDF_ENABLED = False  # Set to True if you need menu PDF hosting
MENU_PDF_BUCKET_NAME = ""  # Custom bucket name for menu PDF
MENU_PDF_FILENAME = ""  # Menu PDF filename
# ============================================

# Build paths relative to this file
infra_dir = os.path.dirname(os.path.abspath(__file__))
content_path = os.path.join(infra_dir, "..", "site", "out")

# Create the main website stack
website_stack = WebsiteStack(
    app,
    f"{SITE_NAME.title().replace('-', '')}Stack",  # e.g., "MyWebsiteStack"
    site_name=SITE_NAME,
    domain_name=DOMAIN_NAME or None,  # None = uses CloudFront default domain
    hosted_zone_id=HOSTED_ZONE_ID or None,
    hosted_zone_name=HOSTED_ZONE_NAME or None,
    content_path=content_path,
    env=cdk.Environment(
        account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
        region=os.environ.get("CDK_DEFAULT_REGION", "us-east-1"),
    ),
    description=f"{SITE_NAME} - Static Website on AWS",
)

# Add menu PDF bucket if enabled
if MENU_PDF_ENABLED and MENU_PDF_BUCKET_NAME and MENU_PDF_FILENAME:
    # Create public menu PDF bucket
    menu_bucket = s3.Bucket(
        website_stack,
        f"{SITE_NAME.title().replace('-', '')}MenuBucket",
        bucket_name=MENU_PDF_BUCKET_NAME,
        removal_policy=RemovalPolicy.DESTROY,
        auto_delete_objects=True,
        block_public_access=s3.BlockPublicAccess(
            block_public_acls=False,
            block_public_policy=False,
            ignore_public_acls=False,
            restrict_public_buckets=False,
        ),
        object_ownership=s3.ObjectOwnership.BUCKET_OWNER_PREFERRED,
    )

    # Add public read policy
    menu_bucket.add_to_resource_policy(
        iam.PolicyStatement(
            actions=["s3:GetObject"],
            resources=[menu_bucket.arn_for_objects("*")],
            principals=[iam.AnyPrincipal()],
        )
    )

    # Deploy menu PDF
    s3deploy.BucketDeployment(
        website_stack,
        f"{SITE_NAME.title().replace('-', '')}MenuDeployment",
        sources=[s3deploy.Source.asset(
            infra_dir,
            exclude=["*", f"!{MENU_PDF_FILENAME}"],
        )],
        destination_bucket=menu_bucket,
        content_type="application/pdf",
    )

    # Output menu PDF URL
    CfnOutput(
        website_stack,
        "MenuPDFURL",
        value=f"https://{menu_bucket.bucket_regional_domain_name}/{MENU_PDF_FILENAME}",
        description="Menu PDF URL",
    )

    CfnOutput(
        website_stack,
        "MenuBucketName",
        value=menu_bucket.bucket_name,
        description="Menu PDF S3 Bucket Name",
    )

app.synth()