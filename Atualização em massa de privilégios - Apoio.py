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
# {"nome": "ADRIANA FERNANDES URGELL","crm": "48123","cpf": "","codigo": "48123","curso": "406","atuacao": "APOIO TELEMEDICINA ","privilegios": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-9, PRV-CLI-10, PRV-CLI-11, PRV-CLI-13, PRV-CLI-15, PRV-CLI-56, PRV-CLI-62"},
# {"nome": "ALEXANDRE TERRA FONTES","crm": "32522","cpf": "","codigo": "32522","curso": "382","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "ALINE COLETTO","crm": "41286","cpf": "","codigo": "41286","curso": "204","atuacao": "APOIO CLINICO","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-10, PRV-CLI-ESP-12, PRV-CLI-15"},
# {"nome": "AMANDA DE FARIAS GABRIEL","crm": "29509","cpf": "2960876024","codigo": "29509","curso": "203","atuacao": "APOIO CLÍNICO","privilegios": "PRV-0, PRV-ODO-1, PRV-ODO-2, PRV-ODO-ESP-3"},
# {"nome": "AMANDA GIMENO DE NEGRI","crm": "42247","cpf": "","codigo": "42247","curso": "303","atuacao": "APOIO PESQUISA","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-7, PRV-CLI-ESP-23, PRV-CLI-ESP-24, PRV-CLI-ESP-25, PRV-CLI-ESP-26, PRV-CLI-ESP-27, PRV-CLI-ESP-28, PRV-CLI-ESP-29, PRV-CLI-ESP-30, PRV-CLI-ESP-31, PRV-CLI-ESP-32"},
# {"nome": "AMANDA TRONCO","crm": "46870","cpf": "","codigo": "46870","curso": "212","atuacao": "APOIO CLINICO","privilegios": "PRV-0, PRV-GO-ESP-6, PRV-GO-ESP-7, PRV-GO-8, PRV-GO-1, PRV-GO-2, PRV-GO-3, PRV-GO-4, PRV-GO-ESP-5, PRV-CIR-ESP-27"},
# {"nome": "ANA FLAVIA BARROS DA SILVA LIMA","crm": "20687","cpf": "","codigo": "20687","curso": "333","atuacao": "APOIO PESQUISA","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-55"},
# {"nome": "ANA LAURA FISCHER KUNZLER","crm": "42994","cpf": "","codigo": "42994","curso": "242","atuacao": "APOIO CLINICO","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-57, PRV-CLI-58, PRV-CLI-59"},
# {"nome": "ANA PAULA ASTARITA SANGOI","crm": "41231","cpf": "","codigo": "41231","curso": "382","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "ANNA KAROLINA PALHARES DE OLIVEIRA","crm": "42320","cpf": "6120055428","codigo": "42320","curso": "217","atuacao": "APOIO CLÍNICO ","privilegios": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-9, PRV-CLI-10, PRV-CLI-11, PRV-CLI-13, PRV-CLI-15, PRV-CLI-56, PRV-CLI-62"},
# {"nome": "ARIANE GIOVANAZ","crm": "42229","cpf": "","codigo": "42229","curso": "382","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "ARTUR GEHRES TRAPP","crm": "45867","cpf": "","codigo": "45867","curso": "479","atuacao": "APOIO ROBOTICA","privilegios": "PRV-0, PRV-CIR-1, PRV-CIR-9, PRV-CIR-14, PRV-CIR-15, PRV-CIR-25, PRV-CIR-ESP-66, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-ESP-67, PRV-CIR-ESP-68, PRV-CIR-ESP-69"},
# {"nome": "BARBARA LIMBERGER NEDEL","crm": "44139","cpf": "","codigo": "44139","curso": "382","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "BARBARA NUNES S RODRIGUES DO NASCIMENTO","crm": "44335","cpf": "","codigo": "44335","curso": "407","atuacao": "APOIO TELEMEDICINA","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "BETINA LEJDERMAN","crm": "38810","cpf": "","codigo": "38810","curso": "239","atuacao": "APOIO CLINICO","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-55"},
# {"nome": "BRUNA BRASIL DAL PUPO","crm": "45710","cpf": "","codigo": "45710","curso": "102","atuacao": "APOIO ANESTESIA","privilegios": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "BRUNA SESSIM GOMES","crm": "43716","cpf": "","codigo": "43716","curso": "102","atuacao": "APOIO ANESTESIA","privilegios": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "CAMILA BERGONSI DE FARIAS","crm": "46218","cpf": "","codigo": "46218","curso": "125","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-13, PRV-CLI-14, PRV-CLI-15, PRV-CLI-16, PRV-CLI-22, PRV-CLI-ESP-63"},
# {"nome": "CAMILA BRAGA VISCONTI","crm": "44108","cpf": "","codigo": "44108","curso": "382","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "CAMILA DE MOURA TURCHIELLO","crm": "48048","cpf": "","codigo": "48048","curso": "102","atuacao": "APOIO ANESTESIOLOGIA","privilegios": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "CAMILA VICENZI","crm": "44648","cpf": "","codigo": "44648","curso": "393","atuacao": "APOIO TELEMEDICINA","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-10, PRV-CLI-ESP-12, PRV-CLI-15"},
# {"nome": "CAREN MENEGHETTI GONÇALVES","crm": "35978","cpf": "","codigo": "35978","curso": "382","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "CARLOS AUGUSTO RODRIGUES VEO","crm": "88733","cpf": "","codigo": "88733","curso": "434","atuacao": "APOIO ROBOTICA","privilegios": "PRV-0, PRV-CIR-1, PRV-CIR-46, PRV-CIR-54"},
# {"nome": "CARLOS EDUARDO BASTIAN DA CUNHA","crm": "42969","cpf": "","codigo": "42969","curso": "233","atuacao": "APOIO CLINICO","privilegios": "PRV-0, PRV-CIR-1, PRV-CIR-12, PRV-CIR-14, PRV-CIR-18, PRV-CIR-ESP-70, PRV-CIR-71, PRV-CIR-72, PRV-CIR-76, PRV-CIR-77, PRV-CIR-ESP-27"},
# {"nome": "CAROLINA SPAT JAVORSKY","crm": "40897","cpf": "","codigo": "40897","curso": "102","atuacao": "APOIO ANESTESIA","privilegios": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "CAROLINE KIRSCHEN BRISTOT","crm": "44288","cpf": "","codigo": "44288","curso": "102","atuacao": "APOIO ANESTESIA","privilegios": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "CAROLINE LOCATELLI DA SILVA","crm": "46030","cpf": "","codigo": "46030","curso": "207","atuacao": "APOIO CLINICO","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "CASIELI NADIA ROHDE","crm": "38352","cpf": "","codigo": "38352","curso": "102","atuacao": "APOIO ANESTESIA","privilegios": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "CASSIA SOUZA DOS SANTOS","crm": "51776","cpf": "","codigo": "51776","curso": "407","atuacao": "APOIO TELEMEDICINA","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "CLAUDIO PEIXOTO CRISPI","crm": "52398816","cpf": "","codigo": "52398816","curso": "448","atuacao": "APOIO ROBOTICA","privilegios": "PRV-0, PRV-GO-ESP-6, PRV-GO-ESP-7, PRV-GO-8, PRV-GO-1, PRV-GO-2, PRV-GO-3, PRV-GO-4, PRV-GO-ESP-5, PRV-CIR-ESP-27"},
# {"nome": "CORA SALLES MARURI CORREA","crm": "41583","cpf": "","codigo": "41583","curso": "102","atuacao": "APOIO ANESTESIA","privilegios": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "CRISTINA MARTINO DA SILVA","crm": "34751","cpf": "","codigo": "34751","curso": "515","atuacao": "APOIO AREAS EXTERNAS","privilegios": "PRV-0, PRV-RESID-1"},
# {"nome": "DANIEL OLIVEIRA BONOMI","crm": "38115","cpf": "","codigo": "38115","curso": "437","atuacao": "APOIO ROBOTICA","privilegios": "PRV-0, PRV-CIR-1, PRV-CIR-8, PRV-CIR-14, PRV-CIR-15, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-21, PRV-CIR-22, PRV-CIR-53, PRV-CIR-54, PRV-CIR-55, PRV-CIR-ESP-56, PRV-CIR-57, PRV-CIR-58, PRV-CIR-59, PRV-CIR-60, PRV-CIR-61, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-62, PRV-CIR-63, PRV-CIR-64, PRV-CIR-ESP-65"},
# {"nome": "DANIEL WEISSBLUTH DE TOLEDO","crm": "46203","cpf": "","codigo": "46203","curso": "102","atuacao": "APOIO ANESTESIA","privilegios": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "EDUARDA SCHUTZ MARTINELLI","crm": "42645","cpf": "","codigo": "42645","curso": "102","atuacao": "APOIO ANESTESIA","privilegios": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "EDUARDO DA SILVA RODRIGUES","crm": "45815","cpf": "","codigo": "45815","curso": "233","atuacao": "APOIO CLINICO","privilegios": "PRV-0, PRV-CIR-1, PRV-CIR-12, PRV-CIR-14, PRV-CIR-18, PRV-CIR-ESP-70, PRV-CIR-71, PRV-CIR-72, PRV-CIR-76, PRV-CIR-77, PRV-CIR-ESP-27"},
# {"nome": "EDUARDO GATTI PIANCA","crm": "38620","cpf": "","codigo": "38620","curso": "125","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-13, PRV-CLI-14, PRV-CLI-15, PRV-CLI-16, PRV-CLI-22, PRV-CLI-ESP-63"},
# {"nome": "EMANUELE PELIZZARI","crm": "35023","cpf": "","codigo": "35023","curso": "353","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-0, PRV-GO-ESP-6, PRV-GO-ESP-7, PRV-GO-8, PRV-GO-1, PRV-GO-2, PRV-GO-3, PRV-GO-4, PRV-GO-ESP-5, PRV-CIR-ESP-27"},
# {"nome": "ENRICO MATTANA MULLER","crm": "34011","cpf": "","codigo": "34011","curso": "523","atuacao": "APOIO AREAS EXTERNAS","privilegios": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "FABIELE DE LIMA RIGHI","crm": "47165","cpf": "","codigo": "47165","curso": "105","atuacao": "APOIO CLINICO","privilegios": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-13, PRV-CLI-14, PRV-CLI-15, PRV-CLI-16, PRV-CLI-22, PRV-CLI-ESP-63"},
# {"nome": "FELIPE CORREA DA SILVA","crm": "44176","cpf": "","codigo": "44176","curso": "102","atuacao": "APOIO ANESTESIA","privilegios": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "FELIPE DE AZEVEDO DOSSIN","crm": "43662","cpf": "","codigo": "43662","curso": "382","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "FERNANDA CHAVES AMANTEA","crm": "49189","cpf": "3636387090","codigo": "49189","curso": "234","atuacao": "APOIO CLINICO","privilegios": "PRV-0, PRV-OTO-1, PRV-OTO-2, PRV-OTO-3, PRV-OTO-4, PRV-OTO-5, PRV-OTO-6, PRV-OTO-7, PRV-OTO-8, PRV-OTO-9, PRV-OTO-10, PRV-OTO-11, PRV-OTO-12, PRV-OTO-13, PRV-OTO-14, PRV-OTO-AVA-15"},
# {"nome": "FERNANDA SCHUH MARTINS","crm": "45344","cpf": "","codigo": "45344","curso": "229","atuacao": "APOIO CLINICO","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-8, PRV-CLI-10, PRV-CLI-ESP-49, PRV-CLI-ESP-50, PRV-CLI-ESP-51, PRV-CLI-ESP-52, PRV-CLI-ESP-53, PRV-CLI-54"},
# {"nome": "FERNANDO ERNESTO CRUZ FELIPPE","crm": "125873","cpf": "","codigo": "125873","curso": "434","atuacao": "APOIO ROBOTICA","privilegios": "PRV-0, PRV-CIR-1, PRV-CIR-46, PRV-CIR-54"},
# {"nome": "FERNANDO MEYER","crm": "13034","cpf": "","codigo": "13034","curso": "479","atuacao": "APOIO ROBOTICA","privilegios": "PRV-0, PRV-CIR-1, PRV-CIR-9, PRV-CIR-14, PRV-CIR-15, PRV-CIR-25, PRV-CIR-ESP-66, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-ESP-67, PRV-CIR-ESP-68, PRV-CIR-ESP-69"},
# {"nome": "FERNANDO MORAES DE MOURA","crm": "42718","cpf": "","codigo": "42718","curso": "232","atuacao": "APOIO CLINICO","privilegios": "PRV-0, PRV-RESID-1"},
# {"nome": "FILIPE RODRIGUES SILVEIRA","crm": "44175","cpf": "","codigo": "44175","curso": "407","atuacao": "APOIO TELEMEDICINA","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "FILIPE RODRIGUES VARGAS DO NASCIMENTO","crm": "48275","cpf": "","codigo": "48275","curso": "407","atuacao": "APOIO TELEMEDICINA","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "FRANCIELE FOUCHARD DE CONTO","crm": "48118","cpf": "","codigo": "48118","curso": "382","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "FRANCINE WURZIUS DE QUADROS","crm": "45468","cpf": "","codigo": "45468","curso": "229","atuacao": "APOIO CLINICO","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-8, PRV-CLI-10, PRV-CLI-ESP-49, PRV-CLI-ESP-50, PRV-CLI-ESP-51, PRV-CLI-ESP-52, PRV-CLI-ESP-53, PRV-CLI-54"},
# {"nome": "GABRIELA ARAUJO DUARTE","crm": "42935","cpf": "","codigo": "42935","curso": "382","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "GABRIELA PEREIRA DE MOURA","crm": "49680","cpf": "3612222031","codigo": "49680","curso": "212","atuacao": "APOIO CLINICO","privilegios": "PRV-0, PRV-GO-ESP-6, PRV-GO-ESP-7, PRV-GO-8, PRV-GO-1, PRV-GO-2, PRV-GO-3, PRV-GO-4, PRV-GO-ESP-5, PRV-CIR-ESP-27"},
# {"nome": "GABRIELA TORTATO","crm": "38222","cpf": "","codigo": "38222","curso": "105","atuacao": "APOIO CLINICO","privilegios": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-13, PRV-CLI-14, PRV-CLI-15, PRV-CLI-16, PRV-CLI-22, PRV-CLI-ESP-63"},
# {"nome": "GABRIELLE LIMA PINTO","crm": "40621","cpf": "","codigo": "40621","curso": "146","atuacao": "APOIO AREAS EXTERNAS","privilegios": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-13, PRV-CLI-14, PRV-CLI-15, PRV-CLI-16, PRV-CLI-22, PRV-CLI-ESP-63"},
# {"nome": "GIORGIA LIONCO PELLINI","crm": "44594","cpf": "","codigo": "44594","curso": "239","atuacao": "APOIO CLINICO","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-55"},
# {"nome": "GIULIA BEVILACQUA SCHMITZ","crm": "43008","cpf": "","codigo": "43008","curso": "146","atuacao": "APOIO AREAS EXTERNAS","privilegios": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-13, PRV-CLI-14, PRV-CLI-15, PRV-CLI-16, PRV-CLI-22, PRV-CLI-ESP-63"},
# {"nome": "GIULIANA BEDUSCHI","crm": "44112","cpf": "","codigo": "44112","curso": "234","atuacao": "APOIO CLINICO","privilegios": "PRV-0, PRV-OTO-1, PRV-OTO-2, PRV-OTO-3, PRV-OTO-4, PRV-OTO-5, PRV-OTO-6, PRV-OTO-7, PRV-OTO-8, PRV-OTO-9, PRV-OTO-10, PRV-OTO-11, PRV-OTO-12, PRV-OTO-13, PRV-OTO-14, PRV-OTO-AVA-15"},
# {"nome": "GRAZIELLA MORAES MACHADO","crm": "35662","cpf": "","codigo": "35662","curso": "407","atuacao": "APOIO TELEMEDICINA","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "GUILHERME HENRIQUE MULLER","crm": "45833","cpf": "","codigo": "45833","curso": "125","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-13, PRV-CLI-14, PRV-CLI-15, PRV-CLI-16, PRV-CLI-22, PRV-CLI-ESP-63"},
# {"nome": "GUILHERME MOIMAZ","crm": "35617","cpf": "","codigo": "35617","curso": "489","atuacao": "APOIO AREAS EXTERNAS","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-54, PRV-CLI-60"},
# {"nome": "GUILHERME STUKER","crm": "43786","cpf": "","codigo": "43786","curso": "382","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "GUNNAR FREDERSON KUSSLER","crm": "43520","cpf": "","codigo": "43520","curso": "227","atuacao": "APOIO CLINICO","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-7, PRV-CLI-33, PRV-CLI-34, PRV-CLI-35, PRV-CLI-36, PRV-CLI-37, PRV-CLI-38"},
# {"nome": "HELENA CARVALHO MALDONADO","crm": "49687","cpf": "","codigo": "49687","curso": "102","atuacao": "APOIO ANESTESIOLOGIA","privilegios": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "HENRIQUE PAVAN","crm": "43904","cpf": "","codigo": "43904","curso": "382","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "JACIRA DAL PRA","crm": "8090","cpf": "","codigo": "8090","curso": "239","atuacao": "APOIO CLINICO","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-55"},
# {"nome": "JACKSON DE AZEVEDO JACUNDA FILHO","crm": "12994","cpf": "","codigo": "12994","curso": "204","atuacao": "APOIO CLINICO","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-10, PRV-CLI-ESP-12, PRV-CLI-15"},
# {"nome": "JESSICA JOHN TONIN","crm": "44625","cpf": "","codigo": "44625","curso": "487","atuacao": "APOIO AREAS EXTERNAS","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-10, PRV-CLI-ESP-12, PRV-CLI-15"},
# {"nome": "JONATAS FAVERO PRIETTO DOS SANTOS","crm": "42647","cpf": "3073498028","codigo": "42647","curso": "240","atuacao": "APOIO CLINICO","privilegios": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "JULIA KOWACS BUTZKE","crm": "48883","cpf": "","codigo": "48883","curso": "212","atuacao": "APOIO CLINICO","privilegios": "PRV-0, PRV-GO-ESP-6, PRV-GO-ESP-7, PRV-GO-8, PRV-GO-1, PRV-GO-2, PRV-GO-3, PRV-GO-4, PRV-GO-ESP-5, PRV-CIR-ESP-27"},
# {"nome": "JULIANA ROCHA BENEDETTI","crm": "39948","cpf": "","codigo": "39948","curso": "102","atuacao": "APOIO ANESTESIA","privilegios": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "JULIANO PEIXOTO BASTOS","crm": "41211","cpf": "","codigo": "41211","curso": "298","atuacao": "APOIO PSIQUIATRIA","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-10, PRV-CLI-ESP-12, PRV-CLI-15"},
# {"nome": "JULIO CEZAR GONÇALVES CORDEIRO DOS SANTO","crm": "46657","cpf": "","codigo": "46657","curso": "309","atuacao": "APOIO PSIQUIATRIA","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-7, PRV-CLI-10"},
# {"nome": "KARINA PEREIRA DA CRUZ","crm": "40782","cpf": "","codigo": "40782","curso": "234","atuacao": "APOIO CLINICO","privilegios": "PRV-0, PRV-OTO-1, PRV-OTO-2, PRV-OTO-3, PRV-OTO-4, PRV-OTO-5, PRV-OTO-6, PRV-OTO-7, PRV-OTO-8, PRV-OTO-9, PRV-OTO-10, PRV-OTO-11, PRV-OTO-12, PRV-OTO-13, PRV-OTO-14, PRV-OTO-AVA-15"},
# {"nome": "KASSIA MERCHIORATTO","crm": "43824","cpf": "","codigo": "43824","curso": "353","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-0, PRV-GO-ESP-6, PRV-GO-ESP-7, PRV-GO-8, PRV-GO-1, PRV-GO-2, PRV-GO-3, PRV-GO-4, PRV-GO-ESP-5, PRV-CIR-ESP-27"},
# {"nome": "LAURA AFANADOR PINEROS VAGHETTI","crm": "38175","cpf": "","codigo": "38175","curso": "407","atuacao": "APOIO TELEMEDICINA","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "LIVIA GORGEN MORSCH","crm": "43682","cpf": "","codigo": "43682","curso": "234","atuacao": "APOIO CLINICO","privilegios": "PRV-0, PRV-OTO-1, PRV-OTO-2, PRV-OTO-3, PRV-OTO-4, PRV-OTO-5, PRV-OTO-6, PRV-OTO-7, PRV-OTO-8, PRV-OTO-9, PRV-OTO-10, PRV-OTO-11, PRV-OTO-12, PRV-OTO-13, PRV-OTO-14, PRV-OTO-AVA-15"},
# {"nome": "LOURENÇO FLECK GOMES CARNEIRO","crm": "48929","cpf": "","codigo": "48929","curso": "102","atuacao": "APOIO ANESTESIOLOGIA","privilegios": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "LUANA MARINHO GONÇALVES","crm": "35762","cpf": "","codigo": "35762","curso": "240","atuacao": "APOIO CLINICO","privilegios": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "LUCAS GRACA ARANHA DE OLIVEIRA COUTO","crm": "35139","cpf": "","codigo": "35139","curso": "479","atuacao": "APOIO ROBOTICA","privilegios": "PRV-0, PRV-CIR-1, PRV-CIR-9, PRV-CIR-14, PRV-CIR-15, PRV-CIR-25, PRV-CIR-ESP-66, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-ESP-67, PRV-CIR-ESP-68, PRV-CIR-ESP-69"},
# {"nome": "LUCAS SAMUEL PERINAZZO PAUVELS","crm": "44649","cpf": "","codigo": "44649","curso": "489","atuacao": "APOIO AREAS EXTERNAS","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-54, PRV-CLI-60"},
# {"nome": "LUCIANA OTERO FELIX","crm": "41430","cpf": "","codigo": "41430","curso": "393","atuacao": "APOIO TELEMEDICINA","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-10, PRV-CLI-ESP-12, PRV-CLI-15"},
# {"nome": "LUCIANO GIORDANI","crm": "44869","cpf": "","codigo": "44869","curso": "125","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-13, PRV-CLI-14, PRV-CLI-15, PRV-CLI-16, PRV-CLI-22, PRV-CLI-ESP-63"},
# {"nome": "LUIS FELIPE CARISSIMI SCHMIDT","crm": "33635","cpf": "","codigo": "33635","curso": "515","atuacao": "APOIO AREAS EXTERNAS","privilegios": "PRV-0, PRV-RESID-1"},
# {"nome": "LUIS GUSTAVO CAPOCHIN ROMAGNOLO","crm": "116858","cpf": "","codigo": "116858","curso": "441","atuacao": "APOIO ROBOTICA","privilegios": "PRV-0, PRV-CIR-1, PRV-CIR-2, PRV-CIR-5, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-25, PRV-CIR-39, PRV-CIR-40, PRV-CIR-42, PRV-CIR-ESP-43, PRV-CIR-ESP-44, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-ESP-41"},
# {"nome": "LUIZ EDUARDO DE CASTILHOS FERREIRA","crm": "44109","cpf": "","codigo": "44109","curso": "102","atuacao": "APOIO ANESTESIA","privilegios": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "LUIZA COSTA SILVEIRA MARTINS","crm": "51279","cpf": "3958355005","codigo": "51279","curso": "102","atuacao": "APOIO ANESTESIOLOGIA ","privilegios": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "LUIZA FERREIRA VAN DER SAND","crm": "46217","cpf": "","codigo": "46217","curso": "105","atuacao": "APOIO CLINICO","privilegios": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-13, PRV-CLI-14, PRV-CLI-15, PRV-CLI-16, PRV-CLI-22, PRV-CLI-ESP-63"},
# {"nome": "MAHIRA DE OLIVEIRA LOPES DA ROSA","crm": "39974","cpf": "","codigo": "39974","curso": "232","atuacao": "APOIO CLINICO","privilegios": "PRV-0, PRV-RESID-1"},
# {"nome": "MARCEL DE ALMEIDA DORNELLES","crm": "35913","cpf": "","codigo": "35913","curso": "102","atuacao": "APOIO ANESTESIA","privilegios": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "MARCELO CEZAR MAFFI","crm": "47146","cpf": "","codigo": "47146","curso": "102","atuacao": "APOIO ANESTESIA","privilegios": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "MARCIO OLIVEIRA LUCAS","crm": "52599780","cpf": "","codigo": "52599780","curso": "437","atuacao": "APOIO ROBOTICA","privilegios": "PRV-0, PRV-CIR-1, PRV-CIR-8, PRV-CIR-14, PRV-CIR-15, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-21, PRV-CIR-22, PRV-CIR-53, PRV-CIR-54, PRV-CIR-55, PRV-CIR-ESP-56, PRV-CIR-57, PRV-CIR-58, PRV-CIR-59, PRV-CIR-60, PRV-CIR-61, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-62, PRV-CIR-63, PRV-CIR-64, PRV-CIR-ESP-65"},
# {"nome": "MARCO AURELIO CASTELLANO DE ALMEIDA","crm": "23203","cpf": "","codigo": "23203","curso": "476","atuacao": "APOIO ROBOTICA","privilegios": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "MARCOS BELOTTO DE OLIVEIRA","crm": "126757","cpf": "","codigo": "126757","curso": "179","atuacao": "APOIO ROBOTICA","privilegios": "PRV-0, PRV-CIR-ESP-27"},
# {"nome": "MARCOS VINICIUS ARAUJO DENADAI","crm": "87508","cpf": "","codigo": "87508","curso": "434","atuacao": "APOIO ROBOTICA","privilegios": "PRV-0, PRV-CIR-1, PRV-CIR-46, PRV-CIR-54"},
# {"nome": "MARIA EDUARDA CORTE GRIPA","crm": "51772","cpf": "","codigo": "51772","curso": "393","atuacao": "APOIO TELEMEDICINA","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-10, PRV-CLI-ESP-12, PRV-CLI-15"},
# {"nome": "MARIANA ALMUDI SOUZA","crm": "44171","cpf": "","codigo": "44171","curso": "229","atuacao": "APOIO CLINICO","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-8, PRV-CLI-10, PRV-CLI-ESP-49, PRV-CLI-ESP-50, PRV-CLI-ESP-51, PRV-CLI-ESP-52, PRV-CLI-ESP-53, PRV-CLI-54"},
# {"nome": "MARIANA TERRAZAS KOTZ MULLER","crm": "37519","cpf": "","codigo": "37519","curso": "240","atuacao": "APOIO CLINICO","privilegios": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "MARILIA VOGES DE SOUZA","crm": "37973","cpf": "","codigo": "37973","curso": "242","atuacao": "APOIO CLINICO","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-57, PRV-CLI-58, PRV-CLI-59"},
# {"nome": "MARTA ISABEL CARUCCIO HUBNER","crm": "30848","cpf": "","codigo": "30848","curso": "382","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "MATEUS BORIN","crm": "49363","cpf": "2978919019","codigo": "49363","curso": "102","atuacao": "APOIO ANESTESIOLOGIA","privilegios": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "MATEUS SAMUEL TONETTO","crm": "32039","cpf": "","codigo": "32039","curso": "382","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "MATHEUS SPORLEDER BORTOLUCI","crm": "38873","cpf": "","codigo": "38873","curso": "123","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "MAXIMILIANO CADAMURO NETO","crm": "117568","cpf": "","codigo": "117568","curso": "434","atuacao": "APOIO ROBOTICA","privilegios": "PRV-0, PRV-CIR-1, PRV-CIR-46, PRV-CIR-54"},
# {"nome": "MIRIAN COHEN","crm": "32815","cpf": "","codigo": "32815","curso": "333","atuacao": "APOIO PSIQUIATRIA","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-55"},
# {"nome": "NATALIA GUERRA DE OLIVEIRA","crm": "43923","cpf": "2323522086","codigo": "43923","curso": "232","atuacao": "APOIO CLINICO","privilegios": "PRV-0, PRV-RESID-1"},
# {"nome": "NATHALIA PALUDO","crm": "45866","cpf": "","codigo": "45866","curso": "102","atuacao": "APOIO ANESTESIA","privilegios": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "PAOLA STEFANIA BOHRER RABAIOLI","crm": "40702","cpf": "","codigo": "40702","curso": "146","atuacao": "APOIO CLINICO para áreas externas","privilegios": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-13, PRV-CLI-14, PRV-CLI-15, PRV-CLI-16, PRV-CLI-22, PRV-CLI-ESP-63"},
# {"nome": "PATRÍCIA YURI NOGUCHI","crm": "45658","cpf": "34084200840","codigo": "45658","curso": "382","atuacao": "APOIO RADIOLOGIA ","privilegios": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "PAULA BLAYA ROCHA","crm": "46300","cpf": "","codigo": "46300","curso": "239","atuacao": "APOIO CLINICO PARA APOIO PSIQUIATRIA","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-55"},
# {"nome": "PAULO AMORIM DA SILVEIRA","crm": "41791","cpf": "","codigo": "41791","curso": "382","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "PEDRO NABUCO DE ARAUJO","crm": "104388","cpf": "","codigo": "104388","curso": "437","atuacao": "APOIO ROBOTICA","privilegios": "PRV-0, PRV-CIR-1, PRV-CIR-8, PRV-CIR-14, PRV-CIR-15, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-21, PRV-CIR-22, PRV-CIR-53, PRV-CIR-54, PRV-CIR-55, PRV-CIR-ESP-56, PRV-CIR-57, PRV-CIR-58, PRV-CIR-59, PRV-CIR-60, PRV-CIR-61, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27, PRV-CIR-62, PRV-CIR-63, PRV-CIR-64, PRV-CIR-ESP-65"},
# {"nome": "PEDRO TOFANI SANT ANNA","crm": "44545","cpf": "","codigo": "44545","curso": "232","atuacao": "APOIO CLINICO","privilegios": "PRV-0, PRV-RESID-1"},
# {"nome": "PRISCILA SILVA","crm": "41570","cpf": "","codigo": "41570","curso": "232","atuacao": "APOIO CLINICO","privilegios": "PRV-0, PRV-RESID-1"},
# {"nome": "PRISCILLA MARTINELLI KREMER","crm": "36189","cpf": "","codigo": "36189","curso": "123","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "RAFAEL CORADIN","crm": "41989","cpf": "","codigo": "41989","curso": "525","atuacao": "APOIO AREAS EXTERNAS","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-57, PRV-CLI-58, PRV-CLI-59"},
# {"nome": "RAFAEL CORREA CACERES","crm": "43669","cpf": "","codigo": "43669","curso": "146","atuacao": "APOIO AREAS EXTERNAS","privilegios": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-13, PRV-CLI-14, PRV-CLI-15, PRV-CLI-16, PRV-CLI-22, PRV-CLI-ESP-63"},
# {"nome": "RANGEL MENEGATTI","crm": "47437","cpf": "2496049064","codigo": "47437","curso": "233","atuacao": "APOIO CLÍNICO","privilegios": "PRV-0, PRV-CIR-1, PRV-CIR-12, PRV-CIR-14, PRV-CIR-18, PRV-CIR-ESP-70, PRV-CIR-71, PRV-CIR-72, PRV-CIR-76, PRV-CIR-77, PRV-CIR-ESP-27"},
# {"nome": "RAQUEL BONFA","crm": "33878","cpf": "","codigo": "33878","curso": "489","atuacao": "APOIO AREAS EXTERNAS","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-54, PRV-CLI-60"},
# {"nome": "RENAN BEZERRA LIRA","crm": "131692","cpf": "","codigo": "131692","curso": "178","atuacao": "APOIO ROBOTICA","privilegios": "PRV-0, PRV-CIR-1, PRV-CIR-10, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-23, PRV-CIR-ESP-70, PRV-CIR-73, PRV-CIR-ESP-27"},
# {"nome": "RENAN REIS CALDAS","crm": "46615","cpf": "","codigo": "46615","curso": "382","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "RENATA ELISE TONOLI","crm": "29059","cpf": "","codigo": "29059","curso": "489","atuacao": "APOIO AREAS EXTERNAS","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-54, PRV-CLI-60"},
# {"nome": "RENATO CALCAGNOTTO","crm": "38509","cpf": "","codigo": "38509","curso": "125","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-13, PRV-CLI-14, PRV-CLI-15, PRV-CLI-16, PRV-CLI-22, PRV-CLI-ESP-63"},
# {"nome": "RENATO JOSE KIST DE MELLO","crm": "35663","cpf": "","codigo": "35663","curso": "240","atuacao": "APOIO CLINICO","privilegios": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "RICARDO CASTILHOS BARCELLOS DE MENEZES","crm": "42694","cpf": "","codigo": "42694","curso": "213","atuacao": "APOIO CLINICO","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-7, PRV-CLI-8, PRV-CLI-39, PRV-CLI-AVA-40"},
# {"nome": "RICARDO DOS REIS","crm": "160128","cpf": "","codigo": "160128","curso": "448","atuacao": "APOIO ROBOTICA","privilegios": "PRV-0, PRV-GO-ESP-6, PRV-GO-ESP-7, PRV-GO-8, PRV-GO-1, PRV-GO-2, PRV-GO-3, PRV-GO-4, PRV-GO-ESP-5, PRV-CIR-ESP-27"},
# {"nome": "RODRIGO HOFFMEISTER","crm": "19754","cpf": "","codigo": "19754","curso": "523","atuacao": "APOIO AREAS EXTERNAS","privilegios": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "RODRIGO NIGRI DE OLIVEIRA","crm": "40158","cpf": "","codigo": "40158","curso": "102","atuacao": "APOIO ANESTESIA","privilegios": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "ROGERS CAMARGO MARIANO DA SILVA","crm": "82508","cpf": "","codigo": "82508","curso": "448","atuacao": "APOIO ROBOTICA","privilegios": "PRV-0, PRV-GO-ESP-6, PRV-GO-ESP-7, PRV-GO-8, PRV-GO-1, PRV-GO-2, PRV-GO-3, PRV-GO-4, PRV-GO-ESP-5, PRV-CIR-ESP-27"},
# {"nome": "ROMMEL FABRICIO PEREIRA DA SILVA","crm": "38224","cpf": "","codigo": "38224","curso": "232","atuacao": "APOIO CLINICO","privilegios": "PRV-0, PRV-RESID-1"},
# {"nome": "SABINE MOSELE GUIDI","crm": "47819","cpf": "","codigo": "47819","curso": "102","atuacao": "APOIO ANESTESIA","privilegios": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "SAMANTA DAIANA DE ROSSI","crm": "38556","cpf": "","codigo": "38556","curso": "489","atuacao": "APOIO AREAS EXTERNAS","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-1, PRV-CLI-54, PRV-CLI-60"},
# {"nome": "SARAH DE SOUZA GIACOBBO CORADIN","crm": "40216","cpf": "","codigo": "40216","curso": "146","atuacao": "APOIO AREAS EXTERNAS","privilegios": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-13, PRV-CLI-14, PRV-CLI-15, PRV-CLI-16, PRV-CLI-22, PRV-CLI-ESP-63"},
# {"nome": "TAIS BELLADONA CARDOSO","crm": "35574","cpf": "","codigo": "35574","curso": "515","atuacao": "APOIO AREAS EXTERNAS","privilegios": "PRV-0, PRV-RESID-1"},
# {"nome": "TAISE LEITEMPERGER BERTAZZO","crm": "46128","cpf": "","codigo": "46128","curso": "234","atuacao": "APOIO CLINICO","privilegios": "PRV-0, PRV-OTO-1, PRV-OTO-2, PRV-OTO-3, PRV-OTO-4, PRV-OTO-5, PRV-OTO-6, PRV-OTO-7, PRV-OTO-8, PRV-OTO-9, PRV-OTO-10, PRV-OTO-11, PRV-OTO-12, PRV-OTO-13, PRV-OTO-14, PRV-OTO-AVA-15"},
# {"nome": "TATIANE APARECIDA FERREIRA","crm": "54230","cpf": "","codigo": "54230","curso": "407","atuacao": "APOIO TELEMEDICINA","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "TATIANE MORGANA DA SILVA","crm": "43167","cpf": "6418361989","codigo": "43167","curso": "512","atuacao": "APOIO AREAS EXTERNAS","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-8, PRV-CLI-10, PRV-CLI-ESP-49, PRV-CLI-ESP-50, PRV-CLI-ESP-51, PRV-CLI-ESP-52, PRV-CLI-ESP-53, PRV-CLI-54"},
# {"nome": "THAIS MARIEL ANDARA BEUREN","crm": "41473","cpf": "","codigo": "41473","curso": "105","atuacao": "APOIO CLINICO","privilegios": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-13, PRV-CLI-14, PRV-CLI-15, PRV-CLI-16, PRV-CLI-22, PRV-CLI-ESP-63"},
# {"nome": "THIAGO LUCAS BASTOS DE MELO MOSZKOWICZ","crm": "41060","cpf": "","codigo": "41060","curso": "386","atuacao": "APOIO TELEMEDICINA","privilegios": "PRV-0, PRV-CIR-1, PRV-CIR-2, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-23, PRV-CIR-24, PRV-CIR-25, PRV-CIR-48, PRV-CIR-55, PRV-CIR-58, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27"},
# {"nome": "TIAGO ELIAS HEINEN","crm": "44070","cpf": "","codigo": "44070","curso": "232","atuacao": "APOIO CLINICO","privilegios": "PRV-0, PRV-RESID-1"},
# {"nome": "VANESSA FRAGA CARPES","crm": "31016","cpf": "","codigo": "31016","curso": "353","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-0, PRV-GO-ESP-6, PRV-GO-ESP-7, PRV-GO-8, PRV-GO-1, PRV-GO-2, PRV-GO-3, PRV-GO-4, PRV-GO-ESP-5, PRV-CIR-ESP-27"},
# {"nome": "VICTOR MASCARENHAS AZEVEDO","crm": "34489","cpf": "","codigo": "34489","curso": "146","atuacao": "APOIO AREAS EXTERNAS","privilegios": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-13, PRV-CLI-14, PRV-CLI-15, PRV-CLI-16, PRV-CLI-22, PRV-CLI-ESP-63"},
# {"nome": "VICTORIA ARMENDARIS EL HALAL","crm": "47985","cpf": "","codigo": "47985","curso": "393","atuacao": "APOIO TELEMEDICINA","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-10, PRV-CLI-ESP-12, PRV-CLI-15"},
# {"nome": "VICTORIA SCHMIDT RAMOS","crm": "43231","cpf": "","codigo": "43231","curso": "125","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-13, PRV-CLI-14, PRV-CLI-15, PRV-CLI-16, PRV-CLI-22, PRV-CLI-ESP-63"},
# {"nome": "VICTORIA SILVEIRA DE CARVALHO","crm": "40808","cpf": "","codigo": "40808","curso": "525","atuacao": "APOIO AREAS EXTERNAS","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-4, PRV-CLI-1, PRV-CLI-57, PRV-CLI-58, PRV-CLI-59"},
# {"nome": "VINICIUS LEITE GONZALEZ","crm": "33962","cpf": "","codigo": "33962","curso": "146","atuacao": "APOIO AREAS EXTERNAS","privilegios": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-13, PRV-CLI-14, PRV-CLI-15, PRV-CLI-16, PRV-CLI-22, PRV-CLI-ESP-63"},
# {"nome": "VIRGINIA DE CARLI DE MOURA","crm": "45915","cpf": "","codigo": "45915","curso": "102","atuacao": "APOIO ANESTESIA","privilegios": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "VITOR DA AGOSTIM CANCELIER","crm": "47874","cpf": "","codigo": "47874","curso": "102","atuacao": "APOIO ANESTESIA","privilegios": "PRV-0, PRV-ANE-1, PRV-ANE-2, PRV-ANE-3, PRV-ANE-4, PRV-ANE-5, PRV-ANE-6, PRV-ANE-7, PRV-ANE-8, PRV-ANE-9, PRV-ANE-10, PRV-ANE-11, PRV-ANE-12, PRV-ANE-13, PRV-ANE-ESP-14, PRV-ANE-15, PRV-ANE-ESP-16, PRV-ANE-ESP-17, PRV-ANE-ESP-18, PRV-ANE-ESP-19"},
# {"nome": "VITOR RIBAS PEREIRA","crm": "49548","cpf": "3420624093","codigo": "49548","curso": "382","atuacao": "APOIO RADIOLOGIA ","privilegios": "PRV-0, PRV-RADL-1, PRV-RADL-2, PRV-RADL-3, PRV-RADL-4, PRV-RADL-5, PRV-RADL-6, PRV-RADL-7, PRV-RADL-8"},
# {"nome": "VIVIAN COLLARES VANASSI","crm": "42353","cpf": "","codigo": "42353","curso": "407","atuacao": "APOIO TELEMEDICINA","privilegios": "PRV-CLI-2, PRV-0, PRV-CLI-1"},
# {"nome": "WORENS LUIZ PEREIRA CAVALINI","crm": "46544","cpf": "","codigo": "46544","curso": "125","atuacao": "APOIO RADIOLOGIA","privilegios": "PRV-CLI-2, PRV-CLI-AVA-3, PRV-0, PRV-CLI-4, PRV-CLI-5, PRV-CLI-1, PRV-CLI-6, PRV-CLI-7, PRV-CLI-8, PRV-CLI-13, PRV-CLI-14, PRV-CLI-15, PRV-CLI-16, PRV-CLI-22, PRV-CLI-ESP-63"},
# {"nome": "YURI THOME MACHADO PETRILLO","crm": "45668","cpf": "","codigo": "45668","curso": "197","atuacao": "APOIO CLINICO","privilegios": "PRV-0, PRV-CIR-1, PRV-CIR-2, PRV-CIR-14, PRV-CIR-15, PRV-CIR-16, PRV-CIR-17, PRV-CIR-18, PRV-CIR-20, PRV-CIR-23, PRV-CIR-24, PRV-CIR-25, PRV-CIR-48, PRV-CIR-55, PRV-CIR-58, PRV-CIR-ESP-70, PRV-CIR-AVA-26, PRV-CIR-ESP-27"},
]

def processar_privilegios(privilegios_str):
    """Converte string de privilégios separados por vírgula em lista e filtra"""
    if isinstance(privilegios_str, str) and privilegios_str.strip():
        privilegios_lista = [p.strip() for p in privilegios_str.split(',')]
        
        # Filtrar: remover PRV-0 e privilégios que contêm ESP-
        privilegios_filtrados = [
            p for p in privilegios_lista 
            if p != "PRV-0" and "ESP-" not in p
        ]
        
        return privilegios_filtrados
    return []

def criar_contato(dados_contato):
    """Cria um contato via API"""
    
    # Preparar dados para a requisição
    body = {
        "nome": dados_contato["nome"],
        "emailPrincipal": dados_contato.get("emailPrincipal", ""),
        "telefonePrincipal": dados_contato.get("telefonePrincipal", ""),
        "codigo": dados_contato["codigo"],
        "camposPersonalizados": {
            "campopersonalizado_1_compl_cont": dados_contato["crm"]
        },
        "evento": {
            "tipo": "404",
            "curso": dados_contato["curso"],
            "codLocalOferta": "PRV-0",
            "camposPersonalizados": {
                "campopersonalizado_191_compl_proc": "Ativo"
            }
        },
        "tags": ["Att. Privilégios - 10/2025"],
        "origem": "9",
        "token": TOKEN
    }
    
    try:
        response = requests.post(URL_CONTATO, json=body, headers={"Content-Type": "application/json"})
        
        # Log da resposta para debug
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
    
    body = {
        "tipo": "137",
        "pessoa": {
            "codigo": dados_contato["codigo"]
        },
        "codRegistro": f"{privilegio}-{contato_id}",
        "camposPersonalizados": {
            "campopersonalizado_30_compl_proc": "2025-08-01",
            "campopersonalizado_32_compl_proc": "",
            "campopersonalizado_31_compl_proc": "2028-08-01"
        },
        "curso": dados_contato["curso"],
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
            "codigo": contato["codigo"],
            "crm": contato["crm"],
            "atuacao": contato.get("atuacao", ""),
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
            
            # Processar e filtrar privilégios do contato
            privilegios_lista = processar_privilegios(contato["privilegios"])
            print(f"Privilegios filtrados: {len(privilegios_lista)}")
            
            # Criar eventos para cada privilégio
            for privilegio in privilegios_lista:
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
    print("RELATORIO FINAL")
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
        print(f"\nContato: {detalhe['nome']} (CRM: {detalhe['crm']})")
        print(f"Codigo: {detalhe['codigo']}")
        print(f"Atuacao: {detalhe['atuacao']}")
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
    nome_arquivo = f"relatorio_crm_{timestamp}.json"
    
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(relatorio, arquivo, indent=2, ensure_ascii=False)
        print(f"\nRelatorio salvo em: {nome_arquivo}")
    except Exception as e:
        print(f"\nErro ao salvar relatorio JSON: {e}")

if __name__ == "__main__":
    print("Iniciando processamento de contatos...")
    relatorio = processar_contatos()
    gerar_relatorio(relatorio)