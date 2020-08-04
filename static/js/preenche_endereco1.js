$('#cep1')
    .focusout(function(){
        //Início do Comando AJAX
        $.ajax({
            //O campo URL diz o caminho de onde virá os dados
            url: 'https://viacep.com.br/ws/' + $(this).val() + '/json/',
            //tipo de dados que será lido, no caso JSON.
            dataType: 'jsonp',
            //SUCESS é referente a função que será executada caso a fonte de dados seja lida com sucesso.
            success: function(resposta){
                // Retorno da função SUCESS
                if(!resposta.erro){
                    $("#logradouro1").val(resposta.logradouro);
                    $("#complemento1").val(resposta.complemento);
                    $("#bairro1").val(resposta.bairro);
                    $("#cidade1").val(resposta.localidade);
                    $("#uf1").val(resposta.uf);
                } else{
                    alert("CEP INVÁLIDO");
                    $("#logradouro1").val('');
                    $("#complemento1").val('');
                    $("#bairro1").val('');
                    $("#cidade1").val('');
                    $("#uf1").val('');
                }
                // $("#numero").focus();
            },
            error: function() {
                alert("CEP INVÁLIDO");
                $("#logradouro1").val('');
                $("#complemento1").val('');
                $("#bairro1").val('');
                $("#cidade1").val('');
                $("#uf1").val('');
            }
        });
    });