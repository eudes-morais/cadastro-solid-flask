<<<<<<< HEAD
$("#cep")
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
                    $("#logradouro").val(resposta.logradouro);
                    $("#complemento").val(resposta.complemento);
                    $("#bairro").val(resposta.bairro);
                    $("#cidade").val(resposta.localidade);
                    $("#uf").val(resposta.uf);
                } else{
                    alert("CEP INVÁLIDO");
                    $("#logradouro").val('');
                    $("#complemento").val('');
                    $("#bairro").val('');
                    $("#cidade").val('');
                    $("#uf").val('');
                }
                // $("#numero").focus();
            },
            error: function() {
=======
$("#cep").focusout(function(){
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
                $("#logradouro").val(resposta.logradouro);
                $("#complemento").val(resposta.complemento);
                $("#bairro").val(resposta.bairro);
                $("#cidade").val(resposta.localidade);
                $("#uf").val(resposta.uf);
            } else{
>>>>>>> 1040a0e5fae20b9267a570f7fa7a715388333e3c
                alert("CEP INVÁLIDO");
                $("#logradouro").val('');
                $("#complemento").val('');
                $("#bairro").val('');
                $("#cidade").val('');
                $("#uf").val('');
            }
<<<<<<< HEAD
        });
    });
=======
            // $("#numero").focus();
        },
        error: function() {
            alert("CEP INVÁLIDO");
            $("#logradouro").val('');
            $("#complemento").val('');
            $("#bairro").val('');
            $("#cidade").val('');
            $("#uf").val('');
        }
    });
});
>>>>>>> 1040a0e5fae20b9267a570f7fa7a715388333e3c
