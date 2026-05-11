import os
import sys
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

def listar_vms_desligadas(subscription_id):
    try:
        # 1. Autenticação Segura
        credential = DefaultAzureCredential()
        
        # 2. Inicialização do Cliente de Computação
        compute_client = ComputeManagementClient(credential, subscription_id)
        
        print(f"## Relatório de VMs Desligadas - Assinatura: {subscription_id}\n")
        
        # 3. Iteração sobre todas as VMs da assinatura
        vms = compute_client.virtual_machines.list_all()
        
        vms_encontradas = []
        
        for vm in vms:
            try:
                # Para saber o status (ligada/desligada), precisamos consultar a 'instance_view'
                vm_instance = compute_client.virtual_machines.get(
                    resource_group_name=get_rg_from_id(vm.id),
                    vm_name=vm.name,
                    expand='instanceView'
                )
                
                statuses = [s.display_status for s in vm_instance.instance_view.statuses]
                
                if "VM deallocated" in statuses or "VM stopped" in statuses:
                    vms_encontradas.append({
                        "nome": vm.name,
                        "localizacao": vm.location,
                        "status": ", ".join(statuses),
                        "rg": get_rg_from_id(vm.id)
                    })
            except Exception as e:
                print(f"> Erro ao verificar VM {vm.name}: {str(e)}")

        if not vms_encontradas:
            print("✅ **Tudo limpo!** Nenhuma VM ociosa encontrada.")
        else:
            print(f"⚠️ Foram encontradas **{len(vms_encontradas)}** VMs desligadas:\n")
            print("| Nome da VM | Resource Group | Localização | Status |")
            print("| --- | --- | --- | --- |")
            for item in vms_encontradas:
                print(f"| {item['nome']} | {item['rg']} | {item['localizacao']} | {item['status']} |")
            
            print(f"\n**Total de VMs desligadas:** {len(vms_encontradas)}")

    except Exception as e:
        print(f"❌ **Erro Crítico:** {str(e)}")
        sys.exit(1)

def get_rg_from_id(vm_id):
    parts = vm_id.split('/')
    return parts[parts.index('resourceGroups') + 1]

if __name__ == "__main__":
    SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")
    if not SUBSCRIPTION_ID:
        print("❌ **Erro:** A variável de ambiente `AZURE_SUBSCRIPTION_ID` não está definida nos Secrets do GitHub.")
        sys.exit(1)
    else:
        listar_vms_desligadas(SUBSCRIPTION_ID)
