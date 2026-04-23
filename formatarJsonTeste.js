// Dados da API externa
const externalData = {
    "status": "OK",
    "content": {
        "data": [
            {
                "teamDoctorsIds": [],
                "isInternalDoctor": false,
                "hidden": false,
                "_id": "66b509bec97560001e3fa13a",
                "name": "ESSE CONTATO NÃO PODE RETORNAR POIS NÃO TEM FOTO",
                "register": "40472",
                "specialties": "NEUROLOGIA",
                "phone": null,
                "cep": null,
                "publicPlace": null,
                "addressNumber": null,
                "addressComplement": null,
                "district": null,
                "city": null,
                "imageUrl": "",
                "haveScheduleOnline": false,
                "haveTelemedicineSchedule": false,
                "mobilePhone": "982898624",
                "createdAt": "2024-08-08T18:09:02.332Z",
                "updatedAt": "2025-01-29T18:09:40.641Z",
                "__v": 0,
                "slug": "abdiel-leite-de-souza-40472"
            },
            {
                "teamDoctorsIds": [],
                "isInternalDoctor": false,
                "hidden": false,
                "_id": "5ee41e705eb75216385665b9",
                "name": "Teste - treinamento solicitações",
                "register": "20983",
                "specialties": "CLINICA MEDICA",
                "phone": "(51) 3211.2766",
                "cep": "90020160",
                "publicPlace": "DOM FELICIANO",
                "addressNumber": "78",
                "addressComplement": "507/508",
                "district": "CENTRO",
                "city": "PORTO ALEGRE",
                "imageUrl": "https://www.hospitalmoinhos.org.br/media/4eea27e3-1c30-497e-9227-f9c9619dc5dd.png",
                "createdAt": "2020-06-13T00:31:44.933Z",
                "updatedAt": "2025-01-29T18:09:54.203Z",
                "__v": 0,
                "slug": "everton-curi-paulo-quadros-20983",
                "haveScheduleOnline": false,
                "haveTelemedicineSchedule": false,
                "seoDescription": {
                    "_id": "633c41065017dc73b243ac11",
                    "pt": " EVERTON CURI PAULO QUADROS",
                    "en": " EVERTON CURI PAULO QUADROS"
                },
                "mobilePhone": "(51) 99998.0672"
            }
        ],
        "totalPages": 4
    }
};

// Lista de CPFs associados aos nomes
const cpfList = [
    { "name": "Teste - treinamento solicitações", "cpf": "5730937334" }
];

// Função para buscar o CPF pelo nome e garantir que tenha 11 dígitos
function getCpfByName(name) {
    const cpfEntry = cpfList.find(entry => entry.name === name);
    if (cpfEntry && cpfEntry.cpf) {
        return cpfEntry.cpf.padStart(11, '0');
    }
    return "";
}

// Função para converter os dados de um contato no formato esperado pela sua API de cadastro
function convertContact(contact) {
    return {
        "nome": contact.name || "",
        "imagemUrl": contact.imageUrl || "",
        "cpf": getCpfByName(contact.name), // Adiciona o CPF correspondente
        "tags": [
            "Foto atribuída"
        ],
        "evento": {
            "tipo": "374"
        },
        "camposPersonalizados": {
            "campopersonalizado_1_compl_cont": contact.register || ""
        },
        "origem": "9",
        "token": "d2cc15f39418956cd23eca96b49681ec"
    };
}

// Filtrar contatos que possuem valor no campo imageUrl e CPF
const filteredContacts = externalData.content.data.filter(contact => contact.imageUrl && contact.imageUrl.trim() !== "" && getCpfByName(contact.name));

// Iterar sobre os dados filtrados e converter cada contato
const convertedDataArray = filteredContacts.map(contact => convertContact(contact));

console.log(JSON.stringify(convertedDataArray, null, 2));
