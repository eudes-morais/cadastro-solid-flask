// Cria a relação dos CNAEs de acordo com o site do IBGE através de uma API
// https://servicodados.ibge.gov.br/api/v2/cnae/subclasses (vide o site do IBGE)
function listaCnae(){
    //Início do Comando AJAX
    $.ajax({
        // type:'GET',
        url:'https://servicodados.ibge.gov.br/api/v2/cnae/subclasses',
        // contentType: "application/json; charset=utf-8",
        dataType: "json",
        // async:false
    }).done(function(response){
        cnaes='';
        $.each(response, function(cn, cnae){
            cnaes+='<option value="'+cnae.id+'">'+cnae.id+' - '+cnae.descricao+'</option>';
        });
        // PREENCHE AS CIDADES DE ACORDO COM O ESTADO
        $('#cnae').html(cnaes);
    });
}

listaCnae();