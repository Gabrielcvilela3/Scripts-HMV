import requests
import pandas as pd
import time
from tqdm import tqdm

# Configurações da API
url = 'https://crmhmv.apprubeus.com.br/api/Curso/listarOfertas'
params = {
    'origem': '9',
    'token': 'd2cc15f39418956cd23eca96b49681ec',
    'contexto': '1'
}

def fetch_data():
    """Busca os dados da API e retorna um DataFrame"""
    print("Conectando a API e buscando dados... Isso pode levar alguns segundos.")
    
    try:
        # Fazer requisição à API com timeout de 60 segundos
        print("Aguardando resposta da API (timeout: 60s)...")
        response = requests.get(url, params=params, timeout=60)
        
        print(f"Status da resposta: {response.status_code}")
        response.raise_for_status()
        
        print("Convertendo resposta para JSON...")
        result = response.json()
        
        if result.get('success'):
            total_registros = len(result['dados'])
            print(f"Total de registros recebidos (ja filtrados pela API): {total_registros}")
            
            # Processar dados
            print("Processando registros...")
            filtered_data = []
            
            for item in tqdm(result['dados'], desc="Processando registros"):
                # Processar locaisOferta para extrair códigos (excluindo PRV-0)
                locais_oferta = item.get('locaisOferta', [])
                codigos_privilegios = []
                
                for local in locais_oferta:
                    codigo = local.get('codigo', '')
                    if codigo and codigo != 'PRV-0':
                        codigos_privilegios.append(codigo)
                
                # Juntar os códigos com vírgula
                privilegios_vinculados = ', '.join(codigos_privilegios) if codigos_privilegios else ''
                
                filtered_data.append({
                    'ID da Especialidade': item.get('id'),
                    'Especialidade': item.get('nome'),
                    'Codigo da Especialidade': item.get('codigo'),
                    'ID da Atuacao': item.get('idCurso'),
                    'Atuacao': item.get('cursoNome'),
                    'Codigo do Atuacao': item.get('codCurso'),
                    'Unidade': item.get('unidadeNome'),
                    'Grupo de Especialidade': item.get('processoSeletivoNome'),
                    'Tipo de atuação': item.get('modalidadeNome'),
                    'Privilégios vinculados': privilegios_vinculados
                })
            
            # Converter para DataFrame
            df = pd.DataFrame(filtered_data)
            
            print(f"Total de registros processados: {len(df)}")
            
            return df
        else:
            print(f"Erro na requisicao: {result.get('message')}")
            return None
            
    except requests.exceptions.Timeout:
        print("ERRO: A requisicao excedeu o tempo limite de 60 segundos.")
        print("A API pode estar lenta ou indisponivel no momento.")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"ERRO de conexao: Nao foi possivel conectar a API.")
        print(f"Detalhes: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisicao HTTP: {e}")
        return None
    except ValueError as e:
        print(f"Erro ao processar JSON: {e}")
        print("A resposta da API pode nao estar no formato esperado.")
        return None
    except Exception as e:
        print(f"Erro inesperado: {type(e).__name__}: {e}")
        return None

def export_to_excel(df, filename):
    """Exporta DataFrame para Excel"""
    if df is None or len(df) == 0:
        print("Nao ha dados para exportar.")
        return
    
    print(f"\nExportando para Excel: {filename}")
    start_time = time.time()
    
    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Dados CRM')
        
        elapsed_time = time.time() - start_time
        print(f"[OK] Exportacao para Excel concluida em {elapsed_time:.2f} segundos")
    except Exception as e:
        print(f"Erro ao exportar Excel: {e}")

def export_to_csv(df, filename):
    """Exporta DataFrame para CSV"""
    if df is None or len(df) == 0:
        print("Nao ha dados para exportar.")
        return
    
    print(f"Exportando para CSV: {filename}")
    start_time = time.time()
    
    try:
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        elapsed_time = time.time() - start_time
        print(f"[OK] Exportacao para CSV concluida em {elapsed_time:.2f} segundos")
    except Exception as e:
        print(f"Erro ao exportar CSV: {e}")

def main():
    print("=" * 60)
    print("SCRIPT DE EXTRACAO DE OFERTAS DO CRM")
    print("=" * 60)
    
    start_time = time.time()
    
    # Buscar e processar dados
    df = fetch_data()
    
    if df is not None and len(df) > 0:
        # Exportar dados
        export_to_excel(df, 'ofertas_crm.xlsx')
        export_to_csv(df, 'ofertas_crm.csv')
        
        # Mostrar estatísticas
        print("\n" + "=" * 60)
        print("INFORMACOES SOBRE OS DADOS")
        print("=" * 60)
        print(f"Numero de registros: {len(df)}")
        print(f"Colunas: {', '.join(df.columns)}")
        
        # Mostrar primeiras linhas para verificação
        print("\nPrimeiros registros:")
        print(df.head(3).to_string())
        
        print("\n[OK] Processo concluido com sucesso!")
        print(f"[OK] Arquivos gerados: ofertas_crm.xlsx e ofertas_crm.csv")
    elif df is not None and len(df) == 0:
        print("\n[AVISO] Nenhum registro encontrado")
    else:
        print("\n[ERRO] Falha ao buscar dados da API")
    
    # Mostrar tempo total de execução
    total_time = time.time() - start_time
    print(f"\nTempo total de execucao: {total_time:.2f} segundos")
    print("=" * 60)

if __name__ == "__main__":
    main()