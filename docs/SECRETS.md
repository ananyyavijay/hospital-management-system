# Secrets Management for HMS v2

## Overview

HMS v2 uses three different locations for configuration and secrets. Each location serves a different purpose based on who needs access to the value.

| Location                               | What lives there                                                                    | Who/What reads it                                                         |
| -------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| GitHub Secrets                         | AZURE_WEBAPP_PUBLISH_PROFILE, deployment credentials, webhook URLs                  | GitHub Actions workflows (CI/CD pipeline)                                 |
| Azure App Service Application Settings | DB_HOST, DB_NAME, DB_PORT, APP_ENV, BLOB_CONTAINER_NAME, AZURE_STORAGE_ACCOUNT_NAME | Running FastAPI application via `os.getenv()`                             |
| Azure Key Vault                        | JWT_SECRET and other highly sensitive secrets                                       | Running FastAPI application via Key Vault references and Managed Identity |

## Secret Placement Rules

### GitHub Secrets

GitHub Secrets are used when the CI/CD pipeline requires a credential.

Examples:

* AZURE_WEBAPP_PUBLISH_PROFILE
* Slack or Teams webhook URLs
* Cloud deployment credentials

These values are consumed by GitHub Actions workflows and are never required directly by the running application.

### Azure App Service Application Settings

Application Settings store runtime configuration values that are not highly sensitive.

Examples:

* APP_ENV
* DB_HOST
* DB_NAME
* DB_PORT
* Storage account configuration

The FastAPI application accesses these values using environment variables (`os.getenv()`).

### Azure Key Vault

Azure Key Vault stores highly sensitive secrets.

Examples:

* JWT_SECRET
* Third-party API keys
* Database passwords (when password-based authentication is used)

Secrets are accessed securely through Managed Identity and Key Vault references.

## Phase 2 Journey

### DB_PASSWORD

The DB_PASSWORD followed this progression:

1. Stored in local `.env` files.
2. Moved to Azure App Service Application Settings.
3. Moved to Azure Key Vault for improved security.
4. Eventually eliminated completely through Azure Managed Identity authentication.

This removed the need to store a database password anywhere.

### JWT_SECRET

The JWT_SECRET followed this progression:

1. Stored in Azure App Service Application Settings.
2. Moved to Azure Key Vault.

Unlike DB_PASSWORD, JWT_SECRET cannot be eliminated because JWT token signing requires a secret value.

### AZURE_WEBAPP_PUBLISH_PROFILE

The publish profile is used only by the deployment pipeline.

Therefore it is stored in GitHub Secrets and is never stored in App Service settings or Azure Key Vault.

## Summary

* GitHub Secrets → Pipeline credentials.
* App Service Settings → Runtime configuration.
* Azure Key Vault → Sensitive application secrets.
* Managed Identity → Preferred whenever a password can be eliminated.
