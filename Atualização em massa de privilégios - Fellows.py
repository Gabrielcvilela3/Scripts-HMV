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
# {"nome": "Pedro Rotta de Ferreira","CRM": "49337","codigo": "49337","codCurso": "6","codOferta": "FELLOW-14"},
# {"nome": "Paulo Eduardo Meneguzzo","CRM": "45168","codigo": "45168","codCurso": "6","codOferta": "FELLOW-15"},
# {"nome": "Kellwin Nery Teixeira","CRM": "47494","codigo": "47494","codCurso": "6","codOferta": "FELLOW-16"},
# {"nome": "Raíssa dos Reis Echer","CRM": "48241","codigo": "48241","codCurso": "6","codOferta": "FELLOW-17"},
# {"nome": "Vivian Luisa Frantz","CRM": "51508","codigo": "51508","codCurso": "6","codOferta": "FELLOW-18"},
# {"nome": "Leonardo Pereira de Lima","CRM": "44443","codigo": "44443","codCurso": "6","codOferta": "FELLOW-19"},
# {"nome": "Marília Paz de Paiva","CRM": "44508","codigo": "44508","codCurso": "6","codOferta": "FELLOW-19"},
# {"nome": "Greyce Berton","CRM": "33277","codigo": "33277","codCurso": "6","codOferta": "FELLOW-20"},
# {"nome": "Rômulo Marx","CRM": "47025","codigo": "47025","codCurso": "6","codOferta": "FELLOW-3"},
# {"nome": "Victor Otávio Derossi","CRM": "54791","codigo": "54791","codCurso": "6","codOferta": "FELLOW-3"},
# {"nome": "Giannini Medeiros Rodrigues","CRM": "58800","codigo": "58800","codCurso": "6","codOferta": "FELLOW-21"},
# {"nome": "Isabela Corrêa Bitencourt","CRM": "59782","codigo": "59782","codCurso": "6","codOferta": "FELLOW-22"},
# {"nome": "Lucas Strassburger Matzenbacher","CRM": "59749","codigo": "59749","codCurso": "6","codOferta": "FELLOW-22"},
# {"nome": "Dânisa Smiljanic Carrijo","CRM": "54661","codigo": "54661","codCurso": "6","codOferta": "FELLOW-23"},
# {"nome": "Luciana D'Amico","CRM": "41639","codigo": "41639","codCurso": "6","codOferta": "FELLOW-12"},
# {"nome": "Maria Paula Alves Corrêa","CRM": "51919","codigo": "51919","codCurso": "6","codOferta": "FELLOW-12"},
# {"nome": "Camila Borges Mosmann Melere","CRM": "36681","codigo": "36681","codCurso": "6","codOferta": "FELLOW-24"},
# {"nome": "Amanda Kühl","CRM": "50092","codigo": "50092","codCurso": "6","codOferta": "FELLOW-25"},
# {"nome": "Ana Carolina Farias Rodrigues","CRM": "49728","codigo": "49728","codCurso": "6","codOferta": "FELLOW-25"},
# {"nome": "María José Santacruz Villalba","CRM": "50227","codigo": "50227","codCurso": "6","codOferta": "FELLOW-25"},
# {"nome": "Paola Iana Fucks da Veiga","CRM": "50584","codigo": "50584","codCurso": "6","codOferta": "FELLOW-26"},
# {"nome": "Cecyra Bauermann Collares Machado","CRM": "36434","codigo": "36434","codCurso": "6","codOferta": "FELLOW-27"},
# {"nome": "Matheus Werlang Donadel","CRM": "47207","codigo": "47207","codCurso": "6","codOferta": "FELLOW-27"},
# {"nome": "Brenda Rigatti","CRM": "47533","codigo": "47533","codCurso": "6","codOferta": "FELLOW-10"},
# {"nome": "Ximena Alejandra Celi Loaiza","CRM": "52244","codigo": "52244","codCurso": "6","codOferta": "FELLOW-28"},
# {"nome": "Leonardo Felipi Schmitz Franco","CRM": "50990","codigo": "50990","codCurso": "6","codOferta": "FELLOW-29"},
# {"nome": "Lucas Leimig Telles Parente","CRM": "52014","codigo": "52014","codCurso": "6","codOferta": "FELLOW-29"},
# {"nome": "Meiri Andreia Maria da Silva","CRM": "35868","codigo": "35868","codCurso": "6","codOferta": "FELLOW-29"},
# {"nome": "Patrícia de Oliveira Pimentel Fonseca","CRM": "48129","codigo": "48129","codCurso": "6","codOferta": "FELLOW-29"},
# {"nome": "Samuel Santos Freitas ","CRM": "46903","codigo": "46903","codCurso": "6","codOferta": "FELLOW-29"},
# {"nome": "Viviani Draghetti","CRM": "24601","codigo": "24601","codCurso": "6","codOferta": "FELLOW-29"},
# {"nome": "Júlia Plentz Portich","CRM": "42592","codigo": "42592","codCurso": "6","codOferta": "FELLOW-30"},
# {"nome": "Caroline Nicola Sangalli - Nutricionista","CRM": "28962","codigo": "28962","codCurso": "6","codOferta": "FELLOW-31"},
# {"nome": "Fernanda Fernandes Cruz - Farmacêutica","CRM": "16046","codigo": "16046","codCurso": "6","codOferta": "FELLOW-31"},
# {"nome": "Flávia Marini Peres de Souza","CRM": "60450","codigo": "60450","codCurso": "6","codOferta": "FELLOW-32"},
# {"nome": "Pablo Rojas Romero","CRM": "52189","codigo": "52189","codCurso": "6","codOferta": "FELLOW-33"},
# Adicione mais contatos aqui conforme necessário
]

# Lista fixa de privilégios para residência
privilegios_fellowship = [
    "PRV-FELLOW-1",
    "PRV-FELLOW-2",
    "PRV-FELLOW-3",
    "PRV-FELLOW-4"
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
            "codCurso": dados_contato["codCurso"],
            "codOferta": dados_contato["codOferta"],
            "codLocalOferta": "PRV-0",
            "camposPersonalizados": {
                "campopersonalizado_191_compl_proc": "Ativo"
            }
        },
        "tags": ["Att. Privilégios Fellows - 09/2025"],
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
        "codCurso": dados_contato["codCurso"],
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
            
            print(f"Criando {len(privilegios_fellowship)} eventos de residência...")
            
            # Criar eventos para cada privilégio fixo
            for privilegio in privilegios_fellowship:
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
    print("RELATORIO FINAL - FELLOWSHIP")
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
    nome_arquivo = f"relatorio_fellowship_{timestamp}.json"
    
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(relatorio, arquivo, indent=2, ensure_ascii=False)
        print(f"\nRelatório salvo em: {nome_arquivo}")
    except Exception as e:
        print(f"\nErro ao salvar relatório JSON: {e}")

if __name__ == "__main__":
    print("Iniciando processamento de contatos - FELLOWSHIP...")
    relatorio = processar_contatos()
    gerar_relatorio(relatorio)