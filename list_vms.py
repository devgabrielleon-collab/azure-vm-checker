import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

def listar_vms_desligadas(subscription_id):
    # 1. Autenticação Segura
    # O DefaultAzureCredential busca credenciais de ambiente, Managed Identity ou CLI
    credential = DefaultAzureCredential()
    
    # 2. Inicialização do Cliente de Computação
    compute_client = ComputeManagementClient(credential, subscription_id)
    
    print(f"--- Verificando VMs na assinatura: {subscription_id} ---")
    
    # 3. Iteração sobre todas as VMs da assinatura
    vms = compute_client.virtual_machines.list_all()
    
    vms_encontradas = 0
    
    for vm in vms:
        # Para saber o status (ligada/desligada), precisamos consultar a 'instance_view'
        vm_instance = compute_client.virtual_machines.get(
            resource_group_name=get_rg_from_id(vm.id),
            vm_name=vm.name,
            expand='instanceView'
        )
        
        # O status 'PowerState/deallocated' significa que a VM está desligada e não cobrando CPU/RAM
        statuses = [s.display_status for s in vm_instance.instance_view.statuses]
        
        if "VM deallocated" in statuses or "VM stopped" in statuses:
            print(f"ALERTA DE CUSTO: VM '{vm.name}' está DESLIGADA.")
            print(f"Localização: {vm.location} | Status: {statuses}")
            vms_encontradas += 1

    if vms_encontradas == 0:
        print("Tudo limpo! Nenhuma VM ociosa encontrada.")
    else:
        print(f"\nTotal de VMs desligadas encontradas: {vms_encontradas}")

def get_rg_from_id(vm_id):
    # Função auxiliar para extrair o nome do Resource Group a partir do ID da VM
    parts = vm_id.split('/')
    return parts[parts.index('resourceGroups') + 1]

if __name__ == "__main__":
    # O ID da assinatura será lido de uma variável de ambiente para segurança
    SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")
    if not SUBSCRIPTION_ID:
        print("Erro: A variável de ambiente AZURE_SUBSCRIPTION_ID não está definida.")
    else:
        listar_vms_desligadas(SUBSCRIPTION_ID)
