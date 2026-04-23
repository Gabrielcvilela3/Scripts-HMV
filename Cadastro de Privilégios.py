import requests
import json
from datetime import datetime
import time

# Configurações fixas
API_URL = "https://crmhmv.apprubeus.com.br/api/LocalOferta/cadastro"
ORIGEM_FIXA = "9"
TOKEN_FIXO = "d2cc15f39418956cd23eca96b49681ec"

# Lista de dados para cadastro
# Substitua esta lista pelos seus dados reais
dados_cadastro = [
# {"codigo": "PRV-CLT-CR-1","titulo": "Realizar ultrassom à beira do leito","descricao": "Realizar ultrassom à beira do leito","bairro": "Geral"},
# {"codigo": "PRV-CLT-CR-2","titulo": "Realizar punção venosa e arterial central e periférica","descricao": "Realizar punção venosa e arterial central e periférica","bairro": "Geral"},
# {"codigo": "PRV-CLT-CR-3","titulo": "Realizar de toracocentese e paracentese diagnóstica e/ou terapêutica","descricao": "Realizar de toracocentese e paracentese diagnóstica e/ou terapêutica","bairro": "Geral"},
# {"codigo": "PRV-CLT-CR-4","titulo": "Realizar cardioversão elétrica e manobras de ressuscitação","descricao": "Realizar cardioversão elétrica e manobras de ressuscitação","bairro": "Geral"},
# {"codigo": "PRV-CLT-CR-5","titulo": "Realizar intubação endotraqueal","descricao": "Realizar intubação endotraqueal","bairro": "Geral"},
# {"codigo": "PRV-CLT-CR-6","titulo": "Realizar sondagem vesical de demora ou de alívio e passagem de sonda oro ou naso gástrica ou entérica","descricao": "Realizar sondagem vesical de demora ou de alívio e passagem de sonda oro ou naso gástrica ou entérica","bairro": "Geral"},
# {"codigo": "PRV-CLT-CR-7","titulo": "Avaliar, diagnosticar, realizar exame físico e histórico de saúde completo dos pacientes atendidos no HMV, sempre preservando os princípios éticos do atendimento médico","descricao": "Avaliar, diagnosticar, realizar exame físico e histórico de saúde completo dos pacientes atendidos no HMV, sempre preservando os princípios éticos do atendimento médico","bairro": "Geral"},
# {"codigo": "PRV-CLT-CR-8","titulo": "Administrar sedação e analgesia","descricao": "Administrar sedação e analgesia","bairro": "Geral"},
# {"codigo": "PRV-CLT-CR-9","titulo": "Realizar cricotireoidostomia ou intubação retrógrada em casos de emergência","descricao": "Realizar cricotireoidostomia ou intubação retrógrada em casos de emergência","bairro": "Geral"},
# {"codigo": "PRV-CLT-CR-10","titulo": "Manejar ventiladores mecânicos invasivos e não invasivos","descricao": "Manejar ventiladores mecânicos invasivos e não invasivos","bairro": "Geral"},
# {"codigo": "PRV-CLT-CR-11","titulo": "Realizar troca, reposicionamento ou higienização de cânula de traqueostomia","descricao": "Realizar troca, reposicionamento ou higienização de cânula de traqueostomia","bairro": "Geral"},
# {"codigo": "PRV-CLT-CR-12","titulo": "Realizar punção lombar","descricao": "Realizar punção lombar","bairro": "Geral"},
# {"codigo": "PRV-CLT-CR-13","titulo": "Realizar drenagem de tórax","descricao": "Realizar drenagem de tórax","bairro": "Geral"},
# {"codigo": "PRV-CLT-CR-14","titulo": "Prescrever nutrição parenteral","descricao": "Prescrever nutrição parenteral","bairro": "Geral"},
# {"codigo": "PRV-CLT-CR-15","titulo": "Indicar e prescrever medicação trombolítica","descricao": "Indicar e prescrever medicação trombolítica","bairro": "Geral"},
# {"codigo": "PRV-CLT-CR-16","titulo": "Realizar pericardiocentese de urgência","descricao": "Realizar pericardiocentese de urgência","bairro": "Geral"},
# {"codigo": "PRV-CLT-CR-17","titulo": "Realizar o implante de marcapasso venoso temporário","descricao": "Realizar o implante de marcapasso venoso temporário","bairro": "Geral"},
# {"codigo": "PRV-CLT-CR-18","titulo": "Introduzir balão esofágico para tratamento de hemorragia digestiva","descricao": "Introduzir balão esofágico para tratamento de hemorragia digestiva","bairro": "Geral"},
# {"codigo": "PRV-CLT-CR-19","titulo": "Realizar transporte de pacientes críticos","descricao": "Realizar transporte de pacientes críticos","bairro": "Geral"},
# {"codigo": "PRV-CLT-CTI-A-1","titulo": "Realizar ultrassom à beira do leito","descricao": "Realizar ultrassom à beira do leito","bairro": "Geral"},
# {"codigo": "PRV-CLT-CTI-A-2","titulo": "Realizar punção venosa e arterial central e periférica","descricao": "Realizar punção venosa e arterial central e periférica","bairro": "Geral"},
# {"codigo": "PRV-CLT-CTI-A-3","titulo": "Realizar de toracocentese e paracentese diagnóstica e/ou terapêutica","descricao": "Realizar de toracocentese e paracentese diagnóstica e/ou terapêutica","bairro": "Geral"},
# {"codigo": "PRV-CLT-CTI-A-4","titulo": "Realizar cardioversão elétrica e manobras de ressuscitação","descricao": "Realizar cardioversão elétrica e manobras de ressuscitação","bairro": "Geral"},
# {"codigo": "PRV-CLT-CTI-A-5","titulo": "Realizar intubação endotraqueal","descricao": "Realizar intubação endotraqueal","bairro": "Geral"},
# {"codigo": "PRV-CLT-CTI-A-6","titulo": "Realizar sondagem vesical de demora ou de alívio e passagem de sonda oro ou naso gástrica ou entérica","descricao": "Realizar sondagem vesical de demora ou de alívio e passagem de sonda oro ou naso gástrica ou entérica","bairro": "Geral"},
# {"codigo": "PRV-CLT-CTI-A-7","titulo": "Avaliar, diagnosticar, realizar exame físico e histórico de saúde completo dos pacientes atendidos no HMV, sempre preservando os princípios éticos do atendimento médico","descricao": "Avaliar, diagnosticar, realizar exame físico e histórico de saúde completo dos pacientes atendidos no HMV, sempre preservando os princípios éticos do atendimento médico","bairro": "Geral"},
# {"codigo": "PRV-CLT-CTI-A-8","titulo": "Administrar sedação e analgesia","descricao": "Administrar sedação e analgesia","bairro": "Geral"},
# {"codigo": "PRV-CLT-CTI-A-9","titulo": "Realizar cricotireoidostomia ou intubação retrógrada em casos de emergência","descricao": "Realizar cricotireoidostomia ou intubação retrógrada em casos de emergência","bairro": "Geral"},
# {"codigo": "PRV-CLT-CTI-A-10","titulo": "Manejar ventiladores mecânicos invasivos e não invasivos","descricao": "Manejar ventiladores mecânicos invasivos e não invasivos","bairro": "Geral"},
# {"codigo": "PRV-CLT-CTI-A-11","titulo": "Realizar troca, reposicionamento ou higienização de cânula de traqueostomia","descricao": "Realizar troca, reposicionamento ou higienização de cânula de traqueostomia","bairro": "Geral"},
# {"codigo": "PRV-CLT-CTI-A-12","titulo": "Realizar punção lombar","descricao": "Realizar punção lombar","bairro": "Geral"},
# {"codigo": "PRV-CLT-CTI-A-13","titulo": "Realizar drenagem de tórax","descricao": "Realizar drenagem de tórax","bairro": "Geral"},
# {"codigo": "PRV-CLT-CTI-A-14","titulo": "Prescrever nutrição parenteral","descricao": "Prescrever nutrição parenteral","bairro": "Geral"},
# {"codigo": "PRV-CLT-CTI-A-15","titulo": "Indicar e prescrever medicação trombolítica","descricao": "Indicar e prescrever medicação trombolítica","bairro": "Geral"},
# {"codigo": "PRV-CLT-CTI-A-16","titulo": "Realizar pericardiocentese de urgência","descricao": "Realizar pericardiocentese de urgência","bairro": "Geral"},
# {"codigo": "PRV-CLT-CTI-A-17","titulo": "Realizar o implante de marcapasso venoso temporário","descricao": "Realizar o implante de marcapasso venoso temporário","bairro": "Geral"},
# {"codigo": "PRV-CLT-CTI-A-18","titulo": "Introduzir balão esofágico para tratamento de hemorragia digestiva","descricao": "Introduzir balão esofágico para tratamento de hemorragia digestiva","bairro": "Geral"},
# {"codigo": "PRV-CLT-CTI-A-19","titulo": "Realizar transporte de pacientes críticos","descricao": "Realizar transporte de pacientes críticos","bairro": "Geral"},
# {"codigo": "PRV-CLT-CTI-A-20","titulo": "Promover o atendimento inicial do paciente politraumatizado ou queimado","descricao": "Promover o atendimento inicial do paciente politraumatizado ou queimado","bairro": "Geral"},
# {"codigo": "PRV-CLT-CTI-A-21","titulo": "Introduzir cateter de saturação de bulbo jugular","descricao": "Introduzir cateter de saturação de bulbo jugular","bairro": "Geral"},
# {"codigo": "PRV-CLT-CTI-A-22","titulo": "Manejo básico de ultrafiltração e de controle de temperatura de paciente em terapia dialítica contínua","descricao": "Manejo básico de ultrafiltração e de controle de temperatura de paciente em terapia dialítica contínua","bairro": "Geral"},
# {"codigo": "PRV-CLT-CTI-A-23","titulo": "Manejar dispositivos de suporte cardíaco (ECMO e Impella)","descricao": "Manejar dispositivos de suporte cardíaco (ECMO e Impella)","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-A-1","titulo": "Realizar ultrassom à beira do leito","descricao": "Realizar ultrassom à beira do leito","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-A-2","titulo": "Realizar punção venosa e arterial central e periférica","descricao": "Realizar punção venosa e arterial central e periférica","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-A-3","titulo": "Realizar de toracocentese e paracentese diagnóstica e/ou terapêutica","descricao": "Realizar de toracocentese e paracentese diagnóstica e/ou terapêutica","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-A-4","titulo": "Realizar cardioversão elétrica e manobras de ressuscitação","descricao": "Realizar cardioversão elétrica e manobras de ressuscitação","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-A-5","titulo": "Realizar intubação endotraqueal","descricao": "Realizar intubação endotraqueal","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-A-6","titulo": "Realizar sondagem vesical de demora ou de alívio e passagem de sonda oro ou naso gástrica ou entérica","descricao": "Realizar sondagem vesical de demora ou de alívio e passagem de sonda oro ou naso gástrica ou entérica","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-A-7","titulo": "Avaliar, diagnosticar, realizar exame físico e histórico de saúde completo dos pacientes atendidos no HMV, sempre preservando os princípios éticos do atendimento médico","descricao": "Avaliar, diagnosticar, realizar exame físico e histórico de saúde completo dos pacientes atendidos no HMV, sempre preservando os princípios éticos do atendimento médico","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-A-8","titulo": "Administrar sedação e analgesia","descricao": "Administrar sedação e analgesia","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-A-9","titulo": "Realizar cricotireoidostomia ou intubação retrógrada em casos de emergência","descricao": "Realizar cricotireoidostomia ou intubação retrógrada em casos de emergência","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-A-10","titulo": "Manejar ventiladores mecânicos invasivos e não invasivos","descricao": "Manejar ventiladores mecânicos invasivos e não invasivos","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-A-11","titulo": "Realizar troca, reposicionamento ou higienização de cânula de traqueostomia","descricao": "Realizar troca, reposicionamento ou higienização de cânula de traqueostomia","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-A-12","titulo": "Realizar punção lombar","descricao": "Realizar punção lombar","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-A-13","titulo": "Realizar drenagem de tórax","descricao": "Realizar drenagem de tórax","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-A-14","titulo": "Prescrever nutrição parenteral","descricao": "Prescrever nutrição parenteral","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-A-15","titulo": "Indicar e prescrever medicação trombolítica","descricao": "Indicar e prescrever medicação trombolítica","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-A-16","titulo": "Realizar pericardiocentese de urgência","descricao": "Realizar pericardiocentese de urgência","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-A-17","titulo": "Realizar o implante de marcapasso venoso temporário","descricao": "Realizar o implante de marcapasso venoso temporário","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-A-18","titulo": "Introduzir balão esofágico para tratamento de hemorragia digestiva","descricao": "Introduzir balão esofágico para tratamento de hemorragia digestiva","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-A-19","titulo": "Realizar transporte de pacientes críticos","descricao": "Realizar transporte de pacientes críticos","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-A-20","titulo": "Promover o atendimento inicial do paciente politraumatizado ou queimado","descricao": "Promover o atendimento inicial do paciente politraumatizado ou queimado","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-P-1","titulo": "Realizar ultrassom à beira do leito","descricao": "Realizar ultrassom à beira do leito","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-P-2","titulo": "Realizar punção venosa e arterial central e periférica","descricao": "Realizar punção venosa e arterial central e periférica","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-P-3","titulo": "Realizar de toracocentese e paracentese diagnóstica e/ou terapêutica","descricao": "Realizar de toracocentese e paracentese diagnóstica e/ou terapêutica","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-P-4","titulo": "Realizar cardioversão elétrica e manobras de ressuscitação","descricao": "Realizar cardioversão elétrica e manobras de ressuscitação","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-P-5","titulo": "Realizar intubação endotraqueal","descricao": "Realizar intubação endotraqueal","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-P-6","titulo": "Realizar sondagem vesical de demora ou de alívio e passagem de sonda oro ou naso gástrica ou entérica","descricao": "Realizar sondagem vesical de demora ou de alívio e passagem de sonda oro ou naso gástrica ou entérica","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-P-7","titulo": "Avaliar, diagnosticar e estabelecer terapias clínicas e cirúrgicas para pacientes com doenças ginecológicas ou obstétricas, baseadas nas melhores práticas científicas","descricao": "Avaliar, diagnosticar e estabelecer terapias clínicas e cirúrgicas para pacientes com doenças ginecológicas ou obstétricas, baseadas nas melhores práticas científicas","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-P-8","titulo": "Realização de partos, inclusive instrumentados, cesarianas, curetagens uterinas e AMIU (Aspiração Manual Intra-Uterina) pós-abortamento","descricao": "Realização de partos, inclusive instrumentados, cesarianas, curetagens uterinas e AMIU (Aspiração Manual Intra-Uterina) pós-abortamento","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-P-9","titulo": "Realizar cricotireoidostomia ou intubação retrógrada em casos de emergência","descricao": "Realizar cricotireoidostomia ou intubação retrógrada em casos de emergência","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-P-10","titulo": "Manejar ventiladores mecânicos invasivos e não invasivos","descricao": "Manejar ventiladores mecânicos invasivos e não invasivos","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-P-11","titulo": "Realizar troca, reposicionamento ou higienização de cânula de traqueostomia","descricao": "Realizar troca, reposicionamento ou higienização de cânula de traqueostomia","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-P-12","titulo": "Realizar punção lombar","descricao": "Realizar punção lombar","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-P-13","titulo": "Realizar drenagem de tórax","descricao": "Realizar drenagem de tórax","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-P-14","titulo": "Prescrever nutrição parenteral","descricao": "Prescrever nutrição parenteral","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-P-15","titulo": "Realizar pericardiocentese de urgência","descricao": "Realizar pericardiocentese de urgência","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-P-16","titulo": "Realizar pericardiocentese de urgência","descricao": "Realizar pericardiocentese de urgência","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-P-17","titulo": "Avaliar e orientar a alta hospitalar da criança e do recém-nascido","descricao": "Avaliar e orientar a alta hospitalar da criança e do recém-nascido","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-P-18","titulo": "Favorecer o vínculo mãe-filho e a humanização no atendimento","descricao": "Favorecer o vínculo mãe-filho e a humanização no atendimento","bairro": "Geral"},
# {"codigo": "PRV-CLT-EME-P-19","titulo": "Realizar transporte de pacientes pediátricos ou neonatos críticos","descricao": "Realizar transporte de pacientes pediátricos ou neonatos críticos","bairro": "Geral"},
# {"codigo": "PRV-CLT-MAT-1","titulo": "Realizar ultrassom à beira do leito","descricao": "Realizar ultrassom à beira do leito","bairro": "Geral"},
# {"codigo": "PRV-CLT-MAT-2","titulo": "Realizar punção venosa e arterial central e periférica","descricao": "Realizar punção venosa e arterial central e periférica","bairro": "Geral"},
# {"codigo": "PRV-CLT-MAT-3","titulo": "Realizar de toracocentese e paracentese diagnóstica e/ou terapêutica","descricao": "Realizar de toracocentese e paracentese diagnóstica e/ou terapêutica","bairro": "Geral"},
# {"codigo": "PRV-CLT-MAT-4","titulo": "Realizar cardioversão elétrica e manobras de ressuscitação","descricao": "Realizar cardioversão elétrica e manobras de ressuscitação","bairro": "Geral"},
# {"codigo": "PRV-CLT-MAT-5","titulo": "Realizar intubação endotraqueal","descricao": "Realizar intubação endotraqueal","bairro": "Geral"},
# {"codigo": "PRV-CLT-MAT-6","titulo": "Realizar sondagem vesical de demora ou de alívio e passagem de sonda oro ou naso gástrica ou entérica","descricao": "Realizar sondagem vesical de demora ou de alívio e passagem de sonda oro ou naso gástrica ou entérica","bairro": "Geral"},
# {"codigo": "PRV-CLT-MAT-7","titulo": "Avaliar, diagnosticar, realizar exame físico e histórico de saúde completo dos pacientes atendidos no HMV, sempre preservando os princípios éticos do atendimento médico","descricao": "Avaliar, diagnosticar, realizar exame físico e histórico de saúde completo dos pacientes atendidos no HMV, sempre preservando os princípios éticos do atendimento médico","bairro": "Geral"},
# {"codigo": "PRV-CLT-MAT-8","titulo": "Administrar sedação e analgesia","descricao": "Administrar sedação e analgesia","bairro": "Geral"},
# {"codigo": "PRV-CLT-MAT-ESP-9","titulo": "Realizar cirurgias vídeo-endoscópicas para diagnóstico ou ressecção parcial ou total de órgãos genitais femininos pélvicos por patologias benignas (necessidade de treinamento específico: apresentar certificação pela Federação Brasileira de Ginecologia","descricao": "Realizar cirurgias vídeo-endoscópicas para diagnóstico ou ressecção parcial ou total de órgãos genitais femininos pélvicos por patologias benignas (necessidade de treinamento específico: apresentar certificação pela Federação Brasileira de Ginecologia e Obstetrícia (FEBRASGO) ou pela Sociedade Vídeo-Endoscópica do RS (SOCIVERS) de treinamento em cirurgia vídeo-endoscópico em Ginecologia ou comprovação de produção cirúrgica no HMV ou como parte do treinamento em residência médica)","bairro": "Específico"},
# {"codigo": "PRV-CLT-MAT-ESP-10","titulo": "Realizar cirurgias vídeo-endoscópicas para ressecção parcial ou total de órgãos genitais femininos pélvicos por patologias malignas, envolvendo linfadenectomia, incuindo ressecção de órgãos não genitais","descricao": "Realizar cirurgias vídeo-endoscópicas para ressecção parcial ou total de órgãos genitais femininos pélvicos por patologias malignas, envolvendo linfadenectomia, incuindo ressecção de órgãos não genitais (necessidade de treinamento específico: apresentar certificação pela Federação Brasileira de Ginecologia e Obstetrícia (FEBRASGO) ou pela Sociedade Vídeo-Endoscópica do RS (SOCIVERS) de treinamento em cirurgia vídeo-endoscópico em Ginecologia ou comprovação de produção cirúrgica no HMV ou como parte do treinamento em residência médica)","bairro": "Específico"},
# {"codigo": "PRV-CLT-MAT-ESP-11","titulo": "Realizar video-histeroscopia diagnóstica ou terapêutica (necessidade de treinamento específico: apresentar certificação pela Federação Brasileira de Ginecologia e Obstetrícia (FEBRASGO) ou pela Sociedade Vídeo-Endoscópica do RS (SOCIVERS)","descricao": "Realizar video-histeroscopia diagnóstica ou terapêutica (necessidade de treinamento específico: apresentar certificação pela Federação Brasileira de Ginecologia e Obstetrícia (FEBRASGO) ou pela Sociedade Vídeo-Endoscópica do RS (SOCIVERS) de treinamento em cirurgia vídeo-endoscópico em Ginecologia ou comprovação de produção cirúrgica no HMV ou como parte do treinamento em residência médica)","bairro": "Específico"},
# {"codigo": "PRV-CLT-MAT-ESP-12","titulo": "Realizar cirurgias de colocação de dispositivos para correção de incontinência urinária (necessidade de treinamento específico: apresentar certificado de treinamento específico em programa de especialização em uroginecologia e reconstrução pélvica","descricao": "Realizar cirurgias de colocação de dispositivos para correção de incontinência urinária (necessidade de treinamento específico: apresentar certificado de treinamento específico em programa de especialização em uroginecologia e reconstrução pélvica ou comprovação de 100 cirurgias realizadas em paciente oncológico nos últimos 10 anos no HMV)","bairro": "Específico"},
# {"codigo": "PRV-CLT-MAT-13","titulo": "Realizar cirurgias de traquelectomia, histerectomia vaginal, e correção de prolapso genital","descricao": "Realizar cirurgias de traquelectomia, histerectomia vaginal, e correção de prolapso genital","bairro": "Geral"},
# {"codigo": "PRV-CLT-MAT-ESP-14","titulo": "Realizar cirurgias por vídeo-endoscopia assistidas por robô (necessidade de treinamento específico: apresentar certificado de treinamento robótico em curso validado pelo HMV)","descricao": "Realizar cirurgias por vídeo-endoscopia assistidas por robô (necessidade de treinamento específico: apresentar certificado de treinamento robótico em curso validado pelo HMV)","bairro": "Específico"},
# {"codigo": "PRV-CLT-MAT-ESP-15","titulo": "Realizar procedimento de coleta de óvulos orientado por ultrassonografia (necessidade de treinamento específico: apresentar diploma ou certificado de conclusão em residência médica em endocrinologia e infertilidade; ou programa de fellowship","descricao": "Realizar procedimento de coleta de óvulos orientado por ultrassonografia (necessidade de treinamento específico: apresentar diploma ou certificado de conclusão em residência médica em endocrinologia e infertilidade; ou programa de fellowship nacional ou internacional)","bairro": "Específico"},
# {"codigo": "PRV-CLT-MAT-ESP-16","titulo": "Realizar ultrassonografia ginecológica e obstétrica via abdominal e transvaginal (necessidade de treinamento específico: apresentar certificado de especialista pela Federação Brasileira de Ginecologia e Obstetrícia (FEBRASGO) ou curso","descricao": "Realizar ultrassonografia ginecológica e obstétrica via abdominal e transvaginal (necessidade de treinamento específico: apresentar certificado de especialista pela Federação Brasileira de Ginecologia e Obstetrícia (FEBRASGO) ou curso de especialização em ultrassonografia ginecológica e obstétrica)","bairro": "Específico"},
# {"codigo": "PRV-CLT-MAT-ESP-17","titulo": "Realizar ultrassonografia ginecológica e obstétrica via abdominal e transvaginal com procedimentos invasivos, incluindo amniocentese, paracenteses, drenagem de coleções, transfusão sanguínea fetal (necessidade de treinamento específico)","descricao": "Realizar ultrassonografia ginecológica e obstétrica via abdominal e transvaginal com procedimentos invasivos, incluindo amniocentese, paracenteses, drenagem de coleções, transfusão sanguínea fetal (necessidade de treinamento específico: apresentar certificado de especialista pela Federação Brasileira de Ginecologia e Obstetrícia (FEBRASGO) ou curso de especialização em ultrassonografia ginecológica e obstétrica)","bairro": "Específico"},
# {"codigo": "PRV-CLT-MAT-ESP-18","titulo": "Cirurgias fetais por fetoscopia, incluindo correção de meningo-mielocele, fulguração a laser de vasos placentários e inserção de plug endo-traqueal fetal (necessidade de treinamento específico)","descricao": "Cirurgias fetais por fetoscopia, incluindo correção de meningo-mielocele, fulguração a laser de vasos placentários e inserção de plug endo-traqueal fetal (necessidade de treinamento específico: apresentar certificado de qualificação em cirurgia fetal)","bairro": "Específico"},
# {"codigo": "PRV-CLT-MAT-ESP-19","titulo": "Realizar procedimentos diagnósticos e terapêuticos que envolvam peritônio, órgãos intraperitoneais, transição toracoabdominal ou parede torácica por abordagem videolaparoscópica (necessidade de treinamento específico)","descricao": "Realizar procedimentos diagnósticos e terapêuticos que envolvam peritônio, órgãos intraperitoneais, transição toracoabdominal ou parede torácica por abordagem videolaparoscópica (necessidade de treinamento específico: apresentar certificado de residência médica em Cirurgia Geral e/ou Cirurgia Digestiva com comprovada presença de programa específico em cirurgia laparoscópica OU Certificado de conclusão e aprovação em Pós-graduação em Cirurgia Minimamente Invasiva com ênfase em Videolaparoscopia OU Certificado de área de atuação emitido pelo Colégio Brasileiro de Cirurgiões ou Sociedade Brasileira de Cirurgia Robótica e Minimamente Invasiva e/ou certificado como Membro Titular Qualificado emitido pela Sociedade Brasileira de Cirurgia Robótica e Minimamente Invasiva OU comprovar experiência em cirurgia videolaparoscópica com execução mínima de 150 procedimentos nos últimos 5 anos)","bairro": "Específico"},
# {"codigo": "PRV-CLT-MAT-ESP-20","titulo": "Realizar procedimentos diagnósticos e terapêuticos que envolvam peritônio, órgãos intraperitoneais, transição toracoabdominal ou parede torácica por abordagem robótica (necessidade de treinamento específico)","descricao": "Realizar procedimentos diagnósticos e terapêuticos que envolvam peritônio, órgãos intraperitoneais, transição toracoabdominal ou parede torácica por abordagem robótica (necessidade de treinamento específico: apresentar certificado de treinamento e habilitação em cirurgia robótica/cirurgião de console, com aprovação, emitido pela empresa Intuitive/Da Vinci Technology OU de treinamento com aprovação em curso HABILITADOR em cirurgia robótica (cirurgião de console) reconhecido/validado no exterior para realização de cirurgias robóticas na plataforma Da Vinci com comprovação de liberação para realizar cirurgias robóticas emitido por cirurgião habilitado como “proctor” pela Intuitive ou executar suas cirurgias no Hospital Moinhos de Vento sob supervisão de proctor validado pelo Programa de Cirurgia Robótica do Hospital Moinhos de Vento com esta finalidade, até liberação pelo mesmo)","bairro": "Específico"},
# {"codigo": "PRV-CLT-MAT-ESP-21","titulo": "Realizar procedimento de inseminação artificial e fertilização in vitro (necessidade de treinamento específico)","descricao": "Realizar procedimento de inseminação artificial e fertilização in vitro (necessidade de treinamento específico: apresentar diploma ou certificado de conclusão em residência médica em endocrinologia e infertilidade; ou programa de fellowship nacional ou internacional)","bairro": "Específico"},
# {"codigo": "PRV-CLT-UTI-NEO-1","titulo": "Realizar ultrassom à beira do leito","descricao": "Realizar ultrassom à beira do leito","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-NEO-2","titulo": "Realizar punção venosa e arterial central e periférica","descricao": "Realizar punção venosa e arterial central e periférica","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-NEO-3","titulo": "Realizar de toracocentese e paracentese diagnóstica e/ou terapêutica","descricao": "Realizar de toracocentese e paracentese diagnóstica e/ou terapêutica","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-NEO-4","titulo": "Realizar cardioversão elétrica e manobras de ressuscitação","descricao": "Realizar cardioversão elétrica e manobras de ressuscitação","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-NEO-5","titulo": "Realizar intubação endotraqueal","descricao": "Realizar intubação endotraqueal","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-NEO-6","titulo": "Realizar sondagem vesical de demora ou de alívio e passagem de sonda oro ou naso gástrica ou entérica","descricao": "Realizar sondagem vesical de demora ou de alívio e passagem de sonda oro ou naso gástrica ou entérica","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-NEO-7","titulo": "Avaliar, diagnosticar, realizar exame físico e histórico de saúde completo dos pacientes atendidos no HMV, sempre preservando os princípios éticos do atendimento médico","descricao": "Avaliar, diagnosticar, realizar exame físico e histórico de saúde completo dos pacientes atendidos no HMV, sempre preservando os princípios éticos do atendimento médico","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-NEO-8","titulo": "Administrar sedação e analgesia","descricao": "Administrar sedação e analgesia","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-NEO-9","titulo": "Realizar cricotireoidostomia ou intubação retrógrada em casos de emergência","descricao": "Realizar cricotireoidostomia ou intubação retrógrada em casos de emergência","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-NEO-10","titulo": "Manejar ventiladores mecânicos invasivos e não invasivos","descricao": "Manejar ventiladores mecânicos invasivos e não invasivos","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-NEO-11","titulo": "Realizar troca, reposicionamento ou higienização de cânula de traqueostomia","descricao": "Realizar troca, reposicionamento ou higienização de cânula de traqueostomia","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-NEO-12","titulo": "Realizar punção lombar","descricao": "Realizar punção lombar","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-NEO-13","titulo": "Realizar drenagem de tórax","descricao": "Realizar drenagem de tórax","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-NEO-14","titulo": "Prescrever nutrição parenteral","descricao": "Prescrever nutrição parenteral","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-NEO-15","titulo": "Realizar pericardiocentese de urgência","descricao": "Realizar pericardiocentese de urgência","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-NEO-16","titulo": "Orientar os pais quanto aos cuidados com a criança ou recém-nascido","descricao": "Orientar os pais quanto aos cuidados com a criança ou recém-nascido","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-NEO-17","titulo": "Avaliar e orientar a alta hospitalar da criança e do recém-nascido","descricao": "Avaliar e orientar a alta hospitalar da criança e do recém-nascido","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-NEO-18","titulo": "Favorecer o vínculo mãe-filho e a humanização no atendimento","descricao": "Favorecer o vínculo mãe-filho e a humanização no atendimento","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-NEO-19","titulo": "Realizar transporte de pacientes pediátricos ou neonatos críticos","descricao": "Realizar transporte de pacientes pediátricos ou neonatos críticos","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-NEO-20","titulo": "Realizar cateterismo cateterismo umbilical arterial e venoso","descricao": "Realizar cateterismo cateterismo umbilical arterial e venoso","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-NEO-21","titulo": "Administrar surfactante","descricao": "Administrar surfactante","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-P-1","titulo": "Realizar ultrassom à beira do leito","descricao": "Realizar ultrassom à beira do leito","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-P-2","titulo": "Realizar punção venosa e arterial central e periférica","descricao": "Realizar punção venosa e arterial central e periférica","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-P-3","titulo": "Realizar de toracocentese e paracentese diagnóstica e/ou terapêutica","descricao": "Realizar de toracocentese e paracentese diagnóstica e/ou terapêutica","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-P-4","titulo": "Realizar cardioversão elétrica e manobras de ressuscitação","descricao": "Realizar cardioversão elétrica e manobras de ressuscitação","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-P-5","titulo": "Realizar intubação endotraqueal","descricao": "Realizar intubação endotraqueal","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-P-6","titulo": "Realizar sondagem vesical de demora ou de alívio e passagem de sonda oro ou naso gástrica ou entérica","descricao": "Realizar sondagem vesical de demora ou de alívio e passagem de sonda oro ou naso gástrica ou entérica","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-P-7","titulo": "Avaliar, diagnosticar, realizar exame físico e histórico de saúde completo dos pacientes atendidos no HMV, sempre preservando os princípios éticos do atendimento médico","descricao": "Avaliar, diagnosticar, realizar exame físico e histórico de saúde completo dos pacientes atendidos no HMV, sempre preservando os princípios éticos do atendimento médico","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-P-8","titulo": "Administrar sedação e analgesia","descricao": "Administrar sedação e analgesia","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-P-9","titulo": "Realizar cricotireoidostomia ou intubação retrógrada em casos de emergência","descricao": "Realizar cricotireoidostomia ou intubação retrógrada em casos de emergência","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-P-10","titulo": "Manejar ventiladores mecânicos invasivos e não invasivos","descricao": "Manejar ventiladores mecânicos invasivos e não invasivos","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-P-11","titulo": "Realizar troca, reposicionamento ou higienização de cânula de traqueostomia","descricao": "Realizar troca, reposicionamento ou higienização de cânula de traqueostomia","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-P-12","titulo": "Realizar punção lombar","descricao": "Realizar punção lombar","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-P-13","titulo": "Realizar drenagem de tórax","descricao": "Realizar drenagem de tórax","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-P-14","titulo": "Prescrever nutrição parenteral","descricao": "Prescrever nutrição parenteral","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-P-15","titulo": "Realizar pericardiocentese de urgência","descricao": "Realizar pericardiocentese de urgência","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-P-16","titulo": "Orientar os pais quanto aos cuidados com a criança ou recém-nascido","descricao": "Orientar os pais quanto aos cuidados com a criança ou recém-nascido","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-P-17","titulo": "Avaliar e orientar a alta hospitalar da criança e do recém-nascido","descricao": "Avaliar e orientar a alta hospitalar da criança e do recém-nascido","bairro": "Geral"},
# {"codigo": "PRV-CLT-UTI-P-18","titulo": "Favorecer o vínculo mãe-filho e a humanização no atendimento","descricao": "Favorecer o vínculo mãe-filho e a humanização no atendimento","bairro": "Geral"}
]

def fazer_requisicao(item):
    """
    Faz a requisição POST para cadastrar um item no CRM
    """
    # Monta o body da requisição com os campos fixos
    # Formata o título como: codigo - titulo
    titulo_formatado = f"{item['codigo']} - {item['titulo']}"
    
    body = {
        "codigo": item["codigo"],
        "titulo": titulo_formatado,
        "descricao": item["descricao"],
        "bairro": item["bairro"],
        "origem": ORIGEM_FIXA,
        "token": TOKEN_FIXO
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(API_URL, json=body, headers=headers, timeout=30)
        return {
            "sucesso": response.status_code == 200,
            "status_code": response.status_code,
            "response_text": response.text,
            "response_json": response.json() if response.headers.get('content-type', '').startswith('application/json') else None
        }
    except requests.exceptions.Timeout:
        return {
            "sucesso": False,
            "status_code": None,
            "response_text": "Timeout na requisição",
            "response_json": None,
            "erro": "Timeout"
        }
    except requests.exceptions.RequestException as e:
        return {
            "sucesso": False,
            "status_code": None,
            "response_text": str(e),
            "response_json": None,
            "erro": str(e)
        }
    except Exception as e:
        return {
            "sucesso": False,
            "status_code": None,
            "response_text": str(e),
            "response_json": None,
            "erro": str(e)
        }

def main():
    print("=" * 80)
    print("INICIANDO CADASTRO DE LOCAIS NO CRM")
    print("=" * 80)
    print(f"Total de itens para cadastrar: {len(dados_cadastro)}")
    print(f"URL da API: {API_URL}")
    print(f"Origem fixa: {ORIGEM_FIXA}")
    print("=" * 80)
    print()
    
    # Lista para armazenar o relatório
    relatorio = []
    sucessos = 0
    falhas = 0
    
    # Processa cada item
    for i, item in enumerate(dados_cadastro, 1):
        print(f"[{i:03d}/{len(dados_cadastro):03d}] Processando: {item['codigo']}")
        
        # Faz a requisição
        resultado = fazer_requisicao(item)
        
        # Adiciona ao relatório
        registro_relatorio = {
            "numero": i,
            "item_original": item.copy(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "resultado": resultado
        }
        relatorio.append(registro_relatorio)
        
        # Exibe resultado no console
        if resultado["sucesso"]:
            print(f"[SUCESSO] - {item['codigo']} - {item['titulo']}")
            sucessos += 1
        else:
            print(f"[ERRO] - {item['codigo']} - {item['titulo']}")
            print(f"         Status: {resultado.get('status_code', 'N/A')}")
            print(f"         Erro: {resultado.get('response_text', 'Erro desconhecido')}")
            falhas += 1
        
        print()
        
        # Pequena pausa entre requisições para não sobrecarregar a API
        time.sleep(0.5)
    
    # Resumo final
    print("=" * 80)
    print("RESUMO DO PROCESSAMENTO")
    print("=" * 80)
    print(f"Total processado: {len(dados_cadastro)}")
    print(f"Sucessos: {sucessos}")
    print(f"Falhas: {falhas}")
    print(f"Taxa de sucesso: {(sucessos/len(dados_cadastro)*100):.1f}%")
    print("=" * 80)
    
    # Gera arquivo de relatório
    nome_arquivo = f"relatorio_cadastro_crm_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    relatorio_final = {
        "resumo": {
            "data_execucao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_itens": len(dados_cadastro),
            "sucessos": sucessos,
            "falhas": falhas,
            "taxa_sucesso": round(sucessos/len(dados_cadastro)*100, 2)
        },
        "detalhes": relatorio
    }
    
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            json.dump(relatorio_final, arquivo, indent=2, ensure_ascii=False)
        print(f"Relatório salvo em: {nome_arquivo}")
    except Exception as e:
        print(f"Erro ao salvar relatório: {e}")
        print("Exibindo relatório no console:")
        print(json.dumps(relatorio_final, indent=2, ensure_ascii=False))
    
    print("\nProcessamento concluído!")

if __name__ == "__main__":
    # Verifica se há dados para processar
    if not dados_cadastro:
        print("ATENÇÃO: A lista 'dados_cadastro' está vazia!")
        print("Adicione os dados que deseja cadastrar na variável 'dados_cadastro' no início do script.")
    else:
        main()