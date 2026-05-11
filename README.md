# Azure VM Checker 🚀

Este projeto foi desenvolvido por **[devgabrielleon-collab](https://github.com/devgabrielleon-collab)** para automatizar a verificação de máquinas virtuais (VMs) desligadas em assinaturas do Azure, ajudando no controle de custos e gestão de recursos.

## 🛠️ Funcionalidades

- Lista todas as VMs com status `deallocated` ou `stopped`.
- Gera um relatório automático via **GitHub Actions**.
- Exibe os resultados diretamente no Job Summary da execução.

## 🚀 Como funciona

O script utiliza a biblioteca `azure-mgmt-compute` para iterar sobre todas as VMs em uma assinatura específica e verifica o `instanceView` para determinar o status de energia.

## ⚙️ Configuração do GitHub Actions

Para que o workflow funcione, você precisa configurar os seguintes **Secrets** no seu repositório GitHub (`Settings > Secrets and variables > Actions`):

| Secret | Descrição |
| --- | --- |
| `AZURE_SUBSCRIPTION_ID` | O ID da sua assinatura Azure. |
| `AZURE_CLIENT_ID` | O ID do Cliente (App ID) do Service Principal. |
| `AZURE_TENANT_ID` | O ID do Tenant do seu Azure AD. |
| `AZURE_CLIENT_SECRET` | O segredo do Cliente do Service Principal. |

## 📝 Autor

Projeto idealizado e desenvolvido por **[devgabrielleon-collab](https://github.com/devgabrielleon-collab)**.
