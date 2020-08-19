// $('#municipio')
//     .click(function(){
//         $.ajax({
//             // type:'GET',
//             url:'https://servicodados.ibge.gov.br/api/v1/localidades/estados/' + $(this).val() + '/municipios',
//             // contentType: "application/json; charset=utf-8",
//             dataType: "json",
//             // async:false
//         }).done(function(response){
//             cidades='';
//             $.each(response, function(c, cidade){
//                 cidades+='<option value="'+cidade.nome+'">'+cidade.nome+'</option>';
//             });
//             // PREENCHE AS CIDADES DE ACORDO COM O ESTADO
//             $('#municipio').html(cidades);
//         });
//     });

// $('#municipio').focus();
// $('#municipio').autocomplete({
//     source: function(request, response) {
//         $.getJSON("https://servicodados.ibge.gov.br/api/v1/localidades/municipios",{query:request.term},response);
//     },
//     minLength: 1,
//     select: function(event, ui) {            

//         //var url = ui.item.value;
//         //location.href = url;
//     },
// });

$(function(){
    $("#tags").autocomplete({
      source: function( request, response ) {
        $.ajax({
          url: "https://servicodados.ibge.gov.br/api/v1/localidades/municipios",
          type: "POST",
          dataType: "json",
          data: {term: request.term},
          success: function(data) {
            response(data);
          }
        });
      } 
    });
  });