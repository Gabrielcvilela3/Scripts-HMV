import json
import subprocess
import requests
import time
import sys
import os

# Configuração
JS_SCRIPT_PATH = "C:\\Users\\gabri\\OneDrive\\Documentos\\Rubeus\\Scripts-HMV\\Evento-Em-Massa\\eventoEmMassa.js"  # Caminho para o seu arquivo JavaScript
API_URL = "https://crmhmv.apprubeus.com.br/api/Evento/cadastro"
MAX_RETRIES = 3  # Número máximo de tentativas para cada requisição
DELAY_BETWEEN_REQUESTS = 0.5  # Tempo de espera entre requisições (em segundos)
BATCH_SIZE = 10  # Número de requisições a fazer antes de imprimir um relatório de progresso

def run_javascript_script():
    """Executa o script JavaScript e retorna sua saída"""
    print(f"Executando o script JavaScript: {JS_SCRIPT_PATH}")
    
    try:
        # Verifica se o arquivo existe
        if not os.path.exists(JS_SCRIPT_PATH):
            raise FileNotFoundError(f"O arquivo {JS_SCRIPT_PATH} não foi encontrado")
        
        # Executa o script JavaScript usando Node.js
        result = subprocess.run(["node", JS_SCRIPT_PATH], 
                               capture_output=True, 
                               text=True, 
                               check=True)
        
        output = result.stdout
        return output
    
    except FileNotFoundError as e:
        print(f"Erro: {e}")
        print("Certifique-se de que o Node.js está instalado e o caminho do arquivo está correto.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script JavaScript: {e}")
        print(f"Saída de erro: {e.stderr}")
        sys.exit(1)

def parse_json_from_output(output):
    """Extrai e analisa o JSON da saída do script JavaScript"""
    print("Processando a saída do script JavaScript...")
    
    try:
        # Procura por um objeto JSON na saída (entre colchetes)
        import re
        json_match = re.search(r'(\[.*\])', output, re.DOTALL)
        
        if not json_match:
            raise ValueError("Nenhum JSON válido encontrado na saída do script")
        
        json_str = json_match.group(1)
        eventos = json.loads(json_str)
        
        print(f"JSON extraído com sucesso. Encontrados {len(eventos)} eventos para processar.")
        return eventos
    
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Erro ao analisar o JSON: {e}")
        print("Saída do script:")
        print(output)
        sys.exit(1)

def send_eventos_to_api(eventos):
    """Envia cada evento para a API com tratamento de erros e retentativas"""
    total = len(eventos)
    successful = 0
    failed = 0
    
    print(f"\nIniciando envio de {total} eventos para a API...")
    print(f"URL da API: {API_URL}")
    
    for index, evento in enumerate(eventos):
        # Informação de progresso a cada BATCH_SIZE eventos
        if index % BATCH_SIZE == 0 and index > 0:
            print(f"Progresso: {index}/{total} eventos processados ({successful} sucesso, {failed} falha)")
        
        # Tenta enviar o evento com retentativas
        success = False
        error_message = None
        
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.post(API_URL, json=evento, timeout=30)
                response.raise_for_status()  # Levanta exceção para códigos de erro HTTP
                
                # Se chegou aqui, a requisição foi bem-sucedida
                success = True
                successful += 1
                
                # Exibe detalhes para o primeiro evento bem-sucedido como exemplo
                if successful == 1:
                    print(f"\nExemplo de requisição bem-sucedida (evento {index+1}):")
                    print(f"Status: {response.status_code}")
                    print(f"Resposta: {response.text[:100]}..." if len(response.text) > 100 else f"Resposta: {response.text}")
                
                break  # Sai do loop de tentativas
                
            except requests.exceptions.RequestException as e:
                error_message = str(e)
                
                # Se não for a última tentativa, espera antes de tentar novamente
                if attempt < MAX_RETRIES - 1:
                    time.sleep(DELAY_BETWEEN_REQUESTS)
        
        # Se todas as tentativas falharam
        if not success:
            failed += 1
            # Exibe detalhes para o primeiro evento com falha como exemplo
            if failed == 1:
                print(f"\nExemplo de requisição com falha (evento {index+1}):")
                print(f"Erro: {error_message}")
                print(f"Dados do evento: {json.dumps(evento)[:100]}..." if len(json.dumps(evento)) > 100 else f"Dados do evento: {json.dumps(evento)}")
        
        # Espera um pouco entre as requisições para não sobrecarregar a API
        time.sleep(DELAY_BETWEEN_REQUESTS)
    
    # Relatório final
    print("\n" + "="*50)
    print(f"RELATÓRIO FINAL DE ENVIO")
    print("="*50)
    print(f"Total de eventos processados: {total}")
    print(f"Eventos enviados com sucesso: {successful}")
    print(f"Eventos com falha: {failed}")
    print(f"Taxa de sucesso: {(successful/total)*100:.2f}%")
    print("="*50)

def main():
    print("="*50)
    print("INTEGRAÇÃO JAVASCRIPT -> PYTHON -> API")
    print("="*50)
    
    # Executa o script JavaScript
    js_output = run_javascript_script()
    
    # Extrai os eventos do JSON na saída
    eventos = parse_json_from_output(js_output)
    
    # Confirmação antes de enviar para a API
    print(f"\nPronto para enviar {len(eventos)} eventos para a API.")
    confirmation = input("Deseja continuar? (s/n): ")
    
    if confirmation.lower() != 's':
        print("Operação cancelada pelo usuário.")
        return
    
    # Envia os eventos para a API
    send_eventos_to_api(eventos)

if __name__ == "__main__":
    main()
