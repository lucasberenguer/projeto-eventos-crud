import os

ARQUIVO = "dados.txt"
eventos_cache = []

def carregar_eventos():
    global eventos_cache
    eventos_cache = []
    if not os.path.exists(ARQUIVO): return
    
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    dados = linha.split("|")
                    if len(dados) >= 5:
                        eventos_cache.append({
                            "nome": dados[0], "tipo": dados[1],
                            "data": dados[2], "local": dados[3],
                            "orcamento": float(dados[4])
                        })
    except Exception as e:
        print(f"Erro ao carregar: {e}")

def salvar_dados():
    try:
        with open(ARQUIVO, "w", encoding="utf-8") as f:
            for ev in eventos_cache:
                linha = f"{ev['nome']}|{ev['tipo']}|{ev['data']}|{ev['local']}|{ev['orcamento']}\n"
                f.write(linha)
    except Exception as e:
        print(f"Erro ao salvar: {e}")

def criar_eventos():
    print("\n--- Adicionar Novo Evento ---")
    nome = input("Nome: ")
    tipo = input("Tipo: ")
    data = input("Data: ")
    local = input("Local: ")
    try:
        orc = float(input("Orçamento: "))
        eventos_cache.append({
            "nome": nome, "tipo": tipo, "data": data, 
            "local": local, "orcamento": orc
        })
        salvar_dados()
        input("Evento criado! [Enter] para continuar...")
    except ValueError:
        input("Erro: Valor inválido. [Enter] para voltar...")

def excluir_eventos():
    print("\n--- Excluir Evento ---")
    busca = input("Digite o NOME do evento para excluir: ")
    
    encontrado = False
    for i, evento in enumerate(eventos_cache):
        if evento['nome'].lower() == busca.lower():
            del eventos_cache[i]
            encontrado = True
            break
            
    if encontrado:
        salvar_dados()
        input(f"Evento '{busca}' removido! [Enter] para continuar...")
    else:
        input("Evento não encontrado. [Enter] para voltar...")

def editar_evento():
    print("\n--- Editar Evento ---")
    busca = input("Nome do evento a editar: ")
    for evento in eventos_cache:
        if evento['nome'].lower() == busca.lower():
            print(f"Editando '{evento['nome']}' (Deixe vazio para não alterar)")
            novo_local = input(f"Local atual ({evento['local']}): ")
            if novo_local: evento['local'] = novo_local
            
            salvar_dados()
            input("Atualizado! [Enter] para continuar...")
            return
    input("Evento não encontrado.")

def painel_eventos():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== GERENCIAMENTO DE EVENTOS ===")
        print(f"{'ÍNDICE':<8} | {'NOME':<20} | {'DATA':<12}")
        print("-" * 45)
        
        if not eventos_cache:
            print("   Nenhum evento cadastrado.")
        else:
            for i, ev in enumerate(eventos_cache):
                print(f"{i+1:<8} | {ev['nome']:<20} | {ev['data']:<12}")
        
        print("-" * 45)
        print("[N]ovo Evento   [E]ditar   [R]emover   [V]oltar Menu Principal")

        opcao = input("Opção > ").upper()
        
        if opcao == "N":
            criar_eventos() 
        elif opcao == "E":
            editar_evento()
        elif opcao == "R":
            excluir_eventos()
        elif opcao == "V":
            break
        else:
            print("Opção inválida.")

def main():
    carregar_eventos()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== SISTEMA ORGANIZA FESTA ===")
        print("1. Gerenciar Eventos (Listar/Criar/Editar/Excluir)")
        print("2. Sair")
        
        op = input("Opção: ")
        
        if op == "1":
            painel_eventos()
        elif op == "2":
            print("Saindo...")
            break

if __name__ == "__main__":
    main()
