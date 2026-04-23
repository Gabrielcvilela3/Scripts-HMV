import requests
import json
from datetime import datetime
import time

# URLs das APIs
URL_CONTATO = "https://crmhmv.apprubeus.com.br/api/Contato/cadastro"
URL_EVENTO = "https://crmhmv.apprubeus.com.br/api/Evento/cadastro"

# Token fixo
TOKEN = "d2cc15f39418956cd23eca96b49681ec"

# Lista de dados dos contatos (exemplo)
contatos_dados = [
# {"nome": "ALESSANDRA CEZIMBRA DORSCH","emailPrincipal": "cezimbraa@yahoo.com.br","telefonePrincipal": "(51)999730473","codigo": "27204","campopersonalizado_1_compl_cont": "27204","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-EME-A-31","campopersonalizado_190_compl_proc": "44313","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "ALESSANDRA SHMULERG","emailPrincipal": "hannahale@gmail.com","telefonePrincipal": "(51)999612930","codigo": "18848","campopersonalizado_1_compl_cont": "18848","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-EME-A-18","campopersonalizado_190_compl_proc": "45862","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "ALEX POSPICH CIOFFI","emailPrincipal": "","telefonePrincipal": "(51)33395103","codigo": "30536","campopersonalizado_1_compl_cont": "30536","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-21","campopersonalizado_190_compl_proc": "40634","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "ALEXANDRE SILVEIRO DO CANTO","emailPrincipal": "docanto.uti@gmail.com","telefonePrincipal": "(51)998949099","codigo": "29078","campopersonalizado_1_compl_cont": "29078","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "45862","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "ALINE COLETTO JACCOTTET","emailPrincipal": "","telefonePrincipal": "","codigo": "41286","campopersonalizado_1_compl_cont": "41286","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-18","campopersonalizado_190_compl_proc": "44348","campopersonalizado_191_compl_proc": "Licença Maternidade","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "ALINE MARIA ASCOLI CICHELERO","emailPrincipal": "","telefonePrincipal": "(51)32121463","codigo": "33021","campopersonalizado_1_compl_cont": "33021","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "42604","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "ANA BEATRIZ MACHADO DE AGUIAR","emailPrincipal": "","telefonePrincipal": "","codigo": "36975","campopersonalizado_1_compl_cont": "36975","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-EME-A-31","campopersonalizado_190_compl_proc": "44690","campopersonalizado_191_compl_proc": "Férias","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "ANA CAROLINA KUWER BUGIN","emailPrincipal": "anakuwer@gmail.com","telefonePrincipal": "(51)982186118","codigo": "49196","campopersonalizado_1_compl_cont": "49196","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-31","campopersonalizado_190_compl_proc": "45659","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "ANA PAULA DA SILVA MIRANDA","emailPrincipal": "","telefonePrincipal": "(51)999624663","codigo": "21049","campopersonalizado_1_compl_cont": "21049","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-UTI-P-51","campopersonalizado_190_compl_proc": "44151","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "ANA PAULA SCHUCH MATA","emailPrincipal": "anasmata@gmail.com","telefonePrincipal": "(51)999851449","codigo": "26141","campopersonalizado_1_compl_cont": "26141","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-UTI-NEO-51","campopersonalizado_190_compl_proc": "40665","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "DESIREE DE FREITAS VALLE VOLKMER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "ANA PAULA TOMAZONI BORTOLOMEDI","emailPrincipal": "anabortolomedi@gmail.com","telefonePrincipal": "(51)981162854","codigo": "37011","campopersonalizado_1_compl_cont": "37011","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-18","campopersonalizado_190_compl_proc": "42832","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "ANDRE LUCAS RIBEIRO","emailPrincipal": "lucasribeiro.andre@gmail.com","telefonePrincipal": "(51)999828016","codigo": "43705","campopersonalizado_1_compl_cont": "43705","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-56","campopersonalizado_190_compl_proc": "45583","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "ANDRE LUIZ DA SILVA ALENCASTRO","emailPrincipal": "alsalencastro@gmail.com","telefonePrincipal": "(51)32252441","codigo": "28190","campopersonalizado_1_compl_cont": "28190","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-CR-18","campopersonalizado_190_compl_proc": "40133","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ARTUR PACHECO SEABRA","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "ARTHUR GUS MANFRO","emailPrincipal": "","telefonePrincipal": "","codigo": "49674","campopersonalizado_1_compl_cont": "49674","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-41","campopersonalizado_190_compl_proc": "45691","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "BETUSA KRAMER DE OLIVEIRA","emailPrincipal": "bkramer235@gmail.com","telefonePrincipal": "(51)33477473","codigo": "23263","campopersonalizado_1_compl_cont": "23263","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "40910","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "BRUNA CONTE","emailPrincipal": "brunafconte@gmail.com","telefonePrincipal": "(51)995611168","codigo": "45044","campopersonalizado_1_compl_cont": "45044","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "44627","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "BRUNA FERREIRA DA COSTA FISCHER","emailPrincipal": "","telefonePrincipal": "","codigo": "37230","campopersonalizado_1_compl_cont": "37230","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-18","campopersonalizado_190_compl_proc": "44851","campopersonalizado_191_compl_proc": "Licença Maternidade","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "BRUNO JASKULSKI KOTZIAN","emailPrincipal": "brunojkotzian@gmail.com","telefonePrincipal": "(51)981427408","codigo": "50393","campopersonalizado_1_compl_cont": "50393","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "45719","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "CAMILA GARCIA PEREIRA","emailPrincipal": "","telefonePrincipal": "(54)99968-8128","codigo": "38904","campopersonalizado_1_compl_cont": "38904","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-5","campopersonalizado_190_compl_proc": "44205","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "CAMILE DO AMARAL CAMARGO","emailPrincipal": "","telefonePrincipal": "(51)998414545","codigo": "26184","campopersonalizado_1_compl_cont": "26184","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-UTI-NEO-51","campopersonalizado_190_compl_proc": "40616","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "DESIREE DE FREITAS VALLE VOLKMER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "CANDICE GUERRA","emailPrincipal": "candiceguerrapoa@gmail.com","telefonePrincipal": "(51)996095015","codigo": "22748","campopersonalizado_1_compl_cont": "22748","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "41397","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "CARLA PIENIZ","emailPrincipal": "carla.pieniz@hotmail.com","telefonePrincipal": "(55)996995942","codigo": "48693","campopersonalizado_1_compl_cont": "48693","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-31","campopersonalizado_190_compl_proc": "45404","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "CAROLINE CARDOSO KLEIN","emailPrincipal": "","telefonePrincipal": "","codigo": "42982","campopersonalizado_1_compl_cont": "42982","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-P-18","campopersonalizado_190_compl_proc": "44581","campopersonalizado_191_compl_proc": "Licença Maternidade","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "CECYRA BAUERMANN COLLARES MACHADO","emailPrincipal": "cecyrabcmachado@yahoo.com","telefonePrincipal": "(48)991270402","codigo": "36434","campopersonalizado_1_compl_cont": "36434","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-18","campopersonalizado_190_compl_proc": "45667","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "CHRISTIAN KINOPP","emailPrincipal": "chkinopp@gmail.com","telefonePrincipal": "(51)997600893","codigo": "39294","campopersonalizado_1_compl_cont": "39294","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "45855","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "CRISLAINE PADILHA PENNA","emailPrincipal": "crislainepenna@gmail.com","telefonePrincipal": "(51)991138887","codigo": "47798","campopersonalizado_1_compl_cont": "47798","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "45810","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "CRISTIANO DE OLIVEIRA ROXO","emailPrincipal": "crisroxo@gmail.com","telefonePrincipal": "(51)992867596","codigo": "32728","campopersonalizado_1_compl_cont": "32728","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-UTI-P-51","campopersonalizado_190_compl_proc": "41246","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "CRISTINA DETONI TRENTIN","emailPrincipal": "cris.Trentin@yahoo.com","telefonePrincipal": "(51)989479190","codigo": "48719","campopersonalizado_1_compl_cont": "48719","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "45491","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "DANIEL AUGUSTO BECKER","emailPrincipal": "","telefonePrincipal": "(51)30194167","codigo": "30979","campopersonalizado_1_compl_cont": "30979","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-18","campopersonalizado_190_compl_proc": "41589","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "DANIEL SANT ANNA VIEIRA","emailPrincipal": "","telefonePrincipal": "(54)30194581","codigo": "21778","campopersonalizado_1_compl_cont": "21778","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-18","campopersonalizado_190_compl_proc": "41928","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "DANIELA ELAINE ROTH BENINCASA","emailPrincipal": "daniroth79@gmail.com","telefonePrincipal": "(51)992684028","codigo": "27852","campopersonalizado_1_compl_cont": "27852","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "42345","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "DANIELE AZEVEDO KANAN DE FREITAS","emailPrincipal": "daniakf@gmail.com","telefonePrincipal": "(51)998434843","codigo": "25480","campopersonalizado_1_compl_cont": "25480","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "45852","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "DEBORA DETTMER","emailPrincipal": "dett.debora@gmail.com","telefonePrincipal": "(51)981495086","codigo": "47526","campopersonalizado_1_compl_cont": "47526","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "45400","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "DENISE HERMANN NODARI","emailPrincipal": "","telefonePrincipal": "","codigo": "34318","campopersonalizado_1_compl_cont": "34318","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-EME-A-29","campopersonalizado_190_compl_proc": "41901","campopersonalizado_191_compl_proc": "Licença Maternidade","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "DIANA MARGARITA CASCAN VALIENTE","emailPrincipal": "dcascan@hotmail.com","telefonePrincipal": "(51)991022400","codigo": "34202","campopersonalizado_1_compl_cont": "34202","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-18","campopersonalizado_190_compl_proc": "44166","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "DIOGO BOLSSON DE MORAES ROCHA","emailPrincipal": "diogo.bmr@hotmail.com","telefonePrincipal": "(51)999626668","codigo": "47931","campopersonalizado_1_compl_cont": "47931","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "45719","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "DIOGO SILVA PIARDI","emailPrincipal": "dpiardi@gmail.com","telefonePrincipal": "(51)992574707","codigo": "34448","campopersonalizado_1_compl_cont": "34448","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-18","campopersonalizado_190_compl_proc": "45362","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "ERIKA BASTOS SCHLUTER","emailPrincipal": "erikabsch@gmail.com","telefonePrincipal": "(51)980150550","codigo": "33170","campopersonalizado_1_compl_cont": "33170","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-EME-A-31","campopersonalizado_190_compl_proc": "44991","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "ERNANI COSER SEELIG","emailPrincipal": "","telefonePrincipal": "","codigo": "30874","campopersonalizado_1_compl_cont": "30874","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-UTI-NEO-51","campopersonalizado_190_compl_proc": "43374","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "DESIREE DE FREITAS VALLE VOLKMER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "FABIANE NEIVA BACKES","emailPrincipal": "fabianebackes@gmail.com","telefonePrincipal": "(51)999717755","codigo": "25221","campopersonalizado_1_compl_cont": "25221","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "42705","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "FELIPE SCHAICH","emailPrincipal": "felipeschaich@yahoo.com.br","telefonePrincipal": "(51)981813449","codigo": "33639","campopersonalizado_1_compl_cont": "33639","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-18","campopersonalizado_190_compl_proc": "45855","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "FERNANDA CHMELNITSKY WAINBERG","emailPrincipal": "","telefonePrincipal": "(51)991029929","codigo": "28592","campopersonalizado_1_compl_cont": "28592","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-EME-A-18","campopersonalizado_190_compl_proc": "43185","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "FERNANDA CRISTINA SCARPA","emailPrincipal": "","telefonePrincipal": "(51)93153969","codigo": "31062","campopersonalizado_1_compl_cont": "31062","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-UTI-P-51","campopersonalizado_190_compl_proc": "41988","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "FERNANDA LAZZAROTTO STRINGHI","emailPrincipal": "felazzastringhi@gmail.com","telefonePrincipal": "(51)35572943","codigo": "30985","campopersonalizado_1_compl_cont": "30985","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "42968","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "FRANCINE POSSEBON BERLESI","emailPrincipal": "","telefonePrincipal": "","codigo": "44211","campopersonalizado_1_compl_cont": "44211","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-EME-A-18","campopersonalizado_190_compl_proc": "44669","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "GABRIELA BLOS","emailPrincipal": "gabiblos72@gmail.com","telefonePrincipal": "(51)993363059","codigo": "23092","campopersonalizado_1_compl_cont": "23092","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-UTI-NEO-51","campopersonalizado_190_compl_proc": "40602","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "DESIREE DE FREITAS VALLE VOLKMER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "GABRIELA NOBREGA MENDONCA","emailPrincipal": "gabrielanobregam@gmail.com","telefonePrincipal": "(81)987846024","codigo": "48282","campopersonalizado_1_compl_cont": "48282","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-18","campopersonalizado_190_compl_proc": "44669","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "GABRIELA NONTICURI BIANCHI","emailPrincipal": "","telefonePrincipal": "","codigo": "39787","campopersonalizado_1_compl_cont": "39787","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "43595","campopersonalizado_191_compl_proc": "Licença Maternidade","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "GABRIELA RODRIGUES IZOLAN","emailPrincipal": "g.izolan@hotmail.com","telefonePrincipal": "(55)999220055","codigo": "39416","campopersonalizado_1_compl_cont": "39416","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "45855","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "GABRIELA VERDUM","emailPrincipal": "gabrielaverdum@hotmail.com","telefonePrincipal": "(51)991214478","codigo": "24860","campopersonalizado_1_compl_cont": "24860","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-UTI-NEO-51","campopersonalizado_190_compl_proc": "39847","campopersonalizado_191_compl_proc": "Férias","campopersonalizado_192_compl_proc": "DESIREE DE FREITAS VALLE VOLKMER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "GENIARA DA SILVA CONRADO","emailPrincipal": "geniara.conrado@gmail.com","telefonePrincipal": "(51)982213737","codigo": "27757","campopersonalizado_1_compl_cont": "27757","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-UTI-P-51","campopersonalizado_190_compl_proc": "43395","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "GIOVANA THOMASI JAHNKE","emailPrincipal": "giovana.thomasi@hotmail.com","telefonePrincipal": "(55)991591542","codigo": "47209","campopersonalizado_1_compl_cont": "47209","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "45834","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "GRAZIELA SANTOS MASSOCHINI DE BELLI","emailPrincipal": "gsmassochini@gmail.com","telefonePrincipal": "(51)32412461","codigo": "39269","campopersonalizado_1_compl_cont": "39269","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "43451","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "HENRIQUE IAHNKE GARBIN","emailPrincipal": "higarbin@gmail.com","telefonePrincipal": "(51)985617269","codigo": "47864","campopersonalizado_1_compl_cont": "47864","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-18","campopersonalizado_190_compl_proc": "45267","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "HENRIQUE MEZZOMO PASQUAL","emailPrincipal": "henriquemezzomop@gmail.com","telefonePrincipal": "(55)996739142","codigo": "50670","campopersonalizado_1_compl_cont": "50670","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "45712","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "HENRIQUE SALTZ NETTO","emailPrincipal": "henrique@salt.com.br","telefonePrincipal": "(51)33888087","codigo": "27878","campopersonalizado_1_compl_cont": "27878","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-18","campopersonalizado_190_compl_proc": "41824","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "HILEL LEVIN","emailPrincipal": "ivs@terra.com.br","telefonePrincipal": "","codigo": "11923","campopersonalizado_1_compl_cont": "11923","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CR-19","campopersonalizado_190_compl_proc": "33602","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ARTUR PACHECO SEABRA","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "IAN TEIXEIRA E SOUSA","emailPrincipal": "iantsousa@gmail.com","telefonePrincipal": "(51)999479755","codigo": "41692","campopersonalizado_1_compl_cont": "41692","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-UTI-P-51","campopersonalizado_190_compl_proc": "44440","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "ISABEL CRISTINA FELTES","emailPrincipal": "belfeltes@gmail.com","telefonePrincipal": "(51)986222949","codigo": "44535","campopersonalizado_1_compl_cont": "44535","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "44958","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "ISABELLA MACHADO BALDINO","emailPrincipal": "baldinoisabella@gmail.com","telefonePrincipal": "(54)996191039","codigo": "47961","campopersonalizado_1_compl_cont": "47961","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-EME-A-31","campopersonalizado_190_compl_proc": "45404","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "ISRAEL DE QUADROS CARDOSO","emailPrincipal": "israel_famed@yahoo.com.br","telefonePrincipal": "(51)992816273","codigo": "34621","campopersonalizado_1_compl_cont": "34621","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "45785","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "JANICE VELLEDA BRANCAO","emailPrincipal": "","telefonePrincipal": "","codigo": "27953","campopersonalizado_1_compl_cont": "27953","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-UTI-P-51","campopersonalizado_190_compl_proc": "39134","campopersonalizado_191_compl_proc": "Férias","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "JAQUELINE WEBER","emailPrincipal": "JAQUEWEB2705@GMAIL.COM","telefonePrincipal": "(51)999481960","codigo": "24954","campopersonalizado_1_compl_cont": "24954","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "42312","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "JIHAD AHMAD HATEM","emailPrincipal": "jihadhatem@yahoo.com.br","telefonePrincipal": "(51)91901178","codigo": "28694","campopersonalizado_1_compl_cont": "28694","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-CR-18","campopersonalizado_190_compl_proc": "40707","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ARTUR PACHECO SEABRA","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "JOANA MATTIONI OURIQUE MONTEIRO","emailPrincipal": "pedjoanamattioni@gmail.com","telefonePrincipal": "(55)991542251","codigo": "43201","campopersonalizado_1_compl_cont": "43201","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "45636","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "JOAO FELIPE FOSCARIN PEDROSO BASEGGIO","emailPrincipal": "joaofelipebaseggio@gmail.com","telefonePrincipal": "(51)991277636","codigo": "43551","campopersonalizado_1_compl_cont": "43551","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-18","campopersonalizado_190_compl_proc": "44146","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "JOAO PEDRO MENDONCA BIDART","emailPrincipal": "","telefonePrincipal": "(51)30228631","codigo": "30604","campopersonalizado_1_compl_cont": "30604","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-EME-A-18","campopersonalizado_190_compl_proc": "40961","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "JOEL STEFANI","emailPrincipal": "stefani.94@gmail.com","telefonePrincipal": "(51)999297499","codigo": "46999","campopersonalizado_1_compl_cont": "46999","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-18","campopersonalizado_190_compl_proc": "45477","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "JULIA DAUERNHEIMER MACHADO","emailPrincipal": "juliadmm@gmail.com","telefonePrincipal": "(51)981100466","codigo": "44702","campopersonalizado_1_compl_cont": "44702","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "45750","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "JULIA DULLIUS OLIVEIRA","emailPrincipal": "juliadullius@gmail.com","telefonePrincipal": "(51)992993223","codigo": "49824","campopersonalizado_1_compl_cont": "49824","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-31","campopersonalizado_190_compl_proc": "45293","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "JULIA LIMA VIEIRA","emailPrincipal": "","telefonePrincipal": "","codigo": "44102","campopersonalizado_1_compl_cont": "44102","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-UTI-P-37","campopersonalizado_190_compl_proc": "44987","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "JULIANA HARDTKE TEICHERT","emailPrincipal": "jujuht@hotmail.com","telefonePrincipal": "(51)996535828","codigo": "31368","campopersonalizado_1_compl_cont": "31368","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-18","campopersonalizado_190_compl_proc": "45817","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "JULIANA MARA STORMOVSKI DE ANDRADE","emailPrincipal": "","telefonePrincipal": "(51)30194167","codigo": "30068","campopersonalizado_1_compl_cont": "30068","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-18","campopersonalizado_190_compl_proc": "41589","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "KARINA LORENZI MARRAMARCO MAZZUCCO","emailPrincipal": "karinamazzucco@gmail.com","telefonePrincipal": "(51)984570893","codigo": "26905","campopersonalizado_1_compl_cont": "26905","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "41201","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "KELIN CRISTINE MARTIN HACKENHAAR","emailPrincipal": "kelinmartin@gmail.com","telefonePrincipal": "(51)985064125","codigo": "36514","campopersonalizado_1_compl_cont": "36514","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-43","campopersonalizado_190_compl_proc": "43073","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "KELLY CARBALLO DE SOUZA","emailPrincipal": "kellycarballo@gmail.com","telefonePrincipal": "(51)991544001","codigo": "28642","campopersonalizado_1_compl_cont": "28642","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-EME-A-18","campopersonalizado_190_compl_proc": "40889","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "LARISSA DE LIMA OLIMPIO AZEVEDO SOUZA","emailPrincipal": "lariolimpio8@gmail.com","telefonePrincipal": "(51)998388249","codigo": "57357","campopersonalizado_1_compl_cont": "57357","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "45839","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "LAURA CORSO CAVALHEIRO","emailPrincipal": "laucorso@gmail.com","telefonePrincipal": "(51)993642503","codigo": "36489","campopersonalizado_1_compl_cont": "36489","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "43234","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "LAURA DREHMER JESINSKI","emailPrincipal": "","telefonePrincipal": "(51)99988-6722","codigo": "42233","campopersonalizado_1_compl_cont": "42233","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-18","campopersonalizado_190_compl_proc": "44287","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "LEANDRA RECH","emailPrincipal": "le.rech@gmail.com","telefonePrincipal": "(51)991799832","codigo": "36179","campopersonalizado_1_compl_cont": "36179","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-UTI-P-51","campopersonalizado_190_compl_proc": "42681","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "LEONARDO SERENA DE MORAIS","emailPrincipal": "leoemergencista@gmail.com","telefonePrincipal": "(54)996487480","codigo": "51493","campopersonalizado_1_compl_cont": "51493","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-31","campopersonalizado_190_compl_proc": "45813","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "LISANDRA PACHECO DIAS XAVIER","emailPrincipal": "lis.xavier@hotmail.com","telefonePrincipal": "(51)33387837","codigo": "27006","campopersonalizado_1_compl_cont": "27006","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "40763","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "LISIANE PALERMO PROCHNOW DA COSTA","emailPrincipal": "","telefonePrincipal": "","codigo": "38381","campopersonalizado_1_compl_cont": "38381","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "44676","campopersonalizado_191_compl_proc": "Licença Maternidade","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "LUANA CANEVESE SELL","emailPrincipal": "luanasellpf@gmail.com","telefonePrincipal": "(51)999434549","codigo": "38677","campopersonalizado_1_compl_cont": "38677","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "43423","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "LUCAS MORAES SITYA","emailPrincipal": "plan3jam3nto@gmail.com","telefonePrincipal": "(51)999549268","codigo": "27089","campopersonalizado_1_compl_cont": "27089","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CR-5","campopersonalizado_190_compl_proc": "39420","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ARTUR PACHECO SEABRA","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "LUCAS OLIVEIRA JUNQUEIRA E SILVA","emailPrincipal": "lojesilva@gmail.com","telefonePrincipal": "(51)992394964","codigo": "49124","campopersonalizado_1_compl_cont": "49124","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-18","campopersonalizado_190_compl_proc": "45264","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "LUCAS VIEIRA DE SOUZA","emailPrincipal": "lucasvdesouza@hotmail.com","telefonePrincipal": "(51)999098649","codigo": "36859","campopersonalizado_1_compl_cont": "36859","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-18","campopersonalizado_190_compl_proc": "42982","campopersonalizado_191_compl_proc": "Férias","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "LUCIANA KUNDE","emailPrincipal": "lucianakunde@gmail.com","telefonePrincipal": "(51)999635993","codigo": "49729","campopersonalizado_1_compl_cont": "49729","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-18","campopersonalizado_190_compl_proc": "45541","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "LUCIANA MARQUARDT DA SILVEIRA","emailPrincipal": "","telefonePrincipal": "","codigo": "35390","campopersonalizado_1_compl_cont": "35390","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "42390","campopersonalizado_191_compl_proc": "Férias","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "LUCIANE MARIA FABIAN RESTELATTO","emailPrincipal": "","telefonePrincipal": "(51)32767212","codigo": "35307","campopersonalizado_1_compl_cont": "35307","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "42968","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "LUIZA FOSCHIERA","emailPrincipal": "luizafoschiera@hotmail.com","telefonePrincipal": "(51)996998366","codigo": "42723","campopersonalizado_1_compl_cont": "42723","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "44593","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "MARCIO ATAIDE LANCA","emailPrincipal": "mlanca@terra.com.br","telefonePrincipal": "(51)33336132","codigo": "22013","campopersonalizado_1_compl_cont": "22013","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-52","campopersonalizado_190_compl_proc": "40909","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "MARIA CLARA FORMOLO DE SOUZA","emailPrincipal": "mariaclaraformolo@hotmail.com","telefonePrincipal": "(49)991487090","codigo": "52042","campopersonalizado_1_compl_cont": "52042","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CR-18","campopersonalizado_190_compl_proc": "45813","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JUCARA GASPARETTO MACCARI","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "MARIA JULIA QUEIROZ PIAI","emailPrincipal": "maju.piai@gmail.com","telefonePrincipal": "(45)991074110","codigo": "52095","campopersonalizado_1_compl_cont": "52095","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-18","campopersonalizado_190_compl_proc": "45566","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "MARIANA BUHLER","emailPrincipal": "","telefonePrincipal": "(51)997169774","codigo": "36143","campopersonalizado_1_compl_cont": "36143","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "44259","campopersonalizado_191_compl_proc": "Férias","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "MARIANA FENSTERSEIFER MATTIONI","emailPrincipal": "","telefonePrincipal": "","codigo": "34785","campopersonalizado_1_compl_cont": "34785","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "42311","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "MARIANA NUNES FERREIRA JOST","emailPrincipal": "mariana_nferreira@hotmail.com","telefonePrincipal": "(51)998061984","codigo": "37185","campopersonalizado_1_compl_cont": "37185","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "44382","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "MARTINA KIRST","emailPrincipal": "","telefonePrincipal": "(51)981428840","codigo": "37238","campopersonalizado_1_compl_cont": "37238","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "42919","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "MATHEUS PEREIRA SCHNEIDER","emailPrincipal": "","telefonePrincipal": "(51)999945806","codigo": "40156","campopersonalizado_1_compl_cont": "40156","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-18","campopersonalizado_190_compl_proc": "44250","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "MICHELE JANAINA GRACIOLI SCHNEIDER","emailPrincipal": "michgracioli@yahoo.com.br","telefonePrincipal": "(51)992442876","codigo": "39902","campopersonalizado_1_compl_cont": "39902","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-18","campopersonalizado_190_compl_proc": "43619","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "MIRELLA REINEHR PONTES","emailPrincipal": "mirella.r.pontes@gmail.com","telefonePrincipal": "(51)981286033","codigo": "45949","campopersonalizado_1_compl_cont": "45949","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-UTI-P-51","campopersonalizado_190_compl_proc": "45124","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "NATALIA BASSO BONIATTI","emailPrincipal": "nataliaboniatti@gmail.com","telefonePrincipal": "(55)996944101","codigo": "46184","campopersonalizado_1_compl_cont": "46184","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-18","campopersonalizado_190_compl_proc": "45548","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "NATALIA BITENCOURT DE LIMA","emailPrincipal": "","telefonePrincipal": "(51)32082101","codigo": "35974","campopersonalizado_1_compl_cont": "35974","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "41730","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "NATALIA FAVIERO DE VASCONCELLOS","emailPrincipal": "nataliafvasconcellos@gmail.com","telefonePrincipal": "(51)980105090","codigo": "44071","campopersonalizado_1_compl_cont": "44071","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "45029","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "NATHALIE BELLO","emailPrincipal": "","telefonePrincipal": "","codigo": "37055","campopersonalizado_1_compl_cont": "37055","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "43724","campopersonalizado_191_compl_proc": "Férias","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "NAYARA MONTEIRO PINHEIRO","emailPrincipal": "","telefonePrincipal": "(51)991464658","codigo": "44910","campopersonalizado_1_compl_cont": "44910","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-31","campopersonalizado_190_compl_proc": "44154","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "NICOLE SANTOS","emailPrincipal": "nicolesantos89@gmail.com","telefonePrincipal": "(53)981090887","codigo": "43077","campopersonalizado_1_compl_cont": "43077","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-18","campopersonalizado_190_compl_proc": "44483","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "NIVEA MARIA OLIVEIRA GUIMARAES","emailPrincipal": "niveaguima@hotmail.com","telefonePrincipal": "(51)33872841","codigo": "25060","campopersonalizado_1_compl_cont": "25060","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "41141","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "PATRICIA BORGES CAUDURO","emailPrincipal": "patriciacauduro545@gmail.com","telefonePrincipal": "(51)991545430","codigo": "40837","campopersonalizado_1_compl_cont": "40837","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-52","campopersonalizado_190_compl_proc": "45089","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "PATRICIA RODRIGUES DA SILVA TRINDADE","emailPrincipal": "","telefonePrincipal": "(51)997492922","codigo": "34529","campopersonalizado_1_compl_cont": "34529","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-UTI-P-51","campopersonalizado_190_compl_proc": "42149","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "PAULA FIGUEIREDO SIMOES","emailPrincipal": "paulafigueiredo.ped@gmail.com","telefonePrincipal": "(21)980235924","codigo": "50564","campopersonalizado_1_compl_cont": "50564","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-P-37","campopersonalizado_190_compl_proc": "44574","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "PAULA MARQUES PRATES BEHRENS","emailPrincipal": "behrens.paula@gmail.com","telefonePrincipal": "(51)999665778","codigo": "41183","campopersonalizado_1_compl_cont": "41183","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "43935","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "PAULO OLDERS SPILIMBERGO","emailPrincipal": "paulo.spilimbergo@gmail.com","telefonePrincipal": "(51)996261901","codigo": "37349","campopersonalizado_1_compl_cont": "37349","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-18","campopersonalizado_190_compl_proc": "44440","campopersonalizado_191_compl_proc": "Férias","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "PAULO RICARDO LOPES SENA","emailPrincipal": "paulolsena@gmail.com","telefonePrincipal": "(51)99196-6451","codigo": "36937","campopersonalizado_1_compl_cont": "36937","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "44501","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "RAFAEL BACK SCHUMACHER","emailPrincipal": "rafaa020@gmail.com","telefonePrincipal": "(51)989021749","codigo": "42925","campopersonalizado_1_compl_cont": "42925","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CR-5","campopersonalizado_190_compl_proc": "45413","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JUCARA GASPARETTO MACCARI","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "RENATA FREITAS TEIXEIRA","emailPrincipal": "renataneo@terra.com.br","telefonePrincipal": "(51)99192044","codigo": "25519","campopersonalizado_1_compl_cont": "25519","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-UTI-NEO-51","campopersonalizado_190_compl_proc": "41548","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "DESIREE DE FREITAS VALLE VOLKMER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "ROBERTO JACKSON DA SILVA NUNES JUNIOR","emailPrincipal": "bibliotecarob@gmail.com","telefonePrincipal": "(65)992211781","codigo": "47401","campopersonalizado_1_compl_cont": "47401","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "45602","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "RODRIGO MEIRELLES BORBA","emailPrincipal": "","telefonePrincipal": "(51)99636345","codigo": "33447","campopersonalizado_1_compl_cont": "33447","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-EME-A-18","campopersonalizado_190_compl_proc": "42954","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "RODRIGO WILTGEN JEFFMAN","emailPrincipal": "rodrigojeffman@gmail.com","telefonePrincipal": "(51)999698834","codigo": "51519","campopersonalizado_1_compl_cont": "51519","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-18","campopersonalizado_190_compl_proc": "45413","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "STEPHANIE BONEIRA PRETTO","emailPrincipal": "stepretto92@gmail.com","telefonePrincipal": "(53)981133798","codigo": "44699","campopersonalizado_1_compl_cont": "44699","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "45036","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "VICTOR COSTA RIBEIRO","emailPrincipal": "vcribeiro11@gmail.com","telefonePrincipal": "(53)99569096","codigo": "48979","campopersonalizado_1_compl_cont": "48979","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-18","campopersonalizado_190_compl_proc": "45691","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "VICTORIA BERNARDES GUIMARAES","emailPrincipal": "vicbguimaraes@gmail.com","telefonePrincipal": "(51)997668349","codigo": "44216","campopersonalizado_1_compl_cont": "44216","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "44987","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "VIVIANE GEHLEN","emailPrincipal": "","telefonePrincipal": "(51)993422143","codigo": "35972","campopersonalizado_1_compl_cont": "35972","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CR-18","campopersonalizado_190_compl_proc": "43619","campopersonalizado_191_compl_proc": "Férias","campopersonalizado_192_compl_proc": "ARTUR PACHECO SEABRA","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "ALINE SPIAZZI","emailPrincipal": "alinespiazzi1@gmail.com","telefonePrincipal": "(54)991720502","codigo": "47281","campopersonalizado_1_compl_cont": "47281","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-UTI-P-51","campopersonalizado_190_compl_proc": "45785","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "DIANE ALICIA TORMES","emailPrincipal": "dianetormes@gmail.com","telefonePrincipal": "(51)991052666","codigo": "38232","campopersonalizado_1_compl_cont": "38232","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-31","campopersonalizado_190_compl_proc": "43556","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "ISADORA FIORENZA SNOVARESKI","emailPrincipal": "isadorasnovareski@gmail.com","telefonePrincipal": "(55)999618682","codigo": "45431","campopersonalizado_1_compl_cont": "45431","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "45876","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "JANAINA ELSING","emailPrincipal": "","telefonePrincipal": "(51)996111902","codigo": "39805","campopersonalizado_1_compl_cont": "39805","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "43770","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "JULIA KOWACS BUTZKE","emailPrincipal": "juliakowacs@icloud.com","telefonePrincipal": "(51)996762077","codigo": "48883","campopersonalizado_1_compl_cont": "48883","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-MAT-26","campopersonalizado_190_compl_proc": "45628","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "EDSON VIEIRA DA CUNHA FILHO","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "LARISSA HANSEN MARCONDES","emailPrincipal": "larissahmarcondes@gmail.com","telefonePrincipal": "(41)988278201","codigo": "46415","campopersonalizado_1_compl_cont": "46415","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-MAT-26","campopersonalizado_190_compl_proc": "45446","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "EDSON VIEIRA DA CUNHA FILHO","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "LETICIA ANTONIUK SEUS","emailPrincipal": "leticiaantoniuk@gmail.com","telefonePrincipal": "(51)991063626","codigo": "15670","campopersonalizado_1_compl_cont": "15670","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "45769","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "LISIANE MACHADO","emailPrincipal": "","telefonePrincipal": "","codigo": "28181","campopersonalizado_1_compl_cont": "28181","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-CR-51","campopersonalizado_190_compl_proc": "40112","campopersonalizado_191_compl_proc": "Auxílio Doença","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "LIVIA MASO BENVENUTTI","emailPrincipal": "liviambenvenutti@gmail.com","telefonePrincipal": "(51)999974747","codigo": "33665","campopersonalizado_1_compl_cont": "33665","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-EME-A-18","campopersonalizado_190_compl_proc": "40956","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "LUAN SOLEI FLORES CANTEIRO","emailPrincipal": "soleiluan@gmail.com","telefonePrincipal": "(67)991814350","codigo": "11586","campopersonalizado_1_compl_cont": "11586","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-31","campopersonalizado_190_compl_proc": "45597","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "LUCIA HELENA SIEBEN MARTINS","emailPrincipal": "luciahsmartins63@gmail.com","telefonePrincipal": "(51)33812266","codigo": "16394","campopersonalizado_1_compl_cont": "16394","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-CR-51","campopersonalizado_190_compl_proc": "33891","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "LUCIA ROSSELL NICOLOSO","emailPrincipal": "","telefonePrincipal": "(51)91040426","codigo": "24302","campopersonalizado_1_compl_cont": "24302","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-UTI-NEO-51","campopersonalizado_190_compl_proc": "40627","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "DESIREE DE FREITAS VALLE VOLKMER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "LUCIANA SAVI TUMELERO SANTIAGO DA CUNHA","emailPrincipal": "luciana.s.tumelero@gmail.com","telefonePrincipal": "(51)996788882","codigo": "35438","campopersonalizado_1_compl_cont": "35438","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "44564","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "LUIZ CARLOS MARQUES PALLARES","emailPrincipal": "","telefonePrincipal": "","codigo": "8737","campopersonalizado_1_compl_cont": "8737","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-EME-A-18","campopersonalizado_190_compl_proc": "43640","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "LUIZ FERNANDO SOARES VARELA","emailPrincipal": "","telefonePrincipal": "(51)991855871","codigo": "32171","campopersonalizado_1_compl_cont": "32171","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-EME-A-31","campopersonalizado_190_compl_proc": "41179","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "LUIZA MACHADO KOBE","emailPrincipal": "luizakobe@hotmail.com","telefonePrincipal": "(51)992071041","codigo": "43028","campopersonalizado_1_compl_cont": "43028","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-MAT-5","campopersonalizado_190_compl_proc": "45446","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "EDSON VIEIRA DA CUNHA FILHO","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "MAIRA LUCILIA MONTEIRO FERREIRA","emailPrincipal": "marylumf@gmail.com","telefonePrincipal": "(31)985825551","codigo": "59500","campopersonalizado_1_compl_cont": "59500","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "45771","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "MARCELO MENEGOTTO DONADEL","emailPrincipal": "menegottomarcelo@gmail.com","telefonePrincipal": "(51)30287799","codigo": "31815","campopersonalizado_1_compl_cont": "31815","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-31","campopersonalizado_190_compl_proc": "41470","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "MARIA LUISA BARRUFI ADIB","emailPrincipal": "dramarialuisaadib@gmail.com","telefonePrincipal": "(51)993097073","codigo": "39739","campopersonalizado_1_compl_cont": "39739","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-31","campopersonalizado_190_compl_proc": "43892","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "MARIANA GONZALEZ DE OLIVEIRA","emailPrincipal": "mariana.oliveira@hmv.org.br","telefonePrincipal": "(51)991148421","codigo": "26142","campopersonalizado_1_compl_cont": "26142","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-UTI-NEO-51","campopersonalizado_190_compl_proc": "40330","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "DESIREE DE FREITAS VALLE VOLKMER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "MARIANA PESSINI","emailPrincipal": "marianapessini@hotmail.com","telefonePrincipal": "(54)999051592","codigo": "51507","campopersonalizado_1_compl_cont": "51507","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-31","campopersonalizado_190_compl_proc": "45597","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "MARIO SALIM KALIL","emailPrincipal": "mariosalimkalil@gmail.com","telefonePrincipal": "(51)999422306","codigo": "44289","campopersonalizado_1_compl_cont": "44289","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-MAT-26","campopersonalizado_190_compl_proc": "45446","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "EDSON VIEIRA DA CUNHA FILHO","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "MATHEUS DE SOUZA NICHES","emailPrincipal": "matheusniches@gmail.com","telefonePrincipal": "(51)982006424","codigo": "53873","campopersonalizado_1_compl_cont": "53873","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CR-18","campopersonalizado_190_compl_proc": "45743","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JUCARA GASPARETTO MACCARI","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "MATHEUS PRESA BARBIERI","emailPrincipal": "","telefonePrincipal": "","codigo": "48969","campopersonalizado_1_compl_cont": "48969","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-EME-A-18","campopersonalizado_190_compl_proc": "45057","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "MICHELLE TOSCAN","emailPrincipal": "","telefonePrincipal": "","codigo": "46265","campopersonalizado_1_compl_cont": "46265","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-UTI-P-51","campopersonalizado_190_compl_proc": "45817","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "MONICA FRANZOI MARCON","emailPrincipal": "monica_marcon@hotmail.com","telefonePrincipal": "(54)999251842","codigo": "43024","campopersonalizado_1_compl_cont": "43024","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-UTI-P-51","campopersonalizado_190_compl_proc": "44595","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "NATALIA BENDER FUHR","emailPrincipal": "natalia.fuhrb@gmail.com","telefonePrincipal": "(51)991831993","codigo": "48648","campopersonalizado_1_compl_cont": "48648","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-31","campopersonalizado_190_compl_proc": "45110","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "NATHAN HERMENEGILDO LISBOA","emailPrincipal": "nathanlisboa@gmail.com","telefonePrincipal": "(51)982760049","codigo": "44509","campopersonalizado_1_compl_cont": "44509","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-EME-A-31","campopersonalizado_190_compl_proc": "44991","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "NICOLE BERTHIER ZANIN","emailPrincipal": "nikazanin@gmail.com","telefonePrincipal": "(51)997734453","codigo": "36564","campopersonalizado_1_compl_cont": "36564","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "44963","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "PATRICIA DE GODOY MARTINS IMSEIS","emailPrincipal": "","telefonePrincipal": "(51)999890926","codigo": "21988","campopersonalizado_1_compl_cont": "21988","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-UTI-NEO-51","campopersonalizado_190_compl_proc": "40602","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "DESIREE DE FREITAS VALLE VOLKMER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "PAULA PITTA PINHEIRO","emailPrincipal": "paulappitta@gmail.com","telefonePrincipal": "(51)999029932","codigo": "35788","campopersonalizado_1_compl_cont": "35788","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-UTI-P-51","campopersonalizado_190_compl_proc": "45113","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "RODOLFO TOME SOVERAL","emailPrincipal": "RTSOVERAL@GMAIL.COM","telefonePrincipal": "(51)997755592","codigo": "45451","campopersonalizado_1_compl_cont": "45451","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "44669","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "RODRIGO DALCANALLE GARCIA","emailPrincipal": "g-rodrigo@hotmail.com","telefonePrincipal": "(51)983176054","codigo": "47446","campopersonalizado_1_compl_cont": "47446","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "45769","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "ROSIRENE MARIA FROHLICH DALL AGNESE","emailPrincipal": "rosimfda@gmail.com","telefonePrincipal": "(51)992727635","codigo": "34717","campopersonalizado_1_compl_cont": "34717","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-UTI-P-51","campopersonalizado_190_compl_proc": "45113","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "SIBELLE GRATSCH","emailPrincipal": "","telefonePrincipal": "(51)32258474","codigo": "21555","campopersonalizado_1_compl_cont": "21555","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-EME-A-32","campopersonalizado_190_compl_proc": "41193","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "TALIS HAAS","emailPrincipal": "","telefonePrincipal": "","codigo": "39325","campopersonalizado_1_compl_cont": "39325","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-18","campopersonalizado_190_compl_proc": "43944","campopersonalizado_191_compl_proc": "Licença Maternidade","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "VINICIUS EDUARDO DO N DE LEMOS CAMPOS","emailPrincipal": "vinieducampos@gmail.com","telefonePrincipal": "(51)996191011","codigo": "40580","campopersonalizado_1_compl_cont": "40580","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-EME-A-23","campopersonalizado_190_compl_proc": "44138","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "ALESSANDRA WANDERLEY TOBARU","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "WILLIAM SILVA DA SILVA","emailPrincipal": "williamsilvamed@gmail.com","telefonePrincipal": "(51)997010620","codigo": "49952","campopersonalizado_1_compl_cont": "49952","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CTI-A-37","campopersonalizado_190_compl_proc": "45848","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "GREGORY SARAIVA MEDEIROS","campopersonalizado_193_compl_proc": "NÃO"},
# {"nome": "YURI CARLOTTO RAMIRES","emailPrincipal": "yuri.ramires@gmail.com","telefonePrincipal": "(53)991584247","codigo": "48949","campopersonalizado_1_compl_cont": "48949","campopersonalizado_52_compl_cont": "MEDICO PLANTONISTA","codOferta": "CLT-CR-18","campopersonalizado_190_compl_proc": "45848","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JUCARA GASPARETTO MACCARI","campopersonalizado_193_compl_proc": "NÃO"},
# Envio individual
# {"nome": "EVANDRO FREDDY MULINARI","emailPrincipal": "evandro.mulinari@gmail.com","telefonePrincipal": "(51)991120363","codigo": "23411","campopersonalizado_1_compl_cont": "23411","campopersonalizado_52_compl_cont": "MEDICO ROT UNID INT HOSPI","codOferta": "CLT-EME-P-51","campopersonalizado_190_compl_proc": "40371","campopersonalizado_191_compl_proc": "Ativo","campopersonalizado_192_compl_proc": "JOAO RONALDO MAFALDA KRAUZER","campopersonalizado_193_compl_proc": "SIM"},
]

# Lista de privilégios
privilegios = [
    # CLT-CR (Centro de Reabilitação)
    "PRV-CLT-CR-1", "PRV-CLT-CR-2", "PRV-CLT-CR-3", "PRV-CLT-CR-4", "PRV-CLT-CR-5",
    "PRV-CLT-CR-6", "PRV-CLT-CR-7", "PRV-CLT-CR-8", "PRV-CLT-CR-9", "PRV-CLT-CR-10",
    "PRV-CLT-CR-11", "PRV-CLT-CR-12", "PRV-CLT-CR-13", "PRV-CLT-CR-14", "PRV-CLT-CR-15",
    "PRV-CLT-CR-16", "PRV-CLT-CR-17", "PRV-CLT-CR-18", "PRV-CLT-CR-19",
    
    # CLT-CTI-A (CTI Adulto)
    "PRV-CLT-CTI-A-1", "PRV-CLT-CTI-A-2", "PRV-CLT-CTI-A-3", "PRV-CLT-CTI-A-4", "PRV-CLT-CTI-A-5",
    "PRV-CLT-CTI-A-6", "PRV-CLT-CTI-A-7", "PRV-CLT-CTI-A-8", "PRV-CLT-CTI-A-9", "PRV-CLT-CTI-A-10",
    "PRV-CLT-CTI-A-11", "PRV-CLT-CTI-A-12", "PRV-CLT-CTI-A-13", "PRV-CLT-CTI-A-14", "PRV-CLT-CTI-A-15",
    "PRV-CLT-CTI-A-16", "PRV-CLT-CTI-A-17", "PRV-CLT-CTI-A-18", "PRV-CLT-CTI-A-19", "PRV-CLT-CTI-A-20",
    "PRV-CLT-CTI-A-21", "PRV-CLT-CTI-A-22", "PRV-CLT-CTI-A-23",
    
    # CLT-EME-A (Emergência Adulto)
    "PRV-CLT-EME-A-1", "PRV-CLT-EME-A-2", "PRV-CLT-EME-A-3", "PRV-CLT-EME-A-4", "PRV-CLT-EME-A-5",
    "PRV-CLT-EME-A-6", "PRV-CLT-EME-A-7", "PRV-CLT-EME-A-8", "PRV-CLT-EME-A-9", "PRV-CLT-EME-A-10",
    "PRV-CLT-EME-A-11", "PRV-CLT-EME-A-12", "PRV-CLT-EME-A-13", "PRV-CLT-EME-A-14", "PRV-CLT-EME-A-15",
    "PRV-CLT-EME-A-16", "PRV-CLT-EME-A-17", "PRV-CLT-EME-A-18", "PRV-CLT-EME-A-19", "PRV-CLT-EME-A-20",
    
    # CLT-EME-P (Emergência Pediátrica)
    "PRV-CLT-EME-P-1", "PRV-CLT-EME-P-2", "PRV-CLT-EME-P-3", "PRV-CLT-EME-P-4", "PRV-CLT-EME-P-5",
    "PRV-CLT-EME-P-6", "PRV-CLT-EME-P-7", "PRV-CLT-EME-P-8", "PRV-CLT-EME-P-9", "PRV-CLT-EME-P-10",
    "PRV-CLT-EME-P-11", "PRV-CLT-EME-P-12", "PRV-CLT-EME-P-13", "PRV-CLT-EME-P-14", "PRV-CLT-EME-P-15",
    "PRV-CLT-EME-P-16", "PRV-CLT-EME-P-17", "PRV-CLT-EME-P-18", "PRV-CLT-EME-P-19",
    
    # CLT-MAT (Maternidade)
    "PRV-CLT-MAT-1", "PRV-CLT-MAT-2", "PRV-CLT-MAT-3", "PRV-CLT-MAT-4", "PRV-CLT-MAT-5",
    "PRV-CLT-MAT-6", "PRV-CLT-MAT-7", "PRV-CLT-MAT-8", "PRV-CLT-MAT-13",
    
    # CLT-MAT-ESP (Maternidade Especializada)
    # "PRV-CLT-MAT-ESP-9", "PRV-CLT-MAT-ESP-10", "PRV-CLT-MAT-ESP-11", "PRV-CLT-MAT-ESP-12",
    # "PRV-CLT-MAT-ESP-14", "PRV-CLT-MAT-ESP-15", "PRV-CLT-MAT-ESP-16", "PRV-CLT-MAT-ESP-17",
    # "PRV-CLT-MAT-ESP-18", "PRV-CLT-MAT-ESP-19", "PRV-CLT-MAT-ESP-20", "PRV-CLT-MAT-ESP-21",
    
    # CLT-UTI-NEO (UTI Neonatal)
    "PRV-CLT-UTI-NEO-1", "PRV-CLT-UTI-NEO-2", "PRV-CLT-UTI-NEO-3", "PRV-CLT-UTI-NEO-4", "PRV-CLT-UTI-NEO-5",
    "PRV-CLT-UTI-NEO-6", "PRV-CLT-UTI-NEO-7", "PRV-CLT-UTI-NEO-8", "PRV-CLT-UTI-NEO-9", "PRV-CLT-UTI-NEO-10",
    "PRV-CLT-UTI-NEO-11", "PRV-CLT-UTI-NEO-12", "PRV-CLT-UTI-NEO-13", "PRV-CLT-UTI-NEO-14", "PRV-CLT-UTI-NEO-15",
    "PRV-CLT-UTI-NEO-16", "PRV-CLT-UTI-NEO-17", "PRV-CLT-UTI-NEO-18", "PRV-CLT-UTI-NEO-19", "PRV-CLT-UTI-NEO-20",
    "PRV-CLT-UTI-NEO-21",
    
    # CLT-UTI-P (UTI Pediátrica)
    "PRV-CLT-UTI-P-1", "PRV-CLT-UTI-P-2", "PRV-CLT-UTI-P-3", "PRV-CLT-UTI-P-4", "PRV-CLT-UTI-P-5",
    "PRV-CLT-UTI-P-6", "PRV-CLT-UTI-P-7", "PRV-CLT-UTI-P-8", "PRV-CLT-UTI-P-9", "PRV-CLT-UTI-P-10",
    "PRV-CLT-UTI-P-11", "PRV-CLT-UTI-P-12", "PRV-CLT-UTI-P-13", "PRV-CLT-UTI-P-14", "PRV-CLT-UTI-P-15",
    "PRV-CLT-UTI-P-16", "PRV-CLT-UTI-P-17", "PRV-CLT-UTI-P-18"
]

def formatar_data(data_str):
    """Converte data de m/d/yyyy para yyyy-mm-dd"""
    try:
        data_obj = datetime.strptime(data_str, "%m/%d/%Y")
        return data_obj.strftime("%Y-%m-%d")
    except:
        try:
            data_obj = datetime.strptime(data_str, "%d/%m/%Y")
            return data_obj.strftime("%Y-%m-%d")
        except:
            return data_str

def tratar_campo_logico(valor):
    """Trata campo lógico - SIM = 1, NAO = vazio"""
    if valor.upper() == "SIM":
        return "1"
    else:
        return ""

def filtrar_privilegios(cod_oferta):
    """Filtra privilégios baseado no código da oferta"""
    
    partes = cod_oferta.split("-")
    
    if len(partes) >= 4:
        # Para códigos como CLT-EME-A-5, CLT-CTI-A-1 (ignora o número final)
        padrao = f"PRV-{partes[0]}-{partes[1]}-{partes[2]}-"
    elif len(partes) == 3:
        # Para códigos como CLT-CR-18 (ignora o número final)
        padrao = f"PRV-{partes[0]}-{partes[1]}-"
    else:
        return []
    
    # Filtra privilégios que começam com o padrão exato
    return [p for p in privilegios if p.startswith(padrao)]

def criar_contato(dados_contato):
    """Cria um contato via API"""
    
    # Preparar dados para a requisição
    body = {
        "nome": dados_contato["nome"],
        "emailPrincipal": dados_contato["emailPrincipal"],
        "telefonePrincipal": dados_contato["telefonePrincipal"],
        "codigo": dados_contato["codigo"],
        "camposPersonalizados": {
            "campopersonalizado_1_compl_cont": dados_contato["campopersonalizado_1_compl_cont"],
            "campopersonalizado_52_compl_cont": dados_contato["campopersonalizado_52_compl_cont"]
        },
        "evento": {
            "tipo": "404",
            "codCurso": "2",
            "codOferta": dados_contato["codOferta"],
            "codLocalOferta": "PRV-0",
            "camposPersonalizados": {
                "campopersonalizado_190_compl_proc": formatar_data(dados_contato["campopersonalizado_190_compl_proc"]),
                "campopersonalizado_191_compl_proc": dados_contato["campopersonalizado_191_compl_proc"],
                "campopersonalizado_192_compl_proc": dados_contato["campopersonalizado_192_compl_proc"],
                "campopersonalizado_193_compl_proc": tratar_campo_logico(dados_contato["campopersonalizado_193_compl_proc"])
            }
        },
        "tags": ["Att. Privilégios - 08/2025"],
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
            "campopersonalizado_30_compl_proc": "2025-08-25",
            "campopersonalizado_32_compl_proc": "",
            "campopersonalizado_31_compl_proc": "2026-08-25"
        },
        "codCurso": "2",
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
            "codigo": contato["codigo"],
            "email": contato["emailPrincipal"],
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
            
            # Filtrar privilégios para este contato
            privilegios_filtrados = filtrar_privilegios(contato["codOferta"])
            print(f"Privilegios encontrados: {len(privilegios_filtrados)}")
            
            # Criar eventos para cada privilégio
            for privilegio in privilegios_filtrados:
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
    
    # Console log (mantém como estava)
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
        print(f"\nContato: {detalhe['nome']} (CRM: {detalhe['codigo']})")
        print(f"Email: {detalhe['email']}")
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
        print(f"\nRelatório salvo em: {nome_arquivo}")
    except Exception as e:
        print(f"\nErro ao salvar relatório JSON: {e}")

if __name__ == "__main__":
    print("Iniciando processamento de contatos...")
    relatorio = processar_contatos()
    gerar_relatorio(relatorio)