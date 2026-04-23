import requests
import json
from datetime import datetime
import time

class CRMOfertasCadastro:
    def __init__(self):
        self.url = "https://crmhmv.apprubeus.com.br/api/Curso/cadastroOferta"
        self.token = "d2cc15f39418956cd23eca96b49681ec"
        self.resultados = []
        
    def processar_cod_local_oferta(self, cod_local_str):
        """
        Converte string de codLocalOferta separado por vírgulas para lista
        """
        cod_local_final = []
        
        # Processa a string separada por vírgulas
        if isinstance(cod_local_str, str) and cod_local_str.strip():
            items = [item.strip() for item in cod_local_str.split(',')]
            cod_local_final.extend(items)
        
        # Garante que PRV-0 esteja na lista, mas sem duplicar
        if "PRV-0" not in cod_local_final:
            cod_local_final.insert(0, "PRV-0")
        
        return cod_local_final
    
    def criar_payload(self, item):
        """
        Cria o payload para a requisição
        """
        cod_local_processado = self.processar_cod_local_oferta(item.get("codLocalOferta", ""))
        
        payload = {
            "nome": item.get("nome", ""),
            "id": item.get("id", ""),
            "codCurso": item.get("codCurso", "2"),
            "codModalidade": item.get("codModalidade", "2.1"),
            "codNivelEnsino": item.get("codNivelEnsino", "N/A"),
            "codLocalOferta": cod_local_processado,
            "codUnidade": "UN1",
            "contexto": "1",
            "origem": "9",
            "token": self.token
        }
        return payload
    
    def fazer_requisicao(self, payload):
        """
        Faz a requisição POST para o CRM
        """
        headers = {
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(
                self.url, 
                data=json.dumps(payload), 
                headers=headers,
                timeout=30
            )
            return response
        except requests.exceptions.RequestException as e:
            print(f"[ERRO] Erro na requisição: {e}")
            return None
    
    def processar_lista_ofertas(self, lista_ofertas):
        """
        Processa toda a lista de ofertas
        """
        total_itens = len(lista_ofertas)
        print(f"=== INICIANDO CADASTRO DE {total_itens} OFERTAS ===\n")
        
        for i, item in enumerate(lista_ofertas, 1):
            nome = item.get("nome", "Sem nome")
            id_oferta = item.get("id", "Sem id")
            
            print(f"Processando item {i}/{total_itens}: {nome} - {id_oferta}")
            
            # Criar payload
            payload = self.criar_payload(item)
            
            # Fazer requisição
            response = self.fazer_requisicao(payload)
            
            if response is not None:
                if response.status_code == 200 or response.status_code == 201:
                    print(f"[SUCESSO] - Item {i} - {nome} - {id_oferta}")
                    self.resultados.append({
                        "item": i,
                        "nome": nome,
                        "id": id_oferta,
                        "status": "SUCESSO",
                        "status_code": response.status_code,
                        "response": response.text
                    })
                else:
                    print(f"[ERRO] - Item {i} - {nome} - {id_oferta} - Status: {response.status_code}")
                    self.resultados.append({
                        "item": i,
                        "nome": nome,
                        "id": id_oferta,
                        "status": "ERRO",
                        "status_code": response.status_code,
                        "response": response.text
                    })
            else:
                print(f"[ERRO] - Item {i} - {nome} - {id_oferta} - Falha na requisição")
                self.resultados.append({
                    "item": i,
                    "nome": nome,
                    "id": id_oferta,
                    "status": "ERRO",
                    "status_code": "N/A",
                    "response": "Falha na requisição"
                })
            
            # Pequena pausa entre requisições
            time.sleep(0.5)
            print()
    
    def gerar_relatorio(self):
        """
        Gera relatório final
        """
        sucessos = sum(1 for r in self.resultados if r["status"] == "SUCESSO")
        erros = sum(1 for r in self.resultados if r["status"] == "ERRO")
        total = len(self.resultados)
        
        print("=" * 60)
        print("RELATÓRIO FINAL DE CADASTRO DE OFERTAS")
        print("=" * 60)
        print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Total de itens processados: {total}")
        print(f"Sucessos: {sucessos}")
        print(f"Erros: {erros}")
        print(f"Taxa de sucesso: {(sucessos/total*100):.1f}%" if total > 0 else "0%")
        print()
        
        # Detalhes dos sucessos
        if sucessos > 0:
            print("ITENS CADASTRADOS COM SUCESSO:")
            print("-" * 40)
            for resultado in self.resultados:
                if resultado["status"] == "SUCESSO":
                    print(f"[OK] Item {resultado['item']}: {resultado['nome']} - {resultado['id']}")
            print()
        
        # Detalhes dos erros
        if erros > 0:
            print("ITENS COM ERRO:")
            print("-" * 40)
            for resultado in self.resultados:
                if resultado["status"] == "ERRO":
                    print(f"[ERRO] Item {resultado['item']}: {resultado['nome']} - {resultado['id']}")
                    print(f"  Status Code: {resultado['status_code']}")
                    print(f"  Response: {resultado['response']}")
                    print()
        
        # Salvar relatório em arquivo
        self.salvar_relatorio_arquivo()
    
    def salvar_relatorio_arquivo(self):
        """
        Salva o relatório em arquivo JSON
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nome_arquivo = f"relatorio_cadastro_ofertas_{timestamp}.json"
        
        relatorio_completo = {
            "timestamp": datetime.now().isoformat(),
            "total_processados": len(self.resultados),
            "sucessos": sum(1 for r in self.resultados if r["status"] == "SUCESSO"),
            "erros": sum(1 for r in self.resultados if r["status"] == "ERRO"),
            "detalhes": self.resultados
        }
        
        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                json.dump(relatorio_completo, f, indent=2, ensure_ascii=False)
            print(f"Relatório salvo em: {nome_arquivo}")
        except Exception as e:
            print(f"Erro ao salvar relatório: {e}")

# LISTA DE DADOS
def main():
    lista_ofertas = [
# {"nome": "ACUPUNTURA","id": "196","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "CIRURGIA DO APARELHO DIGESTIVO","id": "108","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA GERAL","id": "197","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-2, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-23, PRV-CIR-24, PRV-CIR-25, PRV-CIR-48, PRV-CIR-55, PRV-CIR-58, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA ONCOLÓGICA","id": "198","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-46, PRV-CIR-54"},
# {"nome": "CIRURGIA PEDIÁTRICA","id": "199","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-13, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-23, PRV-CIR-24, PRV-CIR-25, PRV-CIR-48, PRV-CIR-53, PRV-CIR-54, PRV-CIR-55, PRV-CIR-57, PRV-CIR-58, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-ESP-41"},
# {"nome": "CIRURGIA PLÁSTICA","id": "200","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-11, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-24, PRV-CIR-ESP-70, PRV-CIR-74, PRV-CIR-75"},
# {"nome": "CIRURGIA TORÁCICA","id": "201","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-8, PRV-CIR-14, PRV-CIR-15, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-21, PRV-CIR-22, PRV-CIR-53, PRV-CIR-54, PRV-CIR-55, PRV-CIR-ESP-56, PRV-CIR-57, PRV-CIR-58, PRV-CIR-59, PRV-CIR-60, PRV-CIR-61, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-62, PRV-CIR-63, PRV-CIR-64, PRV-CIR-ESP-65"},
# {"nome": "CIRURGIA VASCULAR","id": "202","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "CIRURGIÃO DENTISTA","id": "203","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-ODO-1, PRV-ODO-2, PRV-ODO-ESP-3"},
# {"nome": "CLÍNICA MÉDICA","id": "204","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-10, PRV-CLI-ESP-12, PRV-CLI-15"},
# {"nome": "COLOPROCTOLOGIA","id": "205","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-2, PRV-CIR-5, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-25, PRV-CIR-39, PRV-CIR-40, PRV-CIR-42, PRV-CIR-ESP-43, PRV-CIR-ESP-44, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-ESP-41"},
# {"nome": "ALERGIA E IMUNOLOGIA","id": "101","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "DERMATOLOGIA","id": "206","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-54, PRV-CLI-60"},
# {"nome": "ENDOCRINOLOGIA E METABOLOGIA","id": "207","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "ENDOSCOPIA","id": "208","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-ENDO-1, PRV-ENDO-2, PRV-ENDO-3"},
# {"nome": "GASTROENTEROLOGIA","id": "209","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-7, PRV-CLI-ESP-23, PRV-CLI-ESP-24, PRV-CLI-ESP-25, PRV-CLI-ESP-26, PRV-CLI-ESP-27, PRV-CLI-ESP-28, PRV-CLI-ESP-29, PRV-CLI-ESP-30, PRV-CLI-ESP-31, PRV-CLI-ESP-32"},
# {"nome": "GENÉTICA MÉDICA","id": "210","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "GERIATRIA","id": "211","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "GINECOLOGIA E OBSTETRÍCIA","id": "212","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-GO-ESP-6, PRV-GO-ESP-7, PRV-GO-8, PRV-GO-1, PRV-GO-2, PRV-GO-3, PRV-GO-4, PRV-GO-ESP-5, PRV-CIR-ESP-27"},
# {"nome": "HEMATOLOGIA E HEMOTERAPIA","id": "213","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-7, PRV-CLI-8, PRV-CLI-39, PRV-CLI-AVA-40"},
# {"nome": "HOMEOPATIA","id": "214","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "INFECTOLOGIA","id": "215","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-7, PRV-CLI-10"},
# {"nome": "ANESTESIOLOGIA","id": "102","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "MASTOLOGIA","id": "216","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-6, PRV-CIR-14, PRV-CIR-17, PRV-CIR-45, PRV-CIR-46, PRV-CIR-47, PRV-CIR-48, PRV-CIR-ESP-70"},
# {"nome": "MEDICINA DE EMERGÊNCIA","id": "217","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-9, PRV-CLI-10, PRV-CLI-11, PRV-CLI-13, PRV-CLI-15, PRV-CLI-56, PRV-CLI-62"},
# {"nome": "MEDICINA DE FAMÍLIA E COMUNIDADE","id": "218","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "MEDICINA DO TRABALHO","id": "219","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "MEDICINA DO TRÁFEGO","id": "220","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "MEDICINA ESPORTIVA","id": "221","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "MEDICINA FÍSICA E REABILITAÇÃO","id": "222","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "MEDICINA INTENSIVA","id": "223","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-9, PRV-CLI-10, PRV-CLI-11, PRV-CLI-ESP-12, PRV-CLI-13, PRV-CLI-15, PRV-CLI-56, PRV-CLI-62"},
# {"nome": "MEDICINA LEGAL E PERÍCIA MÉDICA","id": "224","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "MEDICINA NUCLEAR","id": "225","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "ANGIOLOGIA","id": "103","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-4, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-21, PRV-CIR-31, PRV-CIR-36, PRV-CIR-37, PRV-CIR-ESP-38, PRV-CIR-ESP-70, PRV-CIR-ESP-27"},
# {"nome": "MEDICINA PREVENTIVA SOCIAL","id": "226","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "NEFROLOGIA","id": "227","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-7, PRV-CLI-33, PRV-CLI-34, PRV-CLI-35, PRV-CLI-36, PRV-CLI-37, PRV-CLI-38"},
# {"nome": "NEUROCIRURGIA","id": "228","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-7, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-18, PRV-CIR-19, PRV-CIR-49, PRV-CIR-50, PRV-CIR-51, PRV-CIR-ESP-52, PRV-CIR-ESP-70"},
# {"nome": "NEUROLOGIA","id": "229","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-8, PRV-CLI-10, PRV-CLI-ESP-49, PRV-CLI-ESP-50, PRV-CLI-ESP-51, PRV-CLI-ESP-52, PRV-CLI-ESP-53, PRV-CLI-54"},
# {"nome": "NUTROLOGIA","id": "230","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-ESP-12"},
# {"nome": "OFTALMOLOGIA","id": "231","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-61"},
# {"nome": "ONCOLOGIA CLÍNICA","id": "232","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-RESID-1"},
# {"nome": "ORTOPEDIA E TRAUMATOLOGIA","id": "233","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-12, PRV-CIR-14, PRV-CIR-18, PRV-CIR-ESP-70, PRV-CIR-71, PRV-CIR-72, PRV-CIR-76, PRV-CIR-77, PRV-CIR-ESP-27"},
# {"nome": "OTORRINOLARINGOLOGIA","id": "234","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-OTO-1, PRV-OTO-2, PRV-OTO-3, PRV-OTO-4, PRV-OTO-5, PRV-OTO-6, PRV-OTO-7, PRV-OTO-8, PRV-OTO-9, PRV-OTO-10, PRV-OTO-11, PRV-OTO-12, PRV-OTO-13, PRV-OTO-14, PRV-OTO-AVA-15"},
# {"nome": "PATOLOGIA","id": "235","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-PAT-1, PRV-PAT-2, PRV-PAT-3, PRV-PAT-4, PRV-PAT-5, PRV-PAT-6, PRV-PAT-7"},
# {"nome": "CARDIOLOGIA","id": "105","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-13, PRV-CLI-14, PRV-CLI-15, PRV-CLI-16, PRV-CLI-22, PRV-CLI-ESP-63"},
# {"nome": "PATOLOGIA CLÍNICA / MEDICINA LABORATORIAL","id": "236","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "PEDIATRIA","id": "237","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-PED-1, PRV-PED-2, PRV-PED-AVA-3, PRV-PED-4, PRV-PED-6, PRV-PED-7, PRV-PED-8, PRV-PED-9, PRV-PED-10, PRV-PED-ESP-11, PRV-PED-12, PRV-PED-13, PRV-PED-14, PRV-PED-15, PRV-PED-16, PRV-PED-17, PRV-PED-18, PRV-CLI-AVA-40"},
# {"nome": "PNEUMOLOGIA","id": "238","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-7, PRV-CLI-8, PRV-CLI-9, PRV-CLI-11, PRV-CLI-42, PRV-CLI-43, PRV-CLI-ESP-47, PRV-CLI-ESP-41, PRV-CLI-44, PRV-CLI-45, PRV-CLI-ESP-46, PRV-CLI-ESP-48"},
# {"nome": "PSIQUIATRIA","id": "239","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-55"},
# {"nome": "RADIOLOGIA E DIAGNÓSTICO POR IMAGEM","id": "240","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "RADIOTERAPIA","id": "241","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-RAD-1, PRV-RAD-2, PRV-RAD-3, PRV-RAD-4, PRV-RAD-5, PRV-RAD-6, PRV-RAD-7, PRV-RAD-8"},
# {"nome": "REUMATOLOGIA","id": "242","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-57, PRV-CLI-58, PRV-CLI-59"},
# {"nome": "UROLOGIA","id": "243","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-9, PRV-CIR-14, PRV-CIR-15, PRV-CIR-25, PRV-CIR-ESP-66, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-ESP-67, PRV-CIR-ESP-68, PRV-CIR-ESP-69"},
# {"nome": "CIRURGIA BUCO-MAXILO-FACIAL","id": "104","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "CIRURGIA CARDIOVASCULAR","id": "109","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-3, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-21, PRV-CIR-22, PRV-CIR-28, PRV-CIR-29, PRV-CIR-30, PRV-CIR-31, PRV-CIR-32, PRV-CIR-33, PRV-CIR-34, PRV-CIR-35, PRV-CIR-ESP-38, PRV-CIR-ESP-70, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA DE CABEÇA E PESCOÇO","id": "106","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-10, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-23, PRV-CIR-ESP-70, PRV-CIR-73, PRV-CIR-ESP-27"},
# {"nome": "ACUPUNTURA","id": "111","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "CIRURGIA DO APARELHO DIGESTIVO","id": "120","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA GERAL","id": "244","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-2, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-23, PRV-CIR-24, PRV-CIR-25, PRV-CIR-48, PRV-CIR-55, PRV-CIR-58, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA ONCOLÓGICA","id": "245","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-46, PRV-CIR-54"},
# {"nome": "CIRURGIA PEDIÁTRICA","id": "246","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-13, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-23, PRV-CIR-24, PRV-CIR-25, PRV-CIR-48, PRV-CIR-53, PRV-CIR-54, PRV-CIR-55, PRV-CIR-57, PRV-CIR-58, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-ESP-41"},
# {"nome": "CIRURGIA PLÁSTICA","id": "247","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-11, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-24, PRV-CIR-ESP-70, PRV-CIR-74, PRV-CIR-75"},
# {"nome": "CIRURGIA TORÁCICA","id": "248","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-8, PRV-CIR-14, PRV-CIR-15, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-21, PRV-CIR-22, PRV-CIR-53, PRV-CIR-54, PRV-CIR-55, PRV-CIR-ESP-56, PRV-CIR-57, PRV-CIR-58, PRV-CIR-59, PRV-CIR-60, PRV-CIR-61, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-62, PRV-CIR-63, PRV-CIR-64, PRV-CIR-ESP-65"},
# {"nome": "CIRURGIA VASCULAR","id": "249","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "CIRURGIÃO DENTISTA","id": "250","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-ODO-1, PRV-ODO-2, PRV-ODO-ESP-3"},
# {"nome": "CLÍNICA MÉDICA","id": "251","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-10, PRV-CLI-ESP-12, PRV-CLI-15"},
# {"nome": "COLOPROCTOLOGIA","id": "252","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-2, PRV-CIR-5, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-25, PRV-CIR-39, PRV-CIR-40, PRV-CIR-42, PRV-CIR-ESP-43, PRV-CIR-ESP-44, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-ESP-41"},
# {"nome": "ALERGIA E IMUNOLOGIA","id": "112","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "DERMATOLOGIA","id": "253","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-54, PRV-CLI-60"},
# {"nome": "ENDOCRINOLOGIA E METABOLOGIA","id": "254","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "ENDOSCOPIA","id": "255","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-ENDO-1, PRV-ENDO-2, PRV-ENDO-3"},
# {"nome": "GASTROENTEROLOGIA","id": "256","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-7, PRV-CLI-ESP-23, PRV-CLI-ESP-24, PRV-CLI-ESP-25, PRV-CLI-ESP-26, PRV-CLI-ESP-27, PRV-CLI-ESP-28, PRV-CLI-ESP-29, PRV-CLI-ESP-30, PRV-CLI-ESP-31, PRV-CLI-ESP-32"},
# {"nome": "GENÉTICA MÉDICA","id": "257","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "GERIATRIA","id": "258","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "GINECOLOGIA E OBSTETRÍCIA","id": "259","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-GO-ESP-6, PRV-GO-ESP-7, PRV-GO-8, PRV-GO-1, PRV-GO-2, PRV-GO-3, PRV-GO-4, PRV-GO-ESP-5, PRV-CIR-ESP-27"},
# {"nome": "HEMATOLOGIA E HEMOTERAPIA","id": "260","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-7, PRV-CLI-8, PRV-CLI-39, PRV-CLI-AVA-40"},
# {"nome": "HOMEOPATIA","id": "261","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "INFECTOLOGIA","id": "262","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-7, PRV-CLI-10"},
# {"nome": "ANESTESIOLOGIA","id": "113","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "MASTOLOGIA","id": "263","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-6, PRV-CIR-14, PRV-CIR-17, PRV-CIR-45, PRV-CIR-46, PRV-CIR-47, PRV-CIR-48, PRV-CIR-ESP-70"},
# {"nome": "MEDICINA DE EMERGÊNCIA","id": "264","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-9, PRV-CLI-10, PRV-CLI-11, PRV-CLI-13, PRV-CLI-15, PRV-CLI-56, PRV-CLI-62"},
# {"nome": "MEDICINA DE FAMÍLIA E COMUNIDADE","id": "265","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "MEDICINA DO TRABALHO","id": "266","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "MEDICINA DO TRÁFEGO","id": "267","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "MEDICINA ESPORTIVA","id": "268","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "MEDICINA FÍSICA E REABILITAÇÃO","id": "269","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "MEDICINA INTENSIVA","id": "270","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-9, PRV-CLI-10, PRV-CLI-11, PRV-CLI-ESP-12, PRV-CLI-13, PRV-CLI-15, PRV-CLI-56, PRV-CLI-62"},
# {"nome": "MEDICINA LEGAL E PERÍCIA MÉDICA","id": "271","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "MEDICINA NUCLEAR","id": "272","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "ANGIOLOGIA","id": "114","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-4, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-21, PRV-CIR-31, PRV-CIR-36, PRV-CIR-37, PRV-CIR-ESP-38, PRV-CIR-ESP-70, PRV-CIR-ESP-27"},
# {"nome": "MEDICINA PREVENTIVA SOCIAL","id": "273","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "NEFROLOGIA","id": "274","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-7, PRV-CLI-33, PRV-CLI-34, PRV-CLI-35, PRV-CLI-36, PRV-CLI-37, PRV-CLI-38"},
# {"nome": "NEUROCIRURGIA","id": "275","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-7, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-18, PRV-CIR-19, PRV-CIR-49, PRV-CIR-50, PRV-CIR-51, PRV-CIR-ESP-52, PRV-CIR-ESP-70"},
# {"nome": "NEUROLOGIA","id": "276","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-8, PRV-CLI-10, PRV-CLI-ESP-49, PRV-CLI-ESP-50, PRV-CLI-ESP-51, PRV-CLI-ESP-52, PRV-CLI-ESP-53, PRV-CLI-54"},
# {"nome": "NUTROLOGIA","id": "277","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-ESP-12"},
# {"nome": "OFTALMOLOGIA","id": "278","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-61"},
# {"nome": "ONCOLOGIA CLÍNICA","id": "279","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-RESID-1"},
# {"nome": "ORTOPEDIA E TRAUMATOLOGIA","id": "280","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-12, PRV-CIR-14, PRV-CIR-18, PRV-CIR-ESP-70, PRV-CIR-71, PRV-CIR-72, PRV-CIR-76, PRV-CIR-77, PRV-CIR-ESP-27"},
# {"nome": "OTORRINOLARINGOLOGIA","id": "281","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-OTO-1, PRV-OTO-2, PRV-OTO-3, PRV-OTO-4, PRV-OTO-5, PRV-OTO-6, PRV-OTO-7, PRV-OTO-8, PRV-OTO-9, PRV-OTO-10, PRV-OTO-11, PRV-OTO-12, PRV-OTO-13, PRV-OTO-14, PRV-OTO-AVA-15"},
# {"nome": "PATOLOGIA","id": "282","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-PAT-1, PRV-PAT-2, PRV-PAT-3, PRV-PAT-4, PRV-PAT-5, PRV-PAT-6, PRV-PAT-7"},
# {"nome": "CARDIOLOGIA","id": "115","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-13, PRV-CLI-14, PRV-CLI-15, PRV-CLI-16, PRV-CLI-22, PRV-CLI-ESP-63"},
# {"nome": "PATOLOGIA CLÍNICA / MEDICINA LABORATORIAL","id": "283","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "PEDIATRIA","id": "284","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-PED-1, PRV-PED-2, PRV-PED-AVA-3, PRV-PED-4, PRV-PED-6, PRV-PED-7, PRV-PED-8, PRV-PED-9, PRV-PED-10, PRV-PED-ESP-11, PRV-PED-12, PRV-PED-13, PRV-PED-14, PRV-PED-15, PRV-PED-16, PRV-PED-17, PRV-PED-18, PRV-CLI-AVA-40"},
# {"nome": "PNEUMOLOGIA","id": "285","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-7, PRV-CLI-8, PRV-CLI-9, PRV-CLI-11, PRV-CLI-42, PRV-CLI-43, PRV-CLI-ESP-47, PRV-CLI-ESP-41, PRV-CLI-44, PRV-CLI-45, PRV-CLI-ESP-46, PRV-CLI-ESP-48"},
# {"nome": "PSIQUIATRIA","id": "286","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-55"},
# {"nome": "RADIOLOGIA E DIAGNÓSTICO POR IMAGEM","id": "287","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "RADIOTERAPIA","id": "288","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-RAD-1, PRV-RAD-2, PRV-RAD-3, PRV-RAD-4, PRV-RAD-5, PRV-RAD-6, PRV-RAD-7, PRV-RAD-8"},
# {"nome": "REUMATOLOGIA","id": "289","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-57, PRV-CLI-58, PRV-CLI-59"},
# {"nome": "UROLOGIA","id": "290","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-9, PRV-CIR-14, PRV-CIR-15, PRV-CIR-25, PRV-CIR-ESP-66, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-ESP-67, PRV-CIR-ESP-68, PRV-CIR-ESP-69"},
# {"nome": "CIRURGIA BUCO-MAXILO-FACIAL","id": "116","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "CIRURGIA CARDIOVASCULAR","id": "117","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-3, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-21, PRV-CIR-22, PRV-CIR-28, PRV-CIR-29, PRV-CIR-30, PRV-CIR-31, PRV-CIR-32, PRV-CIR-33, PRV-CIR-34, PRV-CIR-35, PRV-CIR-ESP-38, PRV-CIR-ESP-70, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA DE CABEÇA E PESCOÇO","id": "119","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-10, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-23, PRV-CIR-ESP-70, PRV-CIR-73, PRV-CIR-ESP-27"},
# {"nome": "ACUPUNTURA","id": "142","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "CIRURGIA DO APARELHO DIGESTIVO","id": "184","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA GERAL","id": "480","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-2, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-23, PRV-CIR-24, PRV-CIR-25, PRV-CIR-48, PRV-CIR-55, PRV-CIR-58, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA ONCOLÓGICA","id": "481","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-46, PRV-CIR-54"},
# {"nome": "CIRURGIA PEDIÁTRICA","id": "482","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-13, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-23, PRV-CIR-24, PRV-CIR-25, PRV-CIR-48, PRV-CIR-53, PRV-CIR-54, PRV-CIR-55, PRV-CIR-57, PRV-CIR-58, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-ESP-41"},
# {"nome": "CIRURGIA PLÁSTICA","id": "483","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-11, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-24, PRV-CIR-ESP-70, PRV-CIR-74, PRV-CIR-75"},
# {"nome": "CIRURGIA TORÁCICA","id": "484","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-8, PRV-CIR-14, PRV-CIR-15, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-21, PRV-CIR-22, PRV-CIR-53, PRV-CIR-54, PRV-CIR-55, PRV-CIR-ESP-56, PRV-CIR-57, PRV-CIR-58, PRV-CIR-59, PRV-CIR-60, PRV-CIR-61, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-62, PRV-CIR-63, PRV-CIR-64, PRV-CIR-ESP-65"},
# {"nome": "CIRURGIA VASCULAR","id": "485","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "CIRURGIÃO DENTISTA","id": "486","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-ODO-1, PRV-ODO-2, PRV-ODO-ESP-3"},
# {"nome": "CLÍNICA MÉDICA","id": "487","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-10, PRV-CLI-ESP-12, PRV-CLI-15"},
# {"nome": "COLOPROCTOLOGIA","id": "488","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-2, PRV-CIR-5, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-25, PRV-CIR-39, PRV-CIR-40, PRV-CIR-42, PRV-CIR-ESP-43, PRV-CIR-ESP-44, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-ESP-41"},
# {"nome": "ALERGIA E IMUNOLOGIA","id": "143","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "DERMATOLOGIA","id": "489","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-54, PRV-CLI-60"},
# {"nome": "ENDOCRINOLOGIA E METABOLOGIA","id": "490","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "ENDOSCOPIA","id": "491","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-ENDO-1, PRV-ENDO-2, PRV-ENDO-3"},
# {"nome": "GASTROENTEROLOGIA","id": "492","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-7, PRV-CLI-ESP-23, PRV-CLI-ESP-24, PRV-CLI-ESP-25, PRV-CLI-ESP-26, PRV-CLI-ESP-27, PRV-CLI-ESP-28, PRV-CLI-ESP-29, PRV-CLI-ESP-30, PRV-CLI-ESP-31, PRV-CLI-ESP-32"},
# {"nome": "GENÉTICA MÉDICA","id": "493","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "GERIATRIA","id": "494","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "GINECOLOGIA E OBSTETRÍCIA","id": "495","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-GO-ESP-6, PRV-GO-ESP-7, PRV-GO-8, PRV-GO-1, PRV-GO-2, PRV-GO-3, PRV-GO-4, PRV-GO-ESP-5, PRV-CIR-ESP-27"},
# {"nome": "HEMATOLOGIA E HEMOTERAPIA","id": "496","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-7, PRV-CLI-8, PRV-CLI-39, PRV-CLI-AVA-40"},
# {"nome": "HOMEOPATIA","id": "497","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "INFECTOLOGIA","id": "498","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-7, PRV-CLI-10"},
# {"nome": "ANESTESIOLOGIA","id": "144","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "MASTOLOGIA","id": "499","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-6, PRV-CIR-14, PRV-CIR-17, PRV-CIR-45, PRV-CIR-46, PRV-CIR-47, PRV-CIR-48, PRV-CIR-ESP-70"},
# {"nome": "MEDICINA DE EMERGÊNCIA","id": "500","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-9, PRV-CLI-10, PRV-CLI-11, PRV-CLI-13, PRV-CLI-15, PRV-CLI-56, PRV-CLI-62"},
# {"nome": "MEDICINA DE FAMÍLIA E COMUNIDADE","id": "501","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "MEDICINA DO TRABALHO","id": "502","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "MEDICINA DO TRÁFEGO","id": "503","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "MEDICINA ESPORTIVA","id": "504","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "MEDICINA FÍSICA E REABILITAÇÃO","id": "505","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "MEDICINA INTENSIVA","id": "506","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-9, PRV-CLI-10, PRV-CLI-11, PRV-CLI-ESP-12, PRV-CLI-13, PRV-CLI-15, PRV-CLI-56, PRV-CLI-62"},
# {"nome": "MEDICINA LEGAL E PERÍCIA MÉDICA","id": "507","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "MEDICINA NUCLEAR","id": "508","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "ANGIOLOGIA","id": "145","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-4, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-21, PRV-CIR-31, PRV-CIR-36, PRV-CIR-37, PRV-CIR-ESP-38, PRV-CIR-ESP-70, PRV-CIR-ESP-27"},
# {"nome": "MEDICINA PREVENTIVA SOCIAL","id": "509","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "NEFROLOGIA","id": "510","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-7, PRV-CLI-33, PRV-CLI-34, PRV-CLI-35, PRV-CLI-36, PRV-CLI-37, PRV-CLI-38"},
# {"nome": "NEUROCIRURGIA","id": "511","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-7, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-18, PRV-CIR-19, PRV-CIR-49, PRV-CIR-50, PRV-CIR-51, PRV-CIR-ESP-52, PRV-CIR-ESP-70"},
# {"nome": "NEUROLOGIA","id": "512","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-8, PRV-CLI-10, PRV-CLI-ESP-49, PRV-CLI-ESP-50, PRV-CLI-ESP-51, PRV-CLI-ESP-52, PRV-CLI-ESP-53, PRV-CLI-54"},
# {"nome": "NUTROLOGIA","id": "513","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-ESP-12"},
# {"nome": "OFTALMOLOGIA","id": "514","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-61"},
# {"nome": "ONCOLOGIA CLÍNICA","id": "515","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-RESID-1"},
# {"nome": "ORTOPEDIA E TRAUMATOLOGIA","id": "516","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-12, PRV-CIR-14, PRV-CIR-18, PRV-CIR-ESP-70, PRV-CIR-71, PRV-CIR-72, PRV-CIR-76, PRV-CIR-77, PRV-CIR-ESP-27"},
# {"nome": "OTORRINOLARINGOLOGIA","id": "517","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-OTO-1, PRV-OTO-2, PRV-OTO-3, PRV-OTO-4, PRV-OTO-5, PRV-OTO-6, PRV-OTO-7, PRV-OTO-8, PRV-OTO-9, PRV-OTO-10, PRV-OTO-11, PRV-OTO-12, PRV-OTO-13, PRV-OTO-14, PRV-OTO-AVA-15"},
# {"nome": "PATOLOGIA","id": "518","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-PAT-1, PRV-PAT-2, PRV-PAT-3, PRV-PAT-4, PRV-PAT-5, PRV-PAT-6, PRV-PAT-7"},
# {"nome": "CARDIOLOGIA","id": "146","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-13, PRV-CLI-14, PRV-CLI-15, PRV-CLI-16, PRV-CLI-22, PRV-CLI-ESP-63"},
# {"nome": "PATOLOGIA CLÍNICA / MEDICINA LABORATORIAL","id": "519","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "PEDIATRIA","id": "520","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-PED-1, PRV-PED-2, PRV-PED-AVA-3, PRV-PED-4, PRV-PED-6, PRV-PED-7, PRV-PED-8, PRV-PED-9, PRV-PED-10, PRV-PED-ESP-11, PRV-PED-12, PRV-PED-13, PRV-PED-14, PRV-PED-15, PRV-PED-16, PRV-PED-17, PRV-PED-18, PRV-CLI-AVA-40"},
# {"nome": "PNEUMOLOGIA","id": "521","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-7, PRV-CLI-8, PRV-CLI-9, PRV-CLI-11, PRV-CLI-42, PRV-CLI-43, PRV-CLI-ESP-47, PRV-CLI-ESP-41, PRV-CLI-44, PRV-CLI-45, PRV-CLI-ESP-46, PRV-CLI-ESP-48"},
# {"nome": "PSIQUIATRIA","id": "522","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-55"},
# {"nome": "RADIOLOGIA E DIAGNÓSTICO POR IMAGEM","id": "523","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "RADIOTERAPIA","id": "524","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-RAD-1, PRV-RAD-2, PRV-RAD-3, PRV-RAD-4, PRV-RAD-5, PRV-RAD-6, PRV-RAD-7, PRV-RAD-8"},
# {"nome": "REUMATOLOGIA","id": "525","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-57, PRV-CLI-58, PRV-CLI-59"},
# {"nome": "UROLOGIA","id": "526","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-9, PRV-CIR-14, PRV-CIR-15, PRV-CIR-25, PRV-CIR-ESP-66, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-ESP-67, PRV-CIR-ESP-68, PRV-CIR-ESP-69"},
# {"nome": "CIRURGIA BUCO-MAXILO-FACIAL","id": "180","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "CIRURGIA CARDIOVASCULAR","id": "181","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-3, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-21, PRV-CIR-22, PRV-CIR-28, PRV-CIR-29, PRV-CIR-30, PRV-CIR-31, PRV-CIR-32, PRV-CIR-33, PRV-CIR-34, PRV-CIR-35, PRV-CIR-ESP-38, PRV-CIR-ESP-70, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA DE CABEÇA E PESCOÇO","id": "183","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-10, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-23, PRV-CIR-ESP-70, PRV-CIR-73, PRV-CIR-ESP-27"},
# {"nome": "ACUPUNTURA","id": "131","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "CIRURGIA DO APARELHO DIGESTIVO","id": "164","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA GERAL","id": "291","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-2, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-23, PRV-CIR-24, PRV-CIR-25, PRV-CIR-48, PRV-CIR-55, PRV-CIR-58, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA ONCOLÓGICA","id": "292","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-46, PRV-CIR-54"},
# {"nome": "CIRURGIA PEDIÁTRICA","id": "293","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-13, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-23, PRV-CIR-24, PRV-CIR-25, PRV-CIR-48, PRV-CIR-53, PRV-CIR-54, PRV-CIR-55, PRV-CIR-57, PRV-CIR-58, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-ESP-41"},
# {"nome": "CIRURGIA PLÁSTICA","id": "294","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-11, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-24, PRV-CIR-ESP-70, PRV-CIR-74, PRV-CIR-75"},
# {"nome": "CIRURGIA TORÁCICA","id": "295","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-8, PRV-CIR-14, PRV-CIR-15, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-21, PRV-CIR-22, PRV-CIR-53, PRV-CIR-54, PRV-CIR-55, PRV-CIR-ESP-56, PRV-CIR-57, PRV-CIR-58, PRV-CIR-59, PRV-CIR-60, PRV-CIR-61, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-62, PRV-CIR-63, PRV-CIR-64, PRV-CIR-ESP-65"},
# {"nome": "CIRURGIA VASCULAR","id": "296","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "CIRURGIÃO DENTISTA","id": "297","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-ODO-1, PRV-ODO-2, PRV-ODO-ESP-3"},
# {"nome": "CLÍNICA MÉDICA","id": "298","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-10, PRV-CLI-ESP-12, PRV-CLI-15"},
# {"nome": "COLOPROCTOLOGIA","id": "299","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-2, PRV-CIR-5, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-25, PRV-CIR-39, PRV-CIR-40, PRV-CIR-42, PRV-CIR-ESP-43, PRV-CIR-ESP-44, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-ESP-41"},
# {"nome": "ALERGIA E IMUNOLOGIA","id": "132","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "DERMATOLOGIA","id": "300","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-54, PRV-CLI-60"},
# {"nome": "ENDOCRINOLOGIA E METABOLOGIA","id": "301","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "ENDOSCOPIA","id": "302","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-ENDO-1, PRV-ENDO-2, PRV-ENDO-3"},
# {"nome": "GASTROENTEROLOGIA","id": "303","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-7, PRV-CLI-ESP-23, PRV-CLI-ESP-24, PRV-CLI-ESP-25, PRV-CLI-ESP-26, PRV-CLI-ESP-27, PRV-CLI-ESP-28, PRV-CLI-ESP-29, PRV-CLI-ESP-30, PRV-CLI-ESP-31, PRV-CLI-ESP-32"},
# {"nome": "GENÉTICA MÉDICA","id": "304","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "GERIATRIA","id": "305","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "GINECOLOGIA E OBSTETRÍCIA","id": "306","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-GO-ESP-6, PRV-GO-ESP-7, PRV-GO-8, PRV-GO-1, PRV-GO-2, PRV-GO-3, PRV-GO-4, PRV-GO-ESP-5, PRV-CIR-ESP-27"},
# {"nome": "HEMATOLOGIA E HEMOTERAPIA","id": "307","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-7, PRV-CLI-8, PRV-CLI-39, PRV-CLI-AVA-40"},
# {"nome": "HOMEOPATIA","id": "308","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "INFECTOLOGIA","id": "309","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-7, PRV-CLI-10"},
# {"nome": "ANESTESIOLOGIA","id": "133","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "MASTOLOGIA","id": "310","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-6, PRV-CIR-14, PRV-CIR-17, PRV-CIR-45, PRV-CIR-46, PRV-CIR-47, PRV-CIR-48, PRV-CIR-ESP-70"},
# {"nome": "MEDICINA DE EMERGÊNCIA","id": "311","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-9, PRV-CLI-10, PRV-CLI-11, PRV-CLI-13, PRV-CLI-15, PRV-CLI-56, PRV-CLI-62"},
# {"nome": "MEDICINA DE FAMÍLIA E COMUNIDADE","id": "312","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "MEDICINA DO TRABALHO","id": "313","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "MEDICINA DO TRÁFEGO","id": "314","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "MEDICINA ESPORTIVA","id": "315","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "MEDICINA FÍSICA E REABILITAÇÃO","id": "316","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "MEDICINA INTENSIVA","id": "317","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-9, PRV-CLI-10, PRV-CLI-11, PRV-CLI-ESP-12, PRV-CLI-13, PRV-CLI-15, PRV-CLI-56, PRV-CLI-62"},
# {"nome": "MEDICINA LEGAL E PERÍCIA MÉDICA","id": "318","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "MEDICINA NUCLEAR","id": "319","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "ANGIOLOGIA","id": "134","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-4, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-21, PRV-CIR-31, PRV-CIR-36, PRV-CIR-37, PRV-CIR-ESP-38, PRV-CIR-ESP-70, PRV-CIR-ESP-27"},
# {"nome": "MEDICINA PREVENTIVA SOCIAL","id": "320","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "NEFROLOGIA","id": "321","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-7, PRV-CLI-33, PRV-CLI-34, PRV-CLI-35, PRV-CLI-36, PRV-CLI-37, PRV-CLI-38"},
# {"nome": "NEUROCIRURGIA","id": "322","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-7, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-18, PRV-CIR-19, PRV-CIR-49, PRV-CIR-50, PRV-CIR-51, PRV-CIR-ESP-52, PRV-CIR-ESP-70"},
# {"nome": "NEUROLOGIA","id": "323","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-8, PRV-CLI-10, PRV-CLI-ESP-49, PRV-CLI-ESP-50, PRV-CLI-ESP-51, PRV-CLI-ESP-52, PRV-CLI-ESP-53, PRV-CLI-54"},
# {"nome": "NUTROLOGIA","id": "324","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-ESP-12"},
# {"nome": "OFTALMOLOGIA","id": "325","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-61"},
# {"nome": "ONCOLOGIA CLÍNICA","id": "326","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-RESID-1"},
# {"nome": "ORTOPEDIA E TRAUMATOLOGIA","id": "327","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-12, PRV-CIR-14, PRV-CIR-18, PRV-CIR-ESP-70, PRV-CIR-71, PRV-CIR-72, PRV-CIR-76, PRV-CIR-77, PRV-CIR-ESP-27"},
# {"nome": "OTORRINOLARINGOLOGIA","id": "328","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-OTO-1, PRV-OTO-2, PRV-OTO-3, PRV-OTO-4, PRV-OTO-5, PRV-OTO-6, PRV-OTO-7, PRV-OTO-8, PRV-OTO-9, PRV-OTO-10, PRV-OTO-11, PRV-OTO-12, PRV-OTO-13, PRV-OTO-14, PRV-OTO-AVA-15"},
# {"nome": "PATOLOGIA","id": "329","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-PAT-1, PRV-PAT-2, PRV-PAT-3, PRV-PAT-4, PRV-PAT-5, PRV-PAT-6, PRV-PAT-7"},
# {"nome": "CARDIOLOGIA","id": "135","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-13, PRV-CLI-14, PRV-CLI-15, PRV-CLI-16, PRV-CLI-22, PRV-CLI-ESP-63"},
# {"nome": "PATOLOGIA CLÍNICA / MEDICINA LABORATORIAL","id": "330","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "PEDIATRIA","id": "331","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-PED-1, PRV-PED-2, PRV-PED-AVA-3, PRV-PED-4, PRV-PED-6, PRV-PED-7, PRV-PED-8, PRV-PED-9, PRV-PED-10, PRV-PED-ESP-11, PRV-PED-12, PRV-PED-13, PRV-PED-14, PRV-PED-15, PRV-PED-16, PRV-PED-17, PRV-PED-18, PRV-CLI-AVA-40"},
# {"nome": "PNEUMOLOGIA","id": "332","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-7, PRV-CLI-8, PRV-CLI-9, PRV-CLI-11, PRV-CLI-42, PRV-CLI-43, PRV-CLI-ESP-47, PRV-CLI-ESP-41, PRV-CLI-44, PRV-CLI-45, PRV-CLI-ESP-46, PRV-CLI-ESP-48"},
# {"nome": "PSIQUIATRIA","id": "333","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-55"},
# {"nome": "RADIOLOGIA E DIAGNÓSTICO POR IMAGEM","id": "334","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "RADIOTERAPIA","id": "335","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-RAD-1, PRV-RAD-2, PRV-RAD-3, PRV-RAD-4, PRV-RAD-5, PRV-RAD-6, PRV-RAD-7, PRV-RAD-8"},
# {"nome": "REUMATOLOGIA","id": "336","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-57, PRV-CLI-58, PRV-CLI-59"},
# {"nome": "UROLOGIA","id": "337","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-9, PRV-CIR-14, PRV-CIR-15, PRV-CIR-25, PRV-CIR-ESP-66, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-ESP-67, PRV-CIR-ESP-68, PRV-CIR-ESP-69"},
# {"nome": "CIRURGIA BUCO-MAXILO-FACIAL","id": "160","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "CIRURGIA CARDIOVASCULAR","id": "161","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-3, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-21, PRV-CIR-22, PRV-CIR-28, PRV-CIR-29, PRV-CIR-30, PRV-CIR-31, PRV-CIR-32, PRV-CIR-33, PRV-CIR-34, PRV-CIR-35, PRV-CIR-ESP-38, PRV-CIR-ESP-70, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA DE CABEÇA E PESCOÇO","id": "163","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-10, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-23, PRV-CIR-ESP-70, PRV-CIR-73, PRV-CIR-ESP-27"},
# {"nome": "ACUPUNTURA","id": "121","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "CIRURGIA DO APARELHO DIGESTIVO","id": "169","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA GERAL","id": "338","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-2, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-23, PRV-CIR-24, PRV-CIR-25, PRV-CIR-48, PRV-CIR-55, PRV-CIR-58, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA ONCOLÓGICA","id": "339","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-46, PRV-CIR-54"},
# {"nome": "CIRURGIA PEDIÁTRICA","id": "340","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-13, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-23, PRV-CIR-24, PRV-CIR-25, PRV-CIR-48, PRV-CIR-53, PRV-CIR-54, PRV-CIR-55, PRV-CIR-57, PRV-CIR-58, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-ESP-41"},
# {"nome": "CIRURGIA PLÁSTICA","id": "341","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-11, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-24, PRV-CIR-ESP-70, PRV-CIR-74, PRV-CIR-75"},
# {"nome": "CIRURGIA TORÁCICA","id": "342","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-8, PRV-CIR-14, PRV-CIR-15, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-21, PRV-CIR-22, PRV-CIR-53, PRV-CIR-54, PRV-CIR-55, PRV-CIR-ESP-56, PRV-CIR-57, PRV-CIR-58, PRV-CIR-59, PRV-CIR-60, PRV-CIR-61, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-62, PRV-CIR-63, PRV-CIR-64, PRV-CIR-ESP-65"},
# {"nome": "CIRURGIA VASCULAR","id": "343","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "CIRURGIÃO DENTISTA","id": "344","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-ODO-1, PRV-ODO-2, PRV-ODO-ESP-3"},
# {"nome": "CLÍNICA MÉDICA","id": "345","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-10, PRV-CLI-ESP-12, PRV-CLI-15"},
# {"nome": "COLOPROCTOLOGIA","id": "346","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-2, PRV-CIR-5, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-25, PRV-CIR-39, PRV-CIR-40, PRV-CIR-42, PRV-CIR-ESP-43, PRV-CIR-ESP-44, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-ESP-41"},
# {"nome": "ALERGIA E IMUNOLOGIA","id": "122","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "DERMATOLOGIA","id": "347","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-54, PRV-CLI-60"},
# {"nome": "ENDOCRINOLOGIA E METABOLOGIA","id": "348","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "ENDOSCOPIA","id": "349","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-ENDO-1, PRV-ENDO-2, PRV-ENDO-3"},
# {"nome": "GASTROENTEROLOGIA","id": "350","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-7, PRV-CLI-ESP-23, PRV-CLI-ESP-24, PRV-CLI-ESP-25, PRV-CLI-ESP-26, PRV-CLI-ESP-27, PRV-CLI-ESP-28, PRV-CLI-ESP-29, PRV-CLI-ESP-30, PRV-CLI-ESP-31, PRV-CLI-ESP-32"},
# {"nome": "GENÉTICA MÉDICA","id": "351","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "GERIATRIA","id": "352","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "GINECOLOGIA E OBSTETRÍCIA","id": "353","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-GO-ESP-6, PRV-GO-ESP-7, PRV-GO-8, PRV-GO-1, PRV-GO-2, PRV-GO-3, PRV-GO-4, PRV-GO-ESP-5, PRV-CIR-ESP-27"},
# {"nome": "HEMATOLOGIA E HEMOTERAPIA","id": "354","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-7, PRV-CLI-8, PRV-CLI-39, PRV-CLI-AVA-40"},
# {"nome": "HOMEOPATIA","id": "356","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "INFECTOLOGIA","id": "357","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-7, PRV-CLI-10"},
# {"nome": "ANESTESIOLOGIA","id": "123","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "MASTOLOGIA","id": "358","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-6, PRV-CIR-14, PRV-CIR-17, PRV-CIR-45, PRV-CIR-46, PRV-CIR-47, PRV-CIR-48, PRV-CIR-ESP-70"},
# {"nome": "MEDICINA DE EMERGÊNCIA","id": "359","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-9, PRV-CLI-10, PRV-CLI-11, PRV-CLI-13, PRV-CLI-15, PRV-CLI-56, PRV-CLI-62"},
# {"nome": "MEDICINA DE FAMÍLIA E COMUNIDADE","id": "360","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "MEDICINA DO TRABALHO","id": "361","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "MEDICINA DO TRÁFEGO","id": "362","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "MEDICINA ESPORTIVA","id": "363","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "MEDICINA FÍSICA E REABILITAÇÃO","id": "364","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "MEDICINA INTENSIVA","id": "365","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-9, PRV-CLI-10, PRV-CLI-11, PRV-CLI-ESP-12, PRV-CLI-13, PRV-CLI-15, PRV-CLI-56, PRV-CLI-62"},
# {"nome": "MEDICINA LEGAL E PERÍCIA MÉDICA","id": "366","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "MEDICINA NUCLEAR","id": "367","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "ANGIOLOGIA","id": "124","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-4, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-21, PRV-CIR-31, PRV-CIR-36, PRV-CIR-37, PRV-CIR-ESP-38, PRV-CIR-ESP-70, PRV-CIR-ESP-27"},
# {"nome": "MEDICINA PREVENTIVA SOCIAL","id": "368","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "NEFROLOGIA","id": "369","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-7, PRV-CLI-33, PRV-CLI-34, PRV-CLI-35, PRV-CLI-36, PRV-CLI-37, PRV-CLI-38"},
# {"nome": "NEUROCIRURGIA","id": "370","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-7, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-18, PRV-CIR-19, PRV-CIR-49, PRV-CIR-50, PRV-CIR-51, PRV-CIR-ESP-52, PRV-CIR-ESP-70"},
# {"nome": "NEUROLOGIA","id": "371","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-8, PRV-CLI-10, PRV-CLI-ESP-49, PRV-CLI-ESP-50, PRV-CLI-ESP-51, PRV-CLI-ESP-52, PRV-CLI-ESP-53, PRV-CLI-54"},
# {"nome": "NUTROLOGIA","id": "372","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-ESP-12"},
# {"nome": "OFTALMOLOGIA","id": "373","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-61"},
# {"nome": "ONCOLOGIA CLÍNICA","id": "374","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-RESID-1"},
# {"nome": "ORTOPEDIA E TRAUMATOLOGIA","id": "375","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-12, PRV-CIR-14, PRV-CIR-18, PRV-CIR-ESP-70, PRV-CIR-71, PRV-CIR-72, PRV-CIR-76, PRV-CIR-77, PRV-CIR-ESP-27"},
# {"nome": "OTORRINOLARINGOLOGIA","id": "376","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-OTO-1, PRV-OTO-2, PRV-OTO-3, PRV-OTO-4, PRV-OTO-5, PRV-OTO-6, PRV-OTO-7, PRV-OTO-8, PRV-OTO-9, PRV-OTO-10, PRV-OTO-11, PRV-OTO-12, PRV-OTO-13, PRV-OTO-14, PRV-OTO-AVA-15"},
# {"nome": "PATOLOGIA","id": "377","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-PAT-1, PRV-PAT-2, PRV-PAT-3, PRV-PAT-4, PRV-PAT-5, PRV-PAT-6, PRV-PAT-7"},
# {"nome": "CARDIOLOGIA","id": "125","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-13, PRV-CLI-14, PRV-CLI-15, PRV-CLI-16, PRV-CLI-22, PRV-CLI-ESP-63"},
# {"nome": "PATOLOGIA CLÍNICA / MEDICINA LABORATORIAL","id": "378","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "PEDIATRIA","id": "379","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-PED-1, PRV-PED-2, PRV-PED-AVA-3, PRV-PED-4, PRV-PED-6, PRV-PED-7, PRV-PED-8, PRV-PED-9, PRV-PED-10, PRV-PED-ESP-11, PRV-PED-12, PRV-PED-13, PRV-PED-14, PRV-PED-15, PRV-PED-16, PRV-PED-17, PRV-PED-18, PRV-CLI-AVA-40"},
# {"nome": "PNEUMOLOGIA","id": "380","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-7, PRV-CLI-8, PRV-CLI-9, PRV-CLI-11, PRV-CLI-42, PRV-CLI-43, PRV-CLI-ESP-47, PRV-CLI-ESP-41, PRV-CLI-44, PRV-CLI-45, PRV-CLI-ESP-46, PRV-CLI-ESP-48"},
# {"nome": "PSIQUIATRIA","id": "381","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-55"},
# {"nome": "RADIOLOGIA E DIAGNÓSTICO POR IMAGEM","id": "382","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "RADIOTERAPIA","id": "383","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-RAD-1, PRV-RAD-2, PRV-RAD-3, PRV-RAD-4, PRV-RAD-5, PRV-RAD-6, PRV-RAD-7, PRV-RAD-8"},
# {"nome": "REUMATOLOGIA","id": "384","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-57, PRV-CLI-58, PRV-CLI-59"},
# {"nome": "UROLOGIA","id": "385","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-9, PRV-CIR-14, PRV-CIR-15, PRV-CIR-25, PRV-CIR-ESP-66, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-ESP-67, PRV-CIR-ESP-68, PRV-CIR-ESP-69"},
# {"nome": "CIRURGIA BUCO-MAXILO-FACIAL","id": "165","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "CIRURGIA CARDIOVASCULAR","id": "166","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-3, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-21, PRV-CIR-22, PRV-CIR-28, PRV-CIR-29, PRV-CIR-30, PRV-CIR-31, PRV-CIR-32, PRV-CIR-33, PRV-CIR-34, PRV-CIR-35, PRV-CIR-ESP-38, PRV-CIR-ESP-70, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA DE CABEÇA E PESCOÇO","id": "168","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-10, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-23, PRV-CIR-ESP-70, PRV-CIR-73, PRV-CIR-ESP-27"},
# {"nome": "ACUPUNTURA","id": "137","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "CIRURGIA DO APARELHO DIGESTIVO","id": "179","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA GERAL","id": "433","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-2, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-23, PRV-CIR-24, PRV-CIR-25, PRV-CIR-48, PRV-CIR-55, PRV-CIR-58, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA ONCOLÓGICA","id": "434","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-46, PRV-CIR-54"},
# {"nome": "CIRURGIA PEDIÁTRICA","id": "435","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-13, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-23, PRV-CIR-24, PRV-CIR-25, PRV-CIR-48, PRV-CIR-53, PRV-CIR-54, PRV-CIR-55, PRV-CIR-57, PRV-CIR-58, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-ESP-41"},
# {"nome": "CIRURGIA PLÁSTICA","id": "436","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-11, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-24, PRV-CIR-ESP-70, PRV-CIR-74, PRV-CIR-75"},
# {"nome": "CIRURGIA TORÁCICA","id": "437","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-8, PRV-CIR-14, PRV-CIR-15, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-21, PRV-CIR-22, PRV-CIR-53, PRV-CIR-54, PRV-CIR-55, PRV-CIR-ESP-56, PRV-CIR-57, PRV-CIR-58, PRV-CIR-59, PRV-CIR-60, PRV-CIR-61, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-62, PRV-CIR-63, PRV-CIR-64, PRV-CIR-ESP-65"},
# {"nome": "CIRURGIA VASCULAR","id": "438","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "CIRURGIÃO DENTISTA","id": "439","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-ODO-1, PRV-ODO-2, PRV-ODO-ESP-3"},
# {"nome": "CLÍNICA MÉDICA","id": "440","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-10, PRV-CLI-ESP-12, PRV-CLI-15"},
# {"nome": "COLOPROCTOLOGIA","id": "441","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-2, PRV-CIR-5, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-25, PRV-CIR-39, PRV-CIR-40, PRV-CIR-42, PRV-CIR-ESP-43, PRV-CIR-ESP-44, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-ESP-41"},
# {"nome": "ALERGIA E IMUNOLOGIA","id": "138","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "DERMATOLOGIA","id": "442","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-54, PRV-CLI-60"},
# {"nome": "ENDOCRINOLOGIA E METABOLOGIA","id": "443","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "ENDOSCOPIA","id": "444","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-ENDO-1, PRV-ENDO-2, PRV-ENDO-3"},
# {"nome": "GASTROENTEROLOGIA","id": "445","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-7, PRV-CLI-ESP-23, PRV-CLI-ESP-24, PRV-CLI-ESP-25, PRV-CLI-ESP-26, PRV-CLI-ESP-27, PRV-CLI-ESP-28, PRV-CLI-ESP-29, PRV-CLI-ESP-30, PRV-CLI-ESP-31, PRV-CLI-ESP-32"},
# {"nome": "GENÉTICA MÉDICA","id": "446","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "GERIATRIA","id": "447","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "GINECOLOGIA E OBSTETRÍCIA","id": "448","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-GO-ESP-6, PRV-GO-ESP-7, PRV-GO-8, PRV-GO-1, PRV-GO-2, PRV-GO-3, PRV-GO-4, PRV-GO-ESP-5, PRV-CIR-ESP-27"},
# {"nome": "HEMATOLOGIA E HEMOTERAPIA","id": "449","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-7, PRV-CLI-8, PRV-CLI-39, PRV-CLI-AVA-40"},
# {"nome": "HOMEOPATIA","id": "450","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "INFECTOLOGIA","id": "451","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-7, PRV-CLI-10"},
# {"nome": "ANESTESIOLOGIA","id": "139","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "MASTOLOGIA","id": "452","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-6, PRV-CIR-14, PRV-CIR-17, PRV-CIR-45, PRV-CIR-46, PRV-CIR-47, PRV-CIR-48, PRV-CIR-ESP-70"},
# {"nome": "MEDICINA DE EMERGÊNCIA","id": "453","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-9, PRV-CLI-10, PRV-CLI-11, PRV-CLI-13, PRV-CLI-15, PRV-CLI-56, PRV-CLI-62"},
# {"nome": "MEDICINA DE FAMÍLIA E COMUNIDADE","id": "454","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "MEDICINA DO TRABALHO","id": "455","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "MEDICINA DO TRÁFEGO","id": "456","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "MEDICINA ESPORTIVA","id": "457","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "MEDICINA FÍSICA E REABILITAÇÃO","id": "458","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "MEDICINA INTENSIVA","id": "459","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-9, PRV-CLI-10, PRV-CLI-11, PRV-CLI-ESP-12, PRV-CLI-13, PRV-CLI-15, PRV-CLI-56, PRV-CLI-62"},
# {"nome": "MEDICINA LEGAL E PERÍCIA MÉDICA","id": "460","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "MEDICINA NUCLEAR","id": "461","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "ANGIOLOGIA","id": "140","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-4, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-21, PRV-CIR-31, PRV-CIR-36, PRV-CIR-37, PRV-CIR-ESP-38, PRV-CIR-ESP-70, PRV-CIR-ESP-27"},
# {"nome": "MEDICINA PREVENTIVA SOCIAL","id": "462","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "NEFROLOGIA","id": "463","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-7, PRV-CLI-33, PRV-CLI-34, PRV-CLI-35, PRV-CLI-36, PRV-CLI-37, PRV-CLI-38"},
# {"nome": "NEUROCIRURGIA","id": "464","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-7, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-18, PRV-CIR-19, PRV-CIR-49, PRV-CIR-50, PRV-CIR-51, PRV-CIR-ESP-52, PRV-CIR-ESP-70"},
# {"nome": "NEUROLOGIA","id": "465","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-8, PRV-CLI-10, PRV-CLI-ESP-49, PRV-CLI-ESP-50, PRV-CLI-ESP-51, PRV-CLI-ESP-52, PRV-CLI-ESP-53, PRV-CLI-54"},
# {"nome": "NUTROLOGIA","id": "466","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-ESP-12"},
# {"nome": "OFTALMOLOGIA","id": "467","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-61"},
# {"nome": "ONCOLOGIA CLÍNICA","id": "468","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-RESID-1"},
# {"nome": "ORTOPEDIA E TRAUMATOLOGIA","id": "469","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-12, PRV-CIR-14, PRV-CIR-18, PRV-CIR-ESP-70, PRV-CIR-71, PRV-CIR-72, PRV-CIR-76, PRV-CIR-77, PRV-CIR-ESP-27"},
# {"nome": "OTORRINOLARINGOLOGIA","id": "470","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-OTO-1, PRV-OTO-2, PRV-OTO-3, PRV-OTO-4, PRV-OTO-5, PRV-OTO-6, PRV-OTO-7, PRV-OTO-8, PRV-OTO-9, PRV-OTO-10, PRV-OTO-11, PRV-OTO-12, PRV-OTO-13, PRV-OTO-14, PRV-OTO-AVA-15"},
# {"nome": "PATOLOGIA","id": "471","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-PAT-1, PRV-PAT-2, PRV-PAT-3, PRV-PAT-4, PRV-PAT-5, PRV-PAT-6, PRV-PAT-7"},
# {"nome": "CARDIOLOGIA","id": "141","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-13, PRV-CLI-14, PRV-CLI-15, PRV-CLI-16, PRV-CLI-22, PRV-CLI-ESP-63"},
# {"nome": "PATOLOGIA CLÍNICA / MEDICINA LABORATORIAL","id": "472","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "PEDIATRIA","id": "473","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-PED-1, PRV-PED-2, PRV-PED-AVA-3, PRV-PED-4, PRV-PED-6, PRV-PED-7, PRV-PED-8, PRV-PED-9, PRV-PED-10, PRV-PED-ESP-11, PRV-PED-12, PRV-PED-13, PRV-PED-14, PRV-PED-15, PRV-PED-16, PRV-PED-17, PRV-PED-18, PRV-CLI-AVA-40"},
# {"nome": "PNEUMOLOGIA","id": "474","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-7, PRV-CLI-8, PRV-CLI-9, PRV-CLI-11, PRV-CLI-42, PRV-CLI-43, PRV-CLI-ESP-47, PRV-CLI-ESP-41, PRV-CLI-44, PRV-CLI-45, PRV-CLI-ESP-46, PRV-CLI-ESP-48"},
# {"nome": "PSIQUIATRIA","id": "475","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-55"},
# {"nome": "RADIOLOGIA E DIAGNÓSTICO POR IMAGEM","id": "476","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "RADIOTERAPIA","id": "477","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-RAD-1, PRV-RAD-2, PRV-RAD-3, PRV-RAD-4, PRV-RAD-5, PRV-RAD-6, PRV-RAD-7, PRV-RAD-8"},
# {"nome": "REUMATOLOGIA","id": "478","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-57, PRV-CLI-58, PRV-CLI-59"},
# {"nome": "UROLOGIA","id": "479","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-9, PRV-CIR-14, PRV-CIR-15, PRV-CIR-25, PRV-CIR-ESP-66, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-ESP-67, PRV-CIR-ESP-68, PRV-CIR-ESP-69"},
# {"nome": "CIRURGIA BUCO-MAXILO-FACIAL","id": "175","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "CIRURGIA CARDIOVASCULAR","id": "176","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-3, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-21, PRV-CIR-22, PRV-CIR-28, PRV-CIR-29, PRV-CIR-30, PRV-CIR-31, PRV-CIR-32, PRV-CIR-33, PRV-CIR-34, PRV-CIR-35, PRV-CIR-ESP-38, PRV-CIR-ESP-70, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA DE CABEÇA E PESCOÇO","id": "178","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-10, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-23, PRV-CIR-ESP-70, PRV-CIR-73, PRV-CIR-ESP-27"},
# {"nome": "ACUPUNTURA","id": "126","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "CIRURGIA DO APARELHO DIGESTIVO","id": "174","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA GERAL","id": "386","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-2, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-23, PRV-CIR-24, PRV-CIR-25, PRV-CIR-48, PRV-CIR-55, PRV-CIR-58, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA ONCOLÓGICA","id": "387","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-46, PRV-CIR-54"},
# {"nome": "CIRURGIA PEDIÁTRICA","id": "388","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-13, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-23, PRV-CIR-24, PRV-CIR-25, PRV-CIR-48, PRV-CIR-53, PRV-CIR-54, PRV-CIR-55, PRV-CIR-57, PRV-CIR-58, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-ESP-41"},
# {"nome": "CIRURGIA PLÁSTICA","id": "389","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-11, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-24, PRV-CIR-ESP-70, PRV-CIR-74, PRV-CIR-75"},
# {"nome": "CIRURGIA TORÁCICA","id": "390","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-8, PRV-CIR-14, PRV-CIR-15, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-21, PRV-CIR-22, PRV-CIR-53, PRV-CIR-54, PRV-CIR-55, PRV-CIR-ESP-56, PRV-CIR-57, PRV-CIR-58, PRV-CIR-59, PRV-CIR-60, PRV-CIR-61, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-62, PRV-CIR-63, PRV-CIR-64, PRV-CIR-ESP-65"},
# {"nome": "CIRURGIA VASCULAR","id": "391","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "CIRURGIÃO DENTISTA","id": "392","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-ODO-1, PRV-ODO-2, PRV-ODO-ESP-3"},
# {"nome": "CLÍNICA MÉDICA","id": "393","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-10, PRV-CLI-ESP-12, PRV-CLI-15"},
# {"nome": "COLOPROCTOLOGIA","id": "394","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-2, PRV-CIR-5, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-25, PRV-CIR-39, PRV-CIR-40, PRV-CIR-42, PRV-CIR-ESP-43, PRV-CIR-ESP-44, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-ESP-41"},
# {"nome": "ALERGIA E IMUNOLOGIA","id": "127","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "DERMATOLOGIA","id": "395","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-54, PRV-CLI-60"},
# {"nome": "ENDOCRINOLOGIA E METABOLOGIA","id": "396","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "ENDOSCOPIA","id": "397","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-ENDO-1, PRV-ENDO-2, PRV-ENDO-3"},
# {"nome": "GASTROENTEROLOGIA","id": "398","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-7, PRV-CLI-ESP-23, PRV-CLI-ESP-24, PRV-CLI-ESP-25, PRV-CLI-ESP-26, PRV-CLI-ESP-27, PRV-CLI-ESP-28, PRV-CLI-ESP-29, PRV-CLI-ESP-30, PRV-CLI-ESP-31, PRV-CLI-ESP-32"},
# {"nome": "GENÉTICA MÉDICA","id": "399","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "GERIATRIA","id": "400","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "GINECOLOGIA E OBSTETRÍCIA","id": "401","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-GO-ESP-6, PRV-GO-ESP-7, PRV-GO-8, PRV-GO-1, PRV-GO-2, PRV-GO-3, PRV-GO-4, PRV-GO-ESP-5, PRV-CIR-ESP-27"},
# {"nome": "HEMATOLOGIA E HEMOTERAPIA","id": "402","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-7, PRV-CLI-8, PRV-CLI-39, PRV-CLI-AVA-40"},
# {"nome": "HOMEOPATIA","id": "403","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "INFECTOLOGIA","id": "404","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-7, PRV-CLI-10"},
# {"nome": "ANESTESIOLOGIA","id": "128","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "MASTOLOGIA","id": "405","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-6, PRV-CIR-14, PRV-CIR-17, PRV-CIR-45, PRV-CIR-46, PRV-CIR-47, PRV-CIR-48, PRV-CIR-ESP-70"},
# {"nome": "MEDICINA DE EMERGÊNCIA","id": "406","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-9, PRV-CLI-10, PRV-CLI-11, PRV-CLI-13, PRV-CLI-15, PRV-CLI-56, PRV-CLI-62"},
# {"nome": "MEDICINA DE FAMÍLIA E COMUNIDADE","id": "407","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "MEDICINA DO TRABALHO","id": "408","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "MEDICINA DO TRÁFEGO","id": "409","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "MEDICINA ESPORTIVA","id": "410","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "MEDICINA FÍSICA E REABILITAÇÃO","id": "411","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "MEDICINA INTENSIVA","id": "412","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-9, PRV-CLI-10, PRV-CLI-11, PRV-CLI-ESP-12, PRV-CLI-13, PRV-CLI-15, PRV-CLI-56, PRV-CLI-62"},
# {"nome": "MEDICINA LEGAL E PERÍCIA MÉDICA","id": "413","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "MEDICINA NUCLEAR","id": "414","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "ANGIOLOGIA","id": "129","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-4, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-21, PRV-CIR-31, PRV-CIR-36, PRV-CIR-37, PRV-CIR-ESP-38, PRV-CIR-ESP-70, PRV-CIR-ESP-27"},
# {"nome": "MEDICINA PREVENTIVA SOCIAL","id": "415","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "NEFROLOGIA","id": "416","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-7, PRV-CLI-33, PRV-CLI-34, PRV-CLI-35, PRV-CLI-36, PRV-CLI-37, PRV-CLI-38"},
# {"nome": "NEUROCIRURGIA","id": "417","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-7, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-18, PRV-CIR-19, PRV-CIR-49, PRV-CIR-50, PRV-CIR-51, PRV-CIR-ESP-52, PRV-CIR-ESP-70"},
# {"nome": "NEUROLOGIA","id": "418","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-8, PRV-CLI-10, PRV-CLI-ESP-49, PRV-CLI-ESP-50, PRV-CLI-ESP-51, PRV-CLI-ESP-52, PRV-CLI-ESP-53, PRV-CLI-54"},
# {"nome": "NUTROLOGIA","id": "419","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-ESP-12"},
# {"nome": "OFTALMOLOGIA","id": "420","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-61"},
# {"nome": "ONCOLOGIA CLÍNICA","id": "421","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-RESID-1"},
# {"nome": "ORTOPEDIA E TRAUMATOLOGIA","id": "422","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-12, PRV-CIR-14, PRV-CIR-18, PRV-CIR-ESP-70, PRV-CIR-71, PRV-CIR-72, PRV-CIR-76, PRV-CIR-77, PRV-CIR-ESP-27"},
# {"nome": "OTORRINOLARINGOLOGIA","id": "423","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-OTO-1, PRV-OTO-2, PRV-OTO-3, PRV-OTO-4, PRV-OTO-5, PRV-OTO-6, PRV-OTO-7, PRV-OTO-8, PRV-OTO-9, PRV-OTO-10, PRV-OTO-11, PRV-OTO-12, PRV-OTO-13, PRV-OTO-14, PRV-OTO-AVA-15"},
# {"nome": "PATOLOGIA","id": "424","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-PAT-1, PRV-PAT-2, PRV-PAT-3, PRV-PAT-4, PRV-PAT-5, PRV-PAT-6, PRV-PAT-7"},
# {"nome": "CARDIOLOGIA","id": "130","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-13, PRV-CLI-14, PRV-CLI-15, PRV-CLI-16, PRV-CLI-22, PRV-CLI-ESP-63"},
# {"nome": "PATOLOGIA CLÍNICA / MEDICINA LABORATORIAL","id": "425","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "PEDIATRIA","id": "426","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-PED-1, PRV-PED-2, PRV-PED-AVA-3, PRV-PED-4, PRV-PED-6, PRV-PED-7, PRV-PED-8, PRV-PED-9, PRV-PED-10, PRV-PED-ESP-11, PRV-PED-12, PRV-PED-13, PRV-PED-14, PRV-PED-15, PRV-PED-16, PRV-PED-17, PRV-PED-18, PRV-CLI-AVA-40"},
# {"nome": "PNEUMOLOGIA","id": "427","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-7, PRV-CLI-8, PRV-CLI-9, PRV-CLI-11, PRV-CLI-42, PRV-CLI-43, PRV-CLI-ESP-47, PRV-CLI-ESP-41, PRV-CLI-44, PRV-CLI-45, PRV-CLI-ESP-46, PRV-CLI-ESP-48"},
# {"nome": "PSIQUIATRIA","id": "428","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-55"},
# {"nome": "RADIOLOGIA E DIAGNÓSTICO POR IMAGEM","id": "429","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "RADIOTERAPIA","id": "430","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-RAD-1, PRV-RAD-2, PRV-RAD-3, PRV-RAD-4, PRV-RAD-5, PRV-RAD-6, PRV-RAD-7, PRV-RAD-8"},
# {"nome": "REUMATOLOGIA","id": "431","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-57, PRV-CLI-58, PRV-CLI-59"},
# {"nome": "UROLOGIA","id": "432","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-9, PRV-CIR-14, PRV-CIR-15, PRV-CIR-25, PRV-CIR-ESP-66, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-ESP-67, PRV-CIR-ESP-68, PRV-CIR-ESP-69"},
# {"nome": "CIRURGIA BUCO-MAXILO-FACIAL","id": "170","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0"},
# {"nome": "CIRURGIA CARDIOVASCULAR","id": "171","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-3, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-21, PRV-CIR-22, PRV-CIR-28, PRV-CIR-29, PRV-CIR-30, PRV-CIR-31, PRV-CIR-32, PRV-CIR-33, PRV-CIR-34, PRV-CIR-35, PRV-CIR-ESP-38, PRV-CIR-ESP-70, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA DE CABEÇA E PESCOÇO","id": "173","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-10, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-23, PRV-CIR-ESP-70, PRV-CIR-73, PRV-CIR-ESP-27"},
#AJUSTE CIRURGIA DA MÃO
# {"nome": "CIRURGIA DA MÃO","id": "110","codCurso": "4","codModalidade": "4.1","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-12, PRV-CIR-14, PRV-CIR-18, PRV-CIR-ESP-70, PRV-CIR-71, PRV-CIR-72, PRV-CIR-76, PRV-CIR-77, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA DA MÃO","id": "118","codCurso": "4","codModalidade": "4.2","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-12, PRV-CIR-14, PRV-CIR-18, PRV-CIR-ESP-70, PRV-CIR-71, PRV-CIR-72, PRV-CIR-76, PRV-CIR-77, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA DA MÃO","id": "182","codCurso": "4","codModalidade": "4.7","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-12, PRV-CIR-14, PRV-CIR-18, PRV-CIR-ESP-70, PRV-CIR-71, PRV-CIR-72, PRV-CIR-76, PRV-CIR-77, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA DA MÃO","id": "162","codCurso": "4","codModalidade": "4.3","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-12, PRV-CIR-14, PRV-CIR-18, PRV-CIR-ESP-70, PRV-CIR-71, PRV-CIR-72, PRV-CIR-76, PRV-CIR-77, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA DA MÃO","id": "167","codCurso": "4","codModalidade": "4.4","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-12, PRV-CIR-14, PRV-CIR-18, PRV-CIR-ESP-70, PRV-CIR-71, PRV-CIR-72, PRV-CIR-76, PRV-CIR-77, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA DA MÃO","id": "177","codCurso": "4","codModalidade": "4.6","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-12, PRV-CIR-14, PRV-CIR-18, PRV-CIR-ESP-70, PRV-CIR-71, PRV-CIR-72, PRV-CIR-76, PRV-CIR-77, PRV-CIR-ESP-27"},
# {"nome": "CIRURGIA DA MÃO","id": "172","codCurso": "4","codModalidade": "4.5","codNivelEnsino": "N/A","codLocalOferta": "PRV-0, PRV-CIR-1, PRV-CIR-12, PRV-CIR-14, PRV-CIR-18, PRV-CIR-ESP-70, PRV-CIR-71, PRV-CIR-72, PRV-CIR-76, PRV-CIR-77, PRV-CIR-ESP-27"},
]
    
    # Executar cadastro
    cadastro = CRMOfertasCadastro()
    cadastro.processar_lista_ofertas(lista_ofertas)
    cadastro.gerar_relatorio()

if __name__ == "__main__":
    main()