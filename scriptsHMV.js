/**
 * Script da página atualização de RQE do HMV
 */

// Mudança

function iniciar() {
    RBLib.config({
      urlBase: "https://crmhmv.apprubeus.com.br",
      urlFicha: "https://hmv.apprbs.com.br",
      token: "d2cc15f39418956cd23eca96b49681ec",
      origem: "9",
      linkPortal: "/atualizacao-rqe",
      pagina: "pagina-personalizada"
    });
  
    setTimeout(() => {
      verificaLogin();
      preencherCampo();
      garantirDesabilitarCamposSelect(camposParaDesabilitar);
      atualizarTextoOpcaoNula()
      atualizarPlaceholderInput()
      // desabilitarCampoSelect();
    }, 500);
  
    setTimeout(() => {
      adicionarTexto();
      preencherCampos(idContato, idRegistro);
      // desabilitarCampoSelect();
    }, 1500);
  
    callback();
  }
  
  let idRegistro = '';
  let idContato = ''
  
  function verificaLogin() {
    let contato = JSON.parse(localStorage.getItem("contato"));
    if (contato) {
      idContato = contato.id;
      var objPessoa = RBLib.api.buscarContato({ id: idContato }, "", "local", false);
    } else {
      urlParams = new URLSearchParams(window.location.search);
      idContato = urlParams.get("idContato");
      var objPessoa = RBLib.api.buscarContato({ id: idContato }, "", "local", false);
    }
  
    if (objPessoa) {
      RBLib.form.preencherCampos(objPessoa, "", "", "");
      RBLib.api.buscarRegistros({ id: idContato }, "", "local", false);
      campo = document.getElementsByName("pessoa.nome")[0];
  
      campo.onblur();
  
    } else {
      console.log("Não achou pessoa");
      window.location.href = "https://hmv.apprbs.com.br/atualizacao-rqe-login";
      localStorage.clear();
    }
  }
  
  /* Preenche o campo configurado */
  function preencherCampo() {
      let campo = document.querySelector('[name="evento.codOferta"]');
  
      if (campo && Array.from(campo.options).length > 1) {
          let todosRegistros = localStorage.getItem('registros');
          let intervalRegistros = setInterval(() => {
              if (todosRegistros != null) {
                  clearInterval(intervalRegistros);
                  let registroEncontrado = JSON.parse(todosRegistros).find(registro => ["1", "2", "6"].includes(registro.processo));
                  if (registroEncontrado) {
                      idRegistro = registroEncontrado.id;
                      idContato = registroEncontrado.pessoaPrincipal;
                      campo.value = registroEncontrado.curso;
                      campo.dispatchEvent(new Event('change'));
  
                      preencherCampos(idContato, idRegistro); // Chama preencherCampos com as variáveis
                      garantirDesabilitarCamposSelect(camposParaDesabilitar); // Desabilita os campos logo após preenchê-los
  
                  }
              } else {
                  todosRegistros = localStorage.getItem('registros');
              }
          }, 300);
      } else {
          setTimeout(preencherCampo, 500);
      }
  }
  
  function preencherCampos(idContato, idRegistro){
    let objPessoa = RBLib.api.buscarContato({ id: idContato }, callback, "local", false);
    let registros = RBLib.api.buscarRegistros({ id: idContato }, callback, "", false);
    let registroSelecionado;
    if (registros.success) {
      registroSelecionado = registros.dados.find((registro) => registro.id == idRegistro);
      registroSelecionado = { dados: registroSelecionado };
    }
  
    RBLib.form.preencherCampos(objPessoa, registroSelecionado.dados, callback, false);
  }
  
  function adicionarTexto() {
    // Seleciona o elemento com a classe 'col s12 rbPadding10 rbLgpdContainer'
    var elementoAlvo = document.querySelector('.col.s12.rbPadding10.rbLgpdContainer');
  
    // Verifica se o elemento existe
    if (elementoAlvo) {
      // Cria um novo elemento <p>
      var novoTexto = document.createElement("p");
  
      // Define o HTML do novo elemento com um link
      novoTexto.innerHTML = "Caso deseje atualizar a suas especialidades ou áreas de atuação, entre em contato com a equipe de Relacionamento com o Corpo Clínico através do número: +55 51 9678-4713 ou do e-mail: <a href='mailto:relacionamento.corpoclinico@hmv.org.br' style='color: #a0a0a0; font-style: italic; font-size: 14px;'>relacionamento.corpoclinico@hmv.org.br</a>. Obrigado!";
  
      // Define o estilo do novo elemento
      novoTexto.style.color = "#a0a0a0";
      novoTexto.style.fontStyle = "italic";
      novoTexto.style.fontSize = "14px";
  
      // Adiciona o novo elemento dentro do elemento alvo
      elementoAlvo.appendChild(novoTexto);
    } else {
      console.log("Elemento não encontrado.");
    }
  }
  
  function desabilitarCamposSelect(seletores) {
    let todosDesabilitados = true;
  
    seletores.forEach(seletor => {
      // Seleciona o campo select pelo nome
      var campoSelect = document.querySelector(seletor);
  
      // Verifica se o campo existe e se ainda não está desabilitado
      if (campoSelect && !campoSelect.disabled) {
        // Desabilita o campo select
        campoSelect.disabled = true;
        console.log(`Campo select (${seletor}) desabilitado.`);
      } else if (campoSelect && campoSelect.disabled) {
        // Campo já desabilitado
        console.log(`Campo select (${seletor}) já estava desabilitado.`);
      } else {
        console.log(`Campo select (${seletor}) não encontrado.`);
        todosDesabilitados = false;
      }
    });
  
    return todosDesabilitados;
  }
  
  // Função que chama desabilitarCamposSelect em intervalos de 500ms até que todos os campos sejam desabilitados
  function garantirDesabilitarCamposSelect(seletores) {
    var intervalo = setInterval(() => {
      if (desabilitarCamposSelect(seletores)) {
        clearInterval(intervalo); // Para o intervalo quando todos os campos são desabilitados
      }
    }, 500);
  }
  
  // Lista de seletores de campos que você quer desabilitar
  var camposParaDesabilitar = [
    'select[name="evento.codOferta"]',
    'input[name="processo.camposPersonalizados.campopersonalizado_12_compl_proc"]',
    'input[name="processo.camposPersonalizados.campopersonalizado_13_compl_proc"]',
    'select[name="processo.camposPersonalizados.campopersonalizado_175_compl_proc"]',
    'select[name="processo.camposPersonalizados.campopersonalizado_176_compl_proc"]',
    'select[name="processo.camposPersonalizados.campopersonalizado_177_compl_proc"]'
  ];
  
  const selectElements = document.querySelectorAll('.rb-form-field-select.col.s12');
  
  // Função para atualizar o texto da opção "null"
  function atualizarTextoOpcaoNula() {
      selectElements.forEach(selectElement => {
          const options = selectElement.options;
          for (let i = 0; i < options.length; i++) {
              if (options[i].value === "null") {
                  options[i].text = "- - -";
                  break;
              }
          }
      });
  }
  
  // Função para atualizar o placeholder dos campos input
  function atualizarPlaceholderInput() {
      const inputs = document.querySelectorAll('input[name="processo.camposPersonalizados.campopersonalizado_12_compl_proc"], input[name="processo.camposPersonalizados.campopersonalizado_13_compl_proc"]');
      
      inputs.forEach(input => {
          if (!input.value) {
              input.placeholder = "- - -";
          }
      });
  }
  
  function callback() {
    console.log("terminou");
  }
  