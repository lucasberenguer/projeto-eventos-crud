import os
import datetime

ARQUIVO_EVENTOS = "dados.txt"
ARQUIVO_TAREFAS = "tarefas.txt"

eventos_cache = []
tarefas_cache = []

def carregar_dados():
    global eventos_cache, tarefas_cache
    eventos_cache = []
    tarefas_cache = []

    if os.path.exists(ARQUIVO_EVENTOS):
        try:
            with open(ARQUIVO_EVENTOS, "r", encoding="utf-8") as f:
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
            print(f"Erro ao carregar eventos: {e}")

    if os.path.exists(ARQUIVO_TAREFAS):
        try:
            with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as f:
                for linha in f:
                    linha = linha.strip()
                    if linha:
                        dados = linha.split("|")
                        if len(dados) >= 3:
                            tarefas_cache.append({
                                "evento_nome": dados[0], 
                                "descricao": dados[1], 
                                "custo": float(dados[2])
                            })
        except Exception as e:
            print(f"Erro ao carregar tarefas: {e}")

def salvar_dados():
    try:
        with open(ARQUIVO_EVENTOS, "w", encoding="utf-8") as f:
            for ev in eventos_cache:
                linha = f"{ev['nome']}|{ev['tipo']}|{ev['data']}|{ev['local']}|{ev['orcamento']}\n"
                f.write(linha)
    except Exception as e:
        print(f"Erro ao salvar eventos: {e}")

    try:
        with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as f:
            for t in tarefas_cache:
                linha = f"{t['evento_nome']}|{t['descricao']}|{t['custo']}\n"
                f.write(linha)
    except Exception as e:
        print(f"Erro ao salvar tarefas: {e}")

def calcular_dias_restantes(data_str):
    try:
        data_evento = datetime.datetime.strptime(data_str, "%d/%m/%Y")
        hoje = datetime.datetime.now()
        diferenca = data_evento - hoje
        return diferenca.days + 1
    except ValueError:
        return "Data Inválida"

def calcular_saldo(nome_evento, orcamento_total):
    gasto_total = 0
    for t in tarefas_cache:
        if t['evento_nome'] == nome_evento:
            gasto_total += t['custo']
    return orcamento_total - gasto_total

def criar_eventos():
    print("\n--- Adicionar Novo Evento ---")
    nome = input("Nome (Identificador único): ")
    
    for ev in eventos_cache:
        if ev['nome'].lower() == nome.lower():
            input("Erro: Já existe um evento com esse nome. Enter para voltar...")
            return

    tipo = input("Tipo (Aniversario/Casamento/Outro): ")
    data = input("Data (DD/MM/AAAA): ")
    local = input("Local: ")
    try:
        orc = float(input("Orçamento Total: "))
        eventos_cache.append({
            "nome": nome, "tipo": tipo, "data": data, 
            "local": local, "orcamento": orc
        })
        salvar_dados()
        input("Evento criado! [Enter] para continuar...")
    except ValueError:
        input("Erro: Valor inválido. [Enter] para voltar...")

def exportar_html(evento):
    print(f"\n--- GERANDO RELATÓRIO HTML PARA: {evento['nome']} ---")
    nome_arquivo = f"{evento['nome'].replace(' ', '_')}_relatorio.html"
    saldo = calcular_saldo(evento['nome'], evento['orcamento'])
    
    cor_saldo = "green" if saldo >= 0 else "red"
    
    html = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Relatório - {evento['nome']}</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #333; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            .info-box {{ background-color: #e8f6f3; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
            .resumo {{ display: flex; justify-content: space-between; margin-bottom: 20px; }}
            .card {{ background: #eee; padding: 15px; width: 45%; border-radius: 5px; text-align: center; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #34495e; color: white; }}
            .total-row {{ font-weight: bold; background-color: #f9f9f9; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Relatório do Evento: {evento['nome']}</h1>
            
            <div class="info-box">
                <p><strong>Tipo:</strong> {evento['tipo']}</p>
                <p><strong>Data:</strong> {evento['data']}</p>
                <p><strong>Local:</strong> {evento['local']}</p>
            </div>

            <div class="resumo">
                <div class="card">
                    <h3>Orçamento Total</h3>
                    <p>R$ {evento['orcamento']:.2f}</p>
                </div>
                <div class="card">
                    <h3>Saldo Disponível</h3>
                    <p style="color: {cor_saldo}; font-weight: bold; font-size: 1.2em;">R$ {saldo:.2f}</p>
                </div>
            </div>

            <h3>Detalhamento de Gastos</h3>
            <table>
                <thead>
                    <tr>
                        <th>Descrição da Tarefa</th>
                        <th>Custo (R$)</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    total_gastos = 0
    tarefas_do_evento = [t for t in tarefas_cache if t['evento_nome'] == evento['nome']]
    
    if not tarefas_do_evento:
        html += "<tr><td colspan='2' style='text-align:center'>Nenhum gasto registrado ainda.</td></tr>"
    else:
        for t in tarefas_do_evento:
            html += f"<tr><td>{t['descricao']}</td><td>R$ {t['custo']:.2f}</td></tr>"
            total_gastos += t['custo']
            
    html += f"""
                </tbody>
                <tfoot>
                    <tr class="total-row">
                        <td>TOTAL GASTO</td>
                        <td>R$ {total_gastos:.2f}</td>
                    </tr>
                </tfoot>
            </table>
            <p style="text-align: center; margin-top: 30px; color: #777; font-size: 12px;">Gerado pelo Sistema Organiza Festa</p>
        </div>
    </body>
    </html>
    """
    
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"\n[SUCESSO] O arquivo '{nome_arquivo}' foi gerado na pasta do projeto!")
    except Exception as e:
        print(f"Erro ao gerar HTML: {e}")
    
    input("\n[Enter] para voltar...")

def gerenciar_evento_especifico(evento):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        saldo = calcular_saldo(evento['nome'], evento['orcamento'])
        dias = calcular_dias_restantes(evento['data'])
        
        print(f"=== GERENCIANDO: {evento['nome'].upper()} ===")
        print(f"Data: {evento['data']} (Faltam {dias} dias)")
        print(f"Orçamento Inicial: R$ {evento['orcamento']:.2f}")
        print(f"SALDO DISPONÍVEL:  R$ {saldo:.2f}")
        print("-" * 40)

        print("Tarefas/Gastos:")
        tem_tarefa = False
        for t in tarefas_cache:
            if t['evento_nome'] == evento['nome']:
                print(f" - {t['descricao']}: R$ {t['custo']:.2f}")
                tem_tarefa = True
        if not tem_tarefa:
            print(" (Nenhuma tarefa cadastrada)")

        print("-" * 40)
        print("1. Adicionar Tarefa/Gasto")
        print("2. Ver Sugestões (IA Básica)")
        print("3. Gerar Relatório HTML (Extra)")
        print("4. Voltar")
        
        op = input("Opção > ")
        
        if op == "1":
            desc = input("Descrição do gasto: ")
            try:
                val = float(input("Valor: "))
                tarefas_cache.append({
                    "evento_nome": evento['nome'],
                    "descricao": desc,
                    "custo": val
                })
                salvar_dados()
            except:
                print("Valor inválido.")
                input()
        elif op == "2":
            dar_sugestoes(evento['tipo'])
        elif op == "3":
            exportar_html(evento)
        elif op == "4":
            break

def dar_sugestoes(tipo):
    print(f"\n--- Sugestões para {tipo} ---")
    if "aniversario" in tipo.lower():
        print("- Não esqueça: Velas, Bolo, Descartáveis.")
    elif "casamento" in tipo.lower():
        print("- Não esqueça: Fotógrafo, Bem-casados, Lembrancinhas.")
    else:
        print("- Geral: Confirme a lista de presença 2 dias antes.")
    input("[Enter] para voltar...")

def excluir_eventos():
    print("\n--- Excluir Evento ---")
    busca = input("Nome do evento para excluir: ")
    nova_lista_ev = [ev for ev in eventos_cache if ev['nome'].lower() != busca.lower()]
    if len(nova_lista_ev) < len(eventos_cache):
        eventos_cache[:] = nova_lista_ev
        tarefas_cache[:] = [t for t in tarefas_cache if t['evento_nome'].lower() != busca.lower()]
        
        salvar_dados()
        input(f"Evento '{busca}' removido! [Enter] para continuar...")
    else:
        input("Evento não encontrado. [Enter] para voltar...")

def editar_evento():
    print("\n--- Editar Evento ---")
    busca = input("Nome do evento para editar: ")
    
    for evento in eventos_cache:
        if evento['nome'].lower() == busca.lower():
            print(f"--- Editando '{evento['nome']}' ---")
            print("(Deixe vazio e aperte Enter para não alterar)")
            
            nome_antigo = evento['nome']
            novo_nome = input(f"Nome ({evento['nome']}): ")
            
            if novo_nome and novo_nome != nome_antigo:
                existe = False
                for ev in eventos_cache:
                    if ev['nome'].lower() == novo_nome.lower():
                        existe = True
                        break
                
                if existe:
                    print("AVISO: Já existe um evento com esse nome. O nome NÃO foi alterado.")
                else:
                    evento['nome'] = novo_nome
                    count_tarefas = 0
                    for t in tarefas_cache:
                        if t['evento_nome'] == nome_antigo:
                            t['evento_nome'] = novo_nome
                            count_tarefas += 1
                    if count_tarefas > 0:
                        print(f"-> {count_tarefas} tarefas foram movidas para o novo nome.")

            novo_tipo = input(f"Tipo ({evento['tipo']}): ")
            if novo_tipo: evento['tipo'] = novo_tipo

            nova_data = input(f"Data ({evento['data']}): ")
            if nova_data: evento['data'] = nova_data

            novo_local = input(f"Local ({evento['local']}): ")
            if novo_local: evento['local'] = novo_local
            
            novo_orc_str = input(f"Orçamento ({evento['orcamento']}): ")
            if novo_orc_str:
                try:
                    evento['orcamento'] = float(novo_orc_str)
                except ValueError:
                    print("Valor de orçamento inválido. Mantido o anterior.")

            salvar_dados()
            input("\nEvento atualizado! [Enter] para continuar...")
            return
            
    input("Evento não encontrado.")

def painel_eventos():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== LISTA DE EVENTOS ===")
        print(f"{'ÍNDICE':<8} | {'NOME':<20} | {'DATA':<12} | {'DIAS REST.'}")
        print("-" * 60)
        
        if not eventos_cache:
            print("   Nenhum evento cadastrado.")
        else:
            for i, ev in enumerate(eventos_cache):
                dias = calcular_dias_restantes(ev['data'])
                print(f"{i+1:<8} | {ev['nome']:<20} | {ev['data']:<12} | {dias}")
        
        print("-" * 60)
        print("[N]ovo Evento   [G]erenciar Detalhes   [E]ditar   [R]emover   [V]oltar")

        opcao = input("Opção > ").upper()
        
        if opcao == "N":
            criar_eventos() 
        elif opcao == "G":
            idx = input("Digite o ÍNDICE do evento para gerenciar: ")
            if idx.isdigit() and 1 <= int(idx) <= len(eventos_cache):
                gerenciar_evento_especifico(eventos_cache[int(idx)-1])
            else:
                input("Índice inválido.")
        elif opcao == "E":
            editar_evento()
        elif opcao == "R":
            excluir_eventos()
        elif opcao == "V":
            break

def main():
    carregar_dados()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== SISTEMA ORGANIZA FESTA ===")
        print("1. Acessar Painel de Eventos")
        print("2. Sair")
        
        op = input("Opção: ")
        
        if op == "1":
            painel_eventos()
        elif op == "2":
            print("Saindo...")
            break

if __name__ == "__main__":
    main()