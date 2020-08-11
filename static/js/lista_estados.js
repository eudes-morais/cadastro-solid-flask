// Função que compara e orderna os estados
function compare(a, b) {
    // Use toUpperCase() to ignore character casing
    const estadoA = a.nome.toUpperCase();
    const estadoB = b.nome.toUpperCase();
  
    let comparison = 0;
    if (estadoA > estadoB) {
      comparison = 1;
    } else if (estadoA < estadoB) {
      comparison = -1;
    }
    return comparison;
 }

function montaCidade(estado){
    //Início do Comando AJAX
    $.ajax({
        // type:'GET',
        url:'https://servicodados.ibge.gov.br/api/v1/localidades/estados/'+estado+'/municipios',
        // contentType: "application/json; charset=utf-8",
        dataType: "json",
        // async:false
    }).done(function(response){
        cidades='';
        $.each(response, function(c, cidade){
            cidades+='<option value="'+cidade.nome+'">'+cidade.nome+'</option>';
        });
        // PREENCHE AS CIDADES DE ACORDO COM O ESTADO
        $('#municipio').html(cidades);
    });
}

function montaUF() {
    //Início do Comando AJAX
    $.ajax({
        //O campo URL diz o caminho de onde virá os dados. Neste caso,
        // foi utilizada a API do IBGE que consome os estados do Brasil
        url: 'http://servicodados.ibge.gov.br/api/v1/localidades/estados',
        //tipo de dados que será lido, no caso JSON.
        dataType: 'json',
        //SUCESS é referente a função que será executada caso a fonte de dados seja lida com sucesso.
        success: function(resposta){
            estados='';
            // Função COMPARE responsável por ordenar os estados
            resposta = resposta.sort(compare);
            $.each(resposta, function(e, estado){
                estados+='<option value="'+estado.id+'">'+estado.nome+'</option>';
            });
            // PREENCHE OS ESTADOS BRASILEIROS
            $("#estado").html(estados);
            // CHAMA A FUNÇÃO QUE PREENCHE AS CIDADES DE ACORDO COM O ESTADO
            montaCidade($('#estado').val());

            // VERIFICA A MUDANÇA NO VALOR DO CAMPO ESTADO E ATUALIZA AS CIDADES
            $('#estado').change(function(){
                montaCidade($('#estado').val());
            });
        }
    });
}

montaUF();