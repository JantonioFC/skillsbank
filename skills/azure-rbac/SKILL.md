---
name: azure-rbac
description: 'Helps users find the right Azure RBAC role for an identity with least
  privilege access, then generate CLI commands and Bicep code to assign it.

  USE FOR: "what role should I assign", "least privilege role", "RBAC role for", "role
  to read blobs", "role for managed identity", "custom role def...'
risk: unknown
source: community
---

Use the 'azure__documentation' tool to find the minimal role definition that matches the desired permissions the user wants to assign to an identity. If no built-in role matches the desired permissions, use the 'azure__extension_cli_generate' tool to create a custom role definition with the desired permissions. Then use the 'azure__extension_cli_generate' tool to generate the CLI commands needed to assign that role to the identity. Finally, use the 'azure__bicepschema' and 'azure__get_azure_bestpractices' tools to provide a Bicep code snippet for adding the role assignment.

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.
