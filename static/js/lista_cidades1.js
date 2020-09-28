$('#ufnascimento')
    .click(function(){
        $.ajax({
            // type:'GET',
            url:'https://servicodados.ibge.gov.br/api/v1/localidades/estados/' + $(this).val() + '/municipios',
            // contentType: "application/json; charset=utf-8",
            dataType: "json",
            // async:false
        }).done(function(response){
            cidades='';
            $.each(response, function(c, cidade){
                cidades+='<option value="'+cidade.nome+'">'+cidade.nome+'</option>';
            });
            // PREENCHE AS CIDADES DE ACORDO COM O ESTADO
            $('#municipionascimento').html(cidades);
        });
    });