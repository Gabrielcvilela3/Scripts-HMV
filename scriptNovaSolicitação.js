function iniciar() {
  RBLib.config({
    urlBase: 'https://crmhmv.apprubeus.com.br',
    urlFicha: "https://hmv.apprbs.com.br",
    token: '8fb190af131b7724404f1d4156384705',
    origem: '53',
    pagina: "nova-solicitacao",
    modulos: [
      {
        modulo: "solicitacao",
        versao: '2.1.0', // '3.0.1',
        url: 'https://sitesrubeus.com.br/rblib/solicitacao/',
        // url: 'https://repositoriosjs.apprbs.com.br/rblib/',
        configs: {
          campoRegistroVinculado: 'campopersonalizado_115_compl_proc'
        }
      },
    ],
  });

   setTimeout(preencherCampo,500);
   setTimeout(preencherCampos, 1000);
   setTimeout(toggleFields, 2000);
}

// function preencherCampos() {
//   const params = new URLSearchParams(document.location.search);
//   let idRegistro = params.get("idRegistro");

//   let registro = RBLib.api.buscarRegistroDados({id: idRegistro}, "", "", "");
//   if(!registro || !registro.success){
//     console.log("REGISTRO NÃO ENCONTRADO, PREENCHIMENTO DESATIVADO.");
//     return;
//   }

//   RBLib.form.preencherCampos({}, registro.dados, null, null);
//   console.log("Campos preenchidos com sucesso!");
// }

function preencherCampos() {
  // const url = document.location.pathname;
  // const pathSegments = url.split("/");
  // let idRegistro = pathSegments[pathSegments.length - 1]; // Último segmento do caminho da URL



  const params = new URLSearchParams(document.location.search);
  let idRegistro = params.get("idRegistro");
  let idPessoa = params.get("idPessoa");
  let idOferta = params.get("idOferta");

  let pessoaDados = RBLib.api.buscarPessoaDados(
    {
      id: idPessoa,
      retornarProcessos: "1",
      pessoasRelacionadasNoRegistro: "1",
      bloquearPessoasRelacionadas: "1",
    },
    null,
    "local",
    false
  );

  const oportunidadeEncontrada = pessoaDados.dados.processos
      .flatMap(processo => processo.oportunidades || []) // Garante um array plano de oportunidades
      .find(oportunidade => oportunidade.id == idRegistro);

  console.log(oportunidadeEncontrada);

  RBLib.form.preencherCampos("", oportunidadeEncontrada, () => console.log("preencheu campos"), false);
  console.log("Campos preenchidos com sucesso!");

  if(idOferta) {
    let campoIdRegistroVinculado = document.getElementsByName("processo.camposPersonalizados.campopersonalizado_166_compl_proc")[0];
    campoIdRegistroVinculado.value = idOferta;
    campoIdRegistroVinculado.oninput();
    campoIdRegistroVinculado.onkeyup();
  }

  // let registro = RBLib.api.buscarRegistroDados({id: idRegistro}, "", "", "");
  // if (!registro || !registro.success) {
  //   console.log("REGISTRO NÃO ENCONTRADO, PREENCHIMENTO DESATIVADO.");
  //   return;
  // }

  // RBLib.form.preencherCampos({}, registro.dados, null, null);
}

//Oculta e exibe campos dependendo dos valores nos campos "codOferta" e "modalidade"
function toggleFields() {
    var codOfertaField = document.querySelector('[name="evento.codOferta"]');
    var modalidadeField = document.querySelector('[name="evento.modalidade"]');

    var codOferta = codOfertaField.options[codOfertaField.selectedIndex].textContent;
    var modalidade = modalidadeField.options[modalidadeField.selectedIndex].textContent;

    var fieldsToHide = [
        "processo.camposPersonalizados.campopersonalizado_11_compl_proc",
        "processo.camposPersonalizados.campopersonalizado_168_compl_proc",
        "processo.camposPersonalizados.campopersonalizado_172_compl_proc",
        "processo.camposPersonalizados.campopersonalizado_12_compl_proc",
        "processo.camposPersonalizados.campopersonalizado_170_compl_proc",
        "processo.camposPersonalizados.campopersonalizado_13_compl_proc",
        "processo.camposPersonalizados.campopersonalizado_171_compl_proc",
        "processo.camposPersonalizados.campopersonalizado_176_compl_proc",
        "processo.camposPersonalizados.campopersonalizado_173_compl_proc",
        "processo.camposPersonalizados.campopersonalizado_177_compl_proc",
        "processo.camposPersonalizados.campopersonalizado_174_compl_proc",
        "processo.camposPersonalizados.campopersonalizado_109_compl_proc",
        "processo.camposPersonalizados.campopersonalizado_110_compl_proc",
        "processo.camposPersonalizados.campopersonalizado_27_compl_proc",
        "processo.camposPersonalizados.campopersonalizado_131_compl_proc",
        "processo.camposPersonalizados.campopersonalizado_14_compl_proc"
    ];

    fieldsToHide.forEach(function(name) {
        var field = document.querySelector('[name="' + name + '"]');
        var container = field.closest('.rb-content-form.col.s12');

        if (container) {
            if (codOferta === "Validação de documentos") {
                container.style.display = "block";
            } else {
                container.style.display = "none";
            }
        }
    });

    var additionalFieldsToShow = [
        "processo.camposPersonalizados.campopersonalizado_109_compl_proc",
        "processo.camposPersonalizados.campopersonalizado_110_compl_proc",
        "processo.camposPersonalizados.campopersonalizado_131_compl_proc"
    ];

    additionalFieldsToShow.forEach(function(name) {
        var field = document.querySelector('[name="' + name + '"]');
        var container = field.closest('.rb-content-form.col.s12');

        if (container) {
            if (codOferta === "Validação de documentos" && (modalidade === "Liberação Especial" || modalidade === "Liberação Temporária - Apoio / Auxílio")) {
                container.style.display = "block";
            } else {
                container.style.display = "none";
            }
        }
    });
}

document.querySelector('[name="evento.codOferta"]').addEventListener('change', toggleFields);
document.querySelector('[name="evento.modalidade"]').addEventListener('change', toggleFields);

//Preenche o campo específico
function preencherCampo(){
  let campo = document.querySelector('[name="processo.camposPersonalizados.campopersonalizado_166_compl_proc"]');

  // Função para extrair o valor após '/registro/' na URL
  function getValorFromURL() {
    let url = window.location.href;
    let parts = url.split('/');
    let index = parts.indexOf('registro');
    if (index !== -1 && parts.length > index + 1) {
      return parts[index + 1];
    }
    return null;
  }

  let valor = getValorFromURL();

  if(campo && valor){
    campo.value = valor;
    campo.dispatchEvent(new Event('change'));
  } else {
    setTimeout(preencherCampo, 500);
  }
}

function callback() {
  console.log("terminou");
}