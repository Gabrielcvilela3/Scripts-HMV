import requests
import json
from datetime import datetime
import time

# URLs das APIs
URL_CONTATO = "https://crmhmv.apprubeus.com.br/api/Contato/cadastro"
URL_EVENTO = "https://crmhmv.apprubeus.com.br/api/Evento/cadastro"

# Token fixo
TOKEN = "d2cc15f39418956cd23eca96b49681ec"

# Lista de dados dos contatos
contatos_dados = [
# {"nome": "Giordano Gatti de Giacomo","CRM": "49002-RS","codigo": "49002-RS","codCurso": "6","codOferta": "RESID-1"},
# {"nome": "João Flavio Fontes Almeida","CRM": "51876-RS","codigo": "51876-RS","codCurso": "6","codOferta": "RESID-1"},
# {"nome": "Felipe Alves da Silva","CRM": "59703-RS","codigo": "59703-RS","codCurso": "6","codOferta": "RESID-1"},
# {"nome": "Julia Vicenzi Carminatti","CRM": "51643-RS","codigo": "51643-RS","codCurso": "6","codOferta": "RESID-1"},
# {"nome": "Moisés Wolfart Kaufmann","CRM": "58774-RS","codigo": "58774-RS","codCurso": "6","codOferta": "RESID-15"},
# {"nome": "Pedro Farias Renk","CRM": "48722-RS","codigo": "48722-RS","codCurso": "6","codOferta": "RESID-15"},
# {"nome": "Andrei Meurer de Andrade","CRM": "56553-RS","codigo": "56553-RS","codCurso": "6","codOferta": "RESID-2"},
# {"nome": "Arthur Proença Rossi","CRM": "56957-RS","codigo": "56957-RS","codCurso": "6","codOferta": "RESID-2"},
# {"nome": "Felipe Dall Agnol Vasatta","CRM": "54169-RS","codigo": "54169-RS","codCurso": "6","codOferta": "RESID-2"},
# {"nome": "Jéssica Danieli Brondani Machado","CRM": "48792-RS","codigo": "48792-RS","codCurso": "6","codOferta": "RESID-2"},
# {"nome": "Larissa Prokopp da Costa","CRM": "53695-RS","codigo": "53695-RS","codCurso": "6","codOferta": "RESID-2"},
# {"nome": "Luiz Francisco Meneguzzi Júnior","CRM": "44640-RS","codigo": "44640-RS","codCurso": "6","codOferta": "RESID-2"},
# {"nome": "Mariana Pereira Ramos","CRM": "56375-RS","codigo": "56375-RS","codCurso": "6","codOferta": "RESID-2"},
# {"nome": "Thathiane Vieira Franco Ribeiro","CRM": "54340-RS","codigo": "54340-RS","codCurso": "6","codOferta": "RESID-2"},
# {"nome": "Fernanda Ceron Damiani","CRM": "53850-RS","codigo": "53850-RS","codCurso": "6","codOferta": "RESID-2"},
# {"nome": "Guilherme Cavalcante Dantas","CRM": "59713-RS","codigo": "59713-RS","codCurso": "6","codOferta": "RESID-2"},
# {"nome": "Luane Pereira Gomes","CRM": "53675-RS","codigo": "53675-RS","codCurso": "6","codOferta": "RESID-2"},
# {"nome": "Maria Eduarda Conte Gripa","CRM": "51772-RS","codigo": "51772-RS","codCurso": "6","codOferta": "RESID-2"},
# {"nome": "Rafaella Willig de Quadros","CRM": "59255-RS","codigo": "59255-RS","codCurso": "6","codOferta": "RESID-2"},
# {"nome": "Thales Lorenz Lampert","CRM": "57417-RS","codigo": "57417-RS","codCurso": "6","codOferta": "RESID-2"},
# {"nome": "Júlia Vives Leal","CRM": "50902-RS","codigo": "50902-RS","codCurso": "6","codOferta": "RESID-3"},
# {"nome": "Luiza Rosso da Silva Pritsch","CRM": "53484-RS","codigo": "53484-RS","codCurso": "6","codOferta": "RESID-3"},
# {"nome": "Laura Przybylski","CRM": "47786-RS","codigo": "47786-RS","codCurso": "6","codOferta": "RESID-4"},
# {"nome": "Luiza Duarte Pittol","CRM": "54554-RS","codigo": "54554-RS","codCurso": "6","codOferta": "RESID-4"},
# {"nome": "Emanuelle Toledo Ortiz","CRM": "49764-RS","codigo": "49764-RS","codCurso": "6","codOferta": "RESID-16"},
# {"nome": "Sabrina Navroski","CRM": "54116-RS","codigo": "54116-RS","codCurso": "6","codOferta": "RESID-16"},
# {"nome": "Amanda de Farias Balbinot","CRM": "59774-RS","codigo": "59774-RS","codCurso": "6","codOferta": "RESID-14"},
# {"nome": "Emerson dos Santos Hoffmann","CRM": "49184-RS","codigo": "49184-RS","codCurso": "6","codOferta": "RESID-14"},
# {"nome": "Nadiana Inocente","CRM": "41093-RS","codigo": "41093-RS","codCurso": "6","codOferta": "RESID-14"},
# {"nome": "Rodrigo Chiavaro da Fonseca","CRM": "47938-RS","codigo": "47938-RS","codCurso": "6","codOferta": "RESID-17"},
# {"nome": "Luiza Rosa Nunes","CRM": "56739-RS","codigo": "56739-RS","codCurso": "6","codOferta": "RESID-5"},
# {"nome": "Marcus Vinicius Daldon Pavinato","CRM": "42208-RS","codigo": "42208-RS","codCurso": "6","codOferta": "RESID-5"},
# {"nome": "Mariana Gruber Pagel","CRM": "47855-RS","codigo": "47855-RS","codCurso": "6","codOferta": "RESID-5"},
# {"nome": "Paolla Favaro Bressiani","CRM": "58820-RS","codigo": "58820-RS","codCurso": "6","codOferta": "RESID-5"},
# {"nome": "Ana Luiza Ferretto Jaenisch","CRM": "59892-RS","codigo": "59892-RS","codCurso": "6","codOferta": "RESID-18"},
# {"nome": "Thomas Pagot Comissoli","CRM": "59953-RS","codigo": "59953-RS","codCurso": "6","codOferta": "RESID-18"},
# {"nome": "Wendersenn Pitterson da Silva Ideão","CRM": "57861","codigo": "57861","codCurso": "6","codOferta": "RESID-18"},
# {"nome": "Fabiana Kurzawa Hagemann","CRM": "56852-RS","codigo": "56852-RS","codCurso": "6","codOferta": "RESID-18"},
# {"nome": "Franciele Smiderle Bremm","CRM": "56741-RS","codigo": "56741-RS","codCurso": "6","codOferta": "RESID-18"},
# {"nome": "Vanessa Wallau Luchsinger","CRM": "56807-RS","codigo": "56807-RS","codCurso": "6","codOferta": "RESID-18"},
# {"nome": "Gabriele Arbugeri Menegotto","CRM": "51696","codigo": "51696","codCurso": "6","codOferta": "RESID-6"},
# {"nome": "Bruna Mirley Cavalcante Barreto","CRM": "54109-RS","codigo": "54109-RS","codCurso": "6","codOferta": "RESID-6"},
# {"nome": "Carlise Capeletti Medeiros","CRM": "49497-RS","codigo": "49497-RS","codCurso": "6","codOferta": "RESID-6"},
# {"nome": "Diego Seibel Júnior","CRM": "54325-RS","codigo": "54325-RS","codCurso": "6","codOferta": "RESID-6"},
# {"nome": "Felipe Cerbaro Viana","CRM": "51841-RS","codigo": "51841-RS","codCurso": "6","codOferta": "RESID-6"},
# {"nome": "Lucas Henrique Skalei Redmann","CRM": "58300","codigo": "58300","codCurso": "6","codOferta": "RESID-6"},
# {"nome": "Luís Henrique Nalin Vizioli","CRM": "51510-RS","codigo": "51510-RS","codCurso": "6","codOferta": "RESID-7"},
# {"nome": "Vinícius Ribeiro Escórcio","CRM": "59254","codigo": "59254","codCurso": "6","codOferta": "RESID-7"},
# {"nome": "Mateus Mondadori Sironi","CRM": "51734-RS","codigo": "51734-RS","codCurso": "6","codOferta": "RESID-7"},
# {"nome": "Pedro d'Elia Machado Silva","CRM": "57427-RS","codigo": "57427-RS","codCurso": "6","codOferta": "RESID-7"},
# {"nome": "Alex Victor Souza Bialecki","CRM": "54241-RS","codigo": "54241-RS","codCurso": "6","codOferta": "RESID-7"},
# {"nome": "Lourenço Ache Fernandes","CRM": "51229-RS","codigo": "51229-RS","codCurso": "6","codOferta": "RESID-7"},
# {"nome": "Isabela Tramontini Muller","CRM": "52983","codigo": "52983","codCurso": "6","codOferta": "RESID-8"},
# {"nome": "Carolina Yuka Ueda","CRM": "49607-RS","codigo": "49607-RS","codCurso": "6","codOferta": "RESID-8"},
# {"nome": "Felipe Dierings Andreis","CRM": "48518-RS","codigo": "48518-RS","codCurso": "6","codOferta": "RESID-8"},
# {"nome": "Michele Garcia Muraro","CRM": "46884-RS","codigo": "46884-RS","codCurso": "6","codOferta": "RESID-8"},
# {"nome": "Odanor Ferretti Tombini Filho","CRM": "54276","codigo": "54276","codCurso": "6","codOferta": "RESID-8"},
# {"nome": "Bernardo Rivera Fernandes Severo","CRM": "57006-RS","codigo": "57006-RS","codCurso": "6","codOferta": "RESID-9"},
# {"nome": "Pedro Augusto Cavagni Ambrosi","CRM": "53527-RS","codigo": "53527-RS","codCurso": "6","codOferta": "RESID-9"},
# {"nome": "Abcael Martins Santos Alves","CRM": "50281-RS","codigo": "50281-RS","codCurso": "6","codOferta": "RESID-9"},
# {"nome": "Gabriel Alves Martinelli","CRM": "49818-RS","codigo": "49818-RS","codCurso": "6","codOferta": "RESID-9"},
# {"nome": "Daniel Ceconello Maronez","CRM": "51686-RS","codigo": "51686-RS","codCurso": "6","codOferta": "RESID-9"},
# {"nome": "Deise Pancotto","CRM": "51781-RS","codigo": "51781-RS","codCurso": "6","codOferta": "RESID-9"},
# {"nome": "Felipe Cardoso dos Santos","CRM": "55606","codigo": "55606","codCurso": "6","codOferta": "RESID-19"},
# {"nome": "Leonardo Foletto Reisdorfer","CRM": "55845-RS","codigo": "55845-RS","codCurso": "6","codOferta": "RESID-19"},
# {"nome": "Carolina Scheer Ely","CRM": "59539","codigo": "59539","codCurso": "6","codOferta": "RESID-10"},
# {"nome": "Joas Cavalcante Estumano","CRM": "60185","codigo": "60185","codCurso": "6","codOferta": "RESID-10"},
# {"nome": "Letícia Kunst","CRM": "57009","codigo": "57009","codCurso": "6","codOferta": "RESID-10"},
# {"nome": "Ana Luíza Fonseca Siqueira","CRM": "49160-RS","codigo": "49160-RS","codCurso": "6","codOferta": "RESID-10"},
# {"nome": "Emanuele Smaniotto Frederich","CRM": "44368-RS","codigo": "44368-RS","codCurso": "6","codOferta": "RESID-10"},
# {"nome": "Georgia de Assunção Krauzer","CRM": "56511-RS","codigo": "56511-RS","codCurso": "6","codOferta": "RESID-10"},
# {"nome": "João Henrique Caurio da Silva","CRM": "47638-RS","codigo": "47638-RS","codCurso": "6","codOferta": "RESID-10"},
# {"nome": "Lara Damiani Cabral","CRM": "56912-RS","codigo": "56912-RS","codCurso": "6","codOferta": "RESID-10"},
# {"nome": "Paloma de Ávila Othero","CRM": "57709-RS","codigo": "57709-RS","codCurso": "6","codOferta": "RESID-10"},
# {"nome": "Thales Mascarenhas","CRM": "50400-RS","codigo": "50400-RS","codCurso": "6","codOferta": "RESID-10"},
# {"nome": "Rayla Rossetto dos Santos","CRM": "58395","codigo": "58395","codCurso": "6","codOferta": "RESID-10"},
# {"nome": "André Goulart Ramos","CRM": "60326","codigo": "60326","codCurso": "6","codOferta": "RESID-11"},
# {"nome": "Giovana Sperandio","CRM": "60105","codigo": "60105","codCurso": "6","codOferta": "RESID-11"},
# {"nome": "Marcela Lorea Habib","CRM": "49740-RS","codigo": "49740-RS","codCurso": "6","codOferta": "RESID-11"},
# {"nome": "Sibele Catarina Bernardi Jacob","CRM": "57535-RS","codigo": "57535-RS","codCurso": "6","codOferta": "RESID-11"},
# {"nome": "Carlos Eduardo Nedel","CRM": "47436-RS","codigo": "47436-RS","codCurso": "6","codOferta": "RESID-12"},
# {"nome": "José Henrique Gorgone Zampieri","CRM": "45372-RS","codigo": "45372-RS","codCurso": "6","codOferta": "RESID-12"},
# {"nome": "Juliana Gonçalves Silveira","CRM": "47788-RS","codigo": "47788-RS","codCurso": "6","codOferta": "RESID-12"},
# {"nome": "Bárbara Luiza Bernardi","CRM": "49487","codigo": "49487","codCurso": "6","codOferta": "RESID-12"},
# {"nome": "Karina Corrêa Brum Zinn","CRM": "55647","codigo": "55647","codCurso": "6","codOferta": "RESID-12"},
# {"nome": "Mateus Xavier Schenato","CRM": "54364","codigo": "54364","codCurso": "6","codOferta": "RESID-12"},
# {"nome": "Débora Koltermann da Silva","CRM": "50655-RS","codigo": "50655-RS","codCurso": "6","codOferta": "RESID-12"},
# {"nome": "Gabriela Carboni","CRM": "52882-RS","codigo": "52882-RS","codCurso": "6","codOferta": "RESID-12"},
# {"nome": "Isadora Zago Krebs","CRM": "50755","codigo": "50755","codCurso": "6","codOferta": "RESID-13"},
# {"nome": "Ana Carolina Milán Rodriguez","CRM": "48774-RS","codigo": "48774-RS","codCurso": "6","codOferta": "RESID-13"},
# {"nome": "Cláudio Roberto Amorim dos Santos Júnior","CRM": "49181","codigo": "49181","codCurso": "6","codOferta": "RESID-20"},
# {"nome": "Victor Kleinfelder Molinari","CRM": "42588","codigo": "42588","codCurso": "6","codOferta": "RESID-20"},
# {"nome": "Gláuber Ian Dalberto","CRM": "46302-RS","codigo": "46302-RS","codCurso": "6","codOferta": "RESID-20"},
# Adicione mais contatos aqui conforme necessário
]

# Lista fixa de privilégios para residência
privilegios_residencia = [
    "PRV-RESID-1",
    "PRV-RESID-2", 
    "PRV-RESID-3"
]

def tratar_crm(crm_str):
    """Remove sufixos como -RS do CRM, mantendo apenas números"""
    if "-" in crm_str:
        return crm_str.split("-")[0]
    return crm_str

def criar_contato(dados_contato):
    """Cria um contato via API"""
    
    # Trata o CRM removendo sufixos como -RS
    crm_tratado = tratar_crm(dados_contato["CRM"])
    
    body = {
        "nome": dados_contato["nome"],
        "codigo": crm_tratado,
        "camposPersonalizados": {
            "campopersonalizado_1_compl_cont": crm_tratado
        },
        "evento": {
            "tipo": "404",
            "codCurso": "6",
            "codOferta": dados_contato["codOferta"],
            "codLocalOferta": "PRV-0",
            "camposPersonalizados": {
                "campopersonalizado_191_compl_proc": "Ativo"
            }
        },
        "tags": [""],
        "origem": "9",
        "token": TOKEN
    }
    
    try:
        response = requests.post(URL_CONTATO, json=body, headers={"Content-Type": "application/json"})
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            resultado = response.json()
            if resultado.get("success"):
                return {"id": resultado.get("dados"), "erro": None}
            else:
                erro_msg = resultado.get("message", "Erro desconhecido da API")
                print(f"API retornou erro para {dados_contato['nome']}: {erro_msg}")
                return {"id": None, "erro": f"API: {erro_msg}"}
        else:
            erro_msg = f"HTTP {response.status_code}: {response.text}"
            print(f"Erro HTTP ao criar contato {dados_contato['nome']}: {erro_msg}")
            return {"id": None, "erro": erro_msg}
            
    except requests.exceptions.Timeout:
        erro_msg = "Timeout na requisição"
        print(f"Timeout ao criar contato {dados_contato['nome']}")
        return {"id": None, "erro": erro_msg}
        
    except requests.exceptions.ConnectionError:
        erro_msg = "Erro de conexão"
        print(f"Erro de conexão ao criar contato {dados_contato['nome']}")
        return {"id": None, "erro": erro_msg}
        
    except requests.exceptions.RequestException as e:
        erro_msg = f"Erro de requisição: {str(e)}"
        print(f"Erro de requisição ao criar contato {dados_contato['nome']}: {e}")
        return {"id": None, "erro": erro_msg}
        
    except json.JSONDecodeError:
        erro_msg = "Resposta inválida da API (não é JSON)"
        print(f"Erro ao decodificar JSON para {dados_contato['nome']}")
        return {"id": None, "erro": erro_msg}

def criar_evento(dados_contato, contato_id, privilegio):
    """Cria um evento via API"""
    
    # Trata o CRM removendo sufixos como -RS
    crm_tratado = tratar_crm(dados_contato["CRM"])
    
    body = {
        "tipo": "137",
        "pessoa": {
            "codigo": crm_tratado
        },
        "codRegistro": f"{privilegio}-{contato_id}",
        "codCurso": "6",
        "codOferta": dados_contato["codOferta"],
        "codLocalOferta": privilegio,
        "origem": "9",
        "token": TOKEN
    }
    
    try:
        response = requests.post(URL_EVENTO, json=body, headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            resultado = response.json()
            sucesso = resultado.get("success", False)
            erro = None if sucesso else resultado.get("message", "Erro desconhecido da API")
            return {"sucesso": sucesso, "erro": erro}
        else:
            erro_msg = f"HTTP {response.status_code}: {response.text}"
            return {"sucesso": False, "erro": erro_msg}
            
    except requests.exceptions.RequestException as e:
        erro_msg = f"Erro de requisição: {str(e)}"
        return {"sucesso": False, "erro": erro_msg}

def processar_contatos():
    """Processa todos os contatos da lista"""
    
    relatorio = {
        "total_contatos": len(contatos_dados),
        "contatos_processados": 0,
        "contatos_com_erro": 0,
        "total_eventos": 0,
        "eventos_com_sucesso": 0,
        "detalhes": []
    }
    
    for i, contato in enumerate(contatos_dados, 1):
        print(f"\nProcessando contato {i}/{len(contatos_dados)}: {contato['nome']}")
        
        # Criar contato
        resultado_contato = criar_contato(contato)
        
        detalhe_contato = {
            "nome": contato["nome"],
            "codigo": tratar_crm(contato["CRM"]),
            "CRM": contato["CRM"],
            "contato_criado": False,
            "contato_id": None,
            "erro_contato": None,
            "eventos": []
        }
        
        if resultado_contato["id"]:
            contato_id = resultado_contato["id"]
            print(f"Contato criado com sucesso. ID: {contato_id}")
            detalhe_contato["contato_criado"] = True
            detalhe_contato["contato_id"] = contato_id
            relatorio["contatos_processados"] += 1
            
            print(f"Criando {len(privilegios_residencia)} eventos de residência...")
            
            # Criar eventos para cada privilégio fixo
            for privilegio in privilegios_residencia:
                print(f"Criando evento com privilégio: {privilegio}")
                resultado_evento = criar_evento(contato, contato_id, privilegio)
                
                detalhe_evento = {
                    "privilegio": privilegio,
                    "sucesso": resultado_evento["sucesso"],
                    "erro": resultado_evento["erro"]
                }
                detalhe_contato["eventos"].append(detalhe_evento)
                relatorio["total_eventos"] += 1
                
                if resultado_evento["sucesso"]:
                    relatorio["eventos_com_sucesso"] += 1
                    print(f"Evento criado com sucesso para privilégio: {privilegio}")
                else:
                    print(f"Erro ao criar evento para privilégio {privilegio}: {resultado_evento['erro']}")
                
                # Pequena pausa entre requisições
                time.sleep(0.5)
                
        else:
            print(f"ERRO ao criar contato: {contato['nome']} - {resultado_contato['erro']}")
            detalhe_contato["erro_contato"] = resultado_contato["erro"]
            relatorio["contatos_com_erro"] += 1
        
        relatorio["detalhes"].append(detalhe_contato)
        
        # Pausa entre contatos
        time.sleep(1)
    
    return relatorio

def gerar_relatorio(relatorio):
    """Gera relatório final em console e salva em JSON"""
    
    print("\n" + "="*50)
    print("RELATORIO FINAL - RESIDENCIA")
    print("="*50)
    print(f"Total de contatos: {relatorio['total_contatos']}")
    print(f"Contatos processados com sucesso: {relatorio['contatos_processados']}")
    print(f"Contatos com erro: {relatorio['contatos_com_erro']}")
    print(f"Total de eventos: {relatorio['total_eventos']}")
    print(f"Eventos com sucesso: {relatorio['eventos_com_sucesso']}")
    print(f"Eventos com erro: {relatorio['total_eventos'] - relatorio['eventos_com_sucesso']}")
    
    print("\nDETALHES POR CONTATO:")
    print("-"*50)
    
    for detalhe in relatorio["detalhes"]:
        print(f"\nContato: {detalhe['nome']} (CRM: {detalhe['CRM']})")
        print(f"Codigo: {detalhe['codigo']}")
        print(f"Status: {'SUCESSO' if detalhe['contato_criado'] else 'ERRO'}")
        
        if detalhe['contato_criado']:
            print(f"ID: {detalhe['contato_id']}")
            eventos_sucesso = sum(1 for e in detalhe['eventos'] if e['sucesso'])
            print(f"Eventos: {eventos_sucesso}/{len(detalhe['eventos'])} com sucesso")
            
            # Listar eventos com erro
            eventos_erro = [e for e in detalhe['eventos'] if not e['sucesso']]
            if eventos_erro:
                print("Eventos com erro:")
                for evento in eventos_erro:
                    print(f"  - {evento['privilegio']}: {evento['erro']}")
        else:
            print(f"Erro: {detalhe['erro_contato']}")
            print("Nenhum evento foi criado (contato não foi cadastrado)")
    
    # Salvar relatório em JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"relatorio_residencia_{timestamp}.json"
    
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(relatorio, arquivo, indent=2, ensure_ascii=False)
        print(f"\nRelatório salvo em: {nome_arquivo}")
    except Exception as e:
        print(f"\nErro ao salvar relatório JSON: {e}")

if __name__ == "__main__":
    print("Iniciando processamento de contatos - RESIDENCIA...")
    relatorio = processar_contatos()
    gerar_relatorio(relatorio)