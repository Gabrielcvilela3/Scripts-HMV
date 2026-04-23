import requests
import json
import pandas as pd
from datetime import datetime

def listar_locais_oferta():
    """
    Função que faz requisição à API e retorna todos os locais de oferta
    
    Returns:
        list: Lista de locais de oferta
    """
    # URL e dados para a requisição
    url = "https://crmhmv.apprubeus.com.br/api/LocalOferta/listarLocaisOferta"
    payload = {
        "origem": "9",
        "token": "d2cc15f39418956cd23eca96b49681ec"
    }
    
    # Fazendo a requisição GET com os dados JSON
    response = requests.get(url, json=payload)
    
    # Verificando se a requisição foi bem-sucedida
    if response.status_code != 200:
        print(f"Erro na requisição: {response.status_code}")
        return []
    
    try:
        # Extraindo dados da resposta
        resposta = response.json()
        print(f"Tipo de resposta recebida: {type(resposta)}")
        
        # Verificando se a resposta tem a chave 'dados'
        if 'dados' in resposta:
            dados = resposta['dados']
            print(f"Encontrada a chave 'dados' na resposta com {len(dados)} itens")
        else:
            print("Chave 'dados' não encontrada na resposta. Chaves disponíveis:", list(resposta.keys()))
            return []
        
        print(f"Total de locais encontrados: {len(dados)}")
        
        return dados
    
    except Exception as e:
        print(f"Erro ao processar os dados: {str(e)}")
        # Imprime mais detalhes sobre a resposta para ajudar na depuração
        print(f"Resposta da API: {response.text[:200]}...")  # Mostra apenas os primeiros 200 caracteres
        return []

def salvar_arquivo_txt(dados, nome_arquivo="locais_cadastros.txt"):
    """
    Salva os dados em formato TXT com os campos: id, codigo, titulo, descricao
    
    Args:
        dados (list): Lista de dicionários com os dados dos locais
        nome_arquivo (str): Nome do arquivo a ser gerado
    """
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        arquivo.write("LISTAGEM DE LOCAIS - CRM\n")
        arquivo.write("=" * 50 + "\n\n")
        
        for i, local in enumerate(dados, 1):
            arquivo.write(f"--- ITEM {i} ---\n")
            arquivo.write(f"ID: {local.get('id', 'N/A')}\n")
            arquivo.write(f"CÓDIGO: {local.get('codigo', 'N/A')}\n")
            arquivo.write(f"TÍTULO: {local.get('titulo', 'N/A')}\n")
            arquivo.write(f"DESCRIÇÃO: {local.get('descricao', 'N/A')}\n")
            arquivo.write("\n")
    
    print(f"Arquivo TXT '{nome_arquivo}' gerado com sucesso!")

def salvar_planilha_excel(dados, nome_arquivo="locais_cadastros.xlsx"):
    """
    Salva os dados em uma planilha Excel com as colunas: id, codigo, titulo, descricao
    
    Args:
        dados (list): Lista de dicionários com os dados dos locais
        nome_arquivo (str): Nome do arquivo Excel a ser gerado
    """
    # Preparando os dados para o DataFrame
    dados_planilha = []
    for local in dados:
        linha = {
            'id': local.get('id', ''),
            'codigo': local.get('codigo', ''),
            'titulo': local.get('titulo', ''),
            'descricao': local.get('descricao', '')
        }
        dados_planilha.append(linha)
    
    # Criando DataFrame
    df = pd.DataFrame(dados_planilha)
    
    # Salvando como Excel
    with pd.ExcelWriter(nome_arquivo, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Locais_CRM', index=False)
        
        # Ajustando largura das colunas
        worksheet = writer.sheets['Locais_CRM']
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)  # Largura máxima de 50
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    print(f"Planilha Excel '{nome_arquivo}' gerada com sucesso!")

def exibir_resumo(dados):
    """
    Exibe um resumo dos dados coletados
    
    Args:
        dados (list): Lista de dicionários com os dados dos locais
    """
    print("\n" + "=" * 50)
    print("RESUMO DOS DADOS COLETADOS")
    print("=" * 50)
    print(f"Total de locais encontrados: {len(dados)}")
    
    if dados:
        print("\nPrimeiros 3 itens como exemplo:")
        for i, local in enumerate(dados[:3], 1):
            print(f"\n{i}. ID: {local.get('id', 'N/A')}")
            print(f"   Código: {local.get('codigo', 'N/A')}")
            print(f"   Título: {local.get('titulo', 'N/A')[:80]}{'...' if len(local.get('titulo', '')) > 80 else ''}")

if __name__ == "__main__":
    print("Iniciando coleta de dados do CRM...")
    
    # Coleta todos os locais de oferta
    dados = listar_locais_oferta()
    
    if dados:
        # Exibe resumo
        exibir_resumo(dados)
        
        # Gera timestamp para nomes únicos de arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Gera arquivo TXT
        nome_txt = f"locais_cadastros_{timestamp}.txt"
        salvar_arquivo_txt(dados, nome_txt)
        
        # Gera planilha Excel
        nome_excel = f"locais_cadastros_{timestamp}.xlsx"
        salvar_planilha_excel(dados, nome_excel)
        
        print(f"\nProcessamento concluído!")
        print(f"Arquivos gerados:")
        print(f"- {nome_txt}")
        print(f"- {nome_excel}")
        
    else:
        print("Nenhum dado foi coletado. Verifique a conexão com a API.")