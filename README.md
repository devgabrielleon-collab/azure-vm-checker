# Azure VM Checker

Este repositório contém um script Python para listar máquinas virtuais (VMs) que estão desligadas ou desalocadas no Azure, ajudando a identificar potenciais economias de custo.

## Como funciona

O script utiliza a biblioteca `azure-mgmt-compute` para iterar sobre todas as VMs em uma assinatura específica e verifica o `instanceView` para determinar o status de energia.

## Configuração do GitHub Actions

Para que o workflow funcione, você precisa configurar os seguintes **Secrets** no seu repositório GitHub (`Settings > Secrets and variables > Actions`):

| Secret | Descrição |
| --- | --- |
| `AZURE_SUBSCRIPTION_ID` | O ID da sua assinatura Azure. |
| `AZURE_CLIENT_ID` | O ID do Cliente (App ID) do Service Principal. |
| `AZURE_TENANT_ID` | O ID do Tenant do seu Azure AD. |
| `AZURE_CLIENT_SECRET` | O segredo do Cliente do Service Principal. |

## Execução

O workflow está configurado para rodar:
1. Automaticamente todos os dias à meia-noite (UTC).
2. Manualmente através da aba "Actions" no GitHub.
