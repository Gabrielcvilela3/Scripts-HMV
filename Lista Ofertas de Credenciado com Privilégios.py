import requests
import pandas as pd
from datetime import datetime

def buscar_ofertas_filtradas():
    """
    Busca ofertas do CRM e filtra pelo cursoNome 'Credenciado'
    """
    
    # Configuração da requisição
    url = "https://crmhmv.apprubeus.com.br/api/Curso/listarOfertas"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    body = {
        "origem": "9",
        "token": "d2cc15f39418956cd23eca96b49681ec"
    }
    
    try:
        # Faz a requisição GET
        print("Buscando ofertas do CRM...")
        response = requests.get(url, json=body, headers=headers)
        response.raise_for_status()
        
        # Processa a resposta
        resposta = response.json()
        
        # Verifica se a requisição foi bem-sucedida
        if not resposta.get('success'):
            print("Erro: A API retornou success=false")
            return None, 0
        
        # Extrai a lista de ofertas da chave 'dados'
        ofertas = resposta.get('dados', [])
        print(f"Total de ofertas na API: {len(ofertas)}")
        
        # Filtra ofertas pelo cursoNome
        ofertas_filtradas = [
            oferta for oferta in ofertas 
            if oferta.get('cursoNome') == 'Credenciado'
        ]
        
        # Extrai apenas os campos necessários
        resultado = []
        for oferta in ofertas_filtradas:
            # Extrai os códigos dos locais de oferta
            locais_oferta = oferta.get('locaisOferta', [])
            codigos_locais = ', '.join([local.get('codigo', '') for local in locais_oferta])
            
            resultado.append({
                'id': oferta.get('id'),
                'nome': oferta.get('nome'),
                'codigo': oferta.get('codigo'),
                'locaisOferta': codigos_locais
            })
        
        # Total de ofertas filtradas
        total_ofertas = len(resultado)
        
        print(f"Total de ofertas filtradas (Credenciado): {total_ofertas}")
        
        # Salva em planilha Excel
        if resultado:
            df = pd.DataFrame(resultado)
            
            # Nome do arquivo com data e hora
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"ofertas_credenciado_{timestamp}.xlsx"
            
            # Cria o Excel com duas abas
            with pd.ExcelWriter(nome_arquivo, engine='openpyxl') as writer:
                # Aba com as ofertas
                df.to_excel(writer, sheet_name='Ofertas', index=False)
                
                # Aba com o totalizador
                df_total = pd.DataFrame({
                    'Descricao': ['Total de Ofertas Filtradas'],
                    'Quantidade': [total_ofertas]
                })
                df_total.to_excel(writer, sheet_name='Totalizador', index=False)
            
            print(f"\n[OK] Planilha salva com sucesso: {nome_arquivo}")
            
            # Exibe os primeiros resultados no console
            print("\nPrimeiras 10 ofertas encontradas:")
            print(df.head(10).to_string(index=False))
            
        else:
            print("\n[AVISO] Nenhuma oferta encontrada com o criterio 'Credenciado'")
            
            # Mostra exemplos de cursoNome disponíveis
            cursos_unicos = set(oferta.get('cursoNome') for oferta in ofertas if oferta.get('cursoNome'))
            if cursos_unicos:
                print("\nExemplos de cursoNome disponiveis:")
                for curso in sorted(cursos_unicos)[:10]:
                    print(f"  - {curso}")
        
        return resultado, total_ofertas
        
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisicao: {e}")
        return None, 0
    except Exception as e:
        print(f"Erro ao processar dados: {e}")
        import traceback
        traceback.print_exc()
        return None, 0

if __name__ == "__main__":
    ofertas, total = buscar_ofertas_filtradas()