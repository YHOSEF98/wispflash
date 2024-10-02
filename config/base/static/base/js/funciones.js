var urlpath = window.location.pathname

function message_error (obj){
    var html = '';
    if(typeof (obj) === 'object'){
        var html = '<ul style="text-align: left;">';
        $.each(obj, function(key, value){
            html += '<li>'+key+':'+value+'</li>';
        })
        html += '</ul>';
    }
    else{
        html += '<p>'+obj+'</p>';
    }
    Swal.fire({
        title: 'Error!',
        html: html,
        icon: 'error'
    });
}

function submit_with_ajax(url, parameters, callback){
    $.confirm({
        theme: 'material',
        title: 'Confirmacion',
        icon: 'fa fa-info',
        content: '¿Estás seguro de realizar esta accion?',
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        url: url, //window.location.pathname
                        type: 'POST',
                        data: parameters,
                        dataType: 'json'
                    }).done(function (data) {
                        console.log(data);
                        if (!data.hasOwnProperty('error')) {
                            callback();
                        } else {
                            message_error(data.error);
                        }
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    }).always(function (data) {

                    });
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    })
}

function envio_withajax(parameters, content, urlpathlist){
    $.confirm({
        theme: 'material',
        title: 'Confirmación!',
        icon: 'fa fa-info',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function (){
                    $.ajax({
                        url: urlpath,
                        type: 'POST',
                        data: parameters,
                        dataType: 'json',
                        processData: false,
                        contentType: false
                    }).done(function(data){
                        if(!data.hasOwnProperty('error')){
                            window.location.href = urlpathlist;
                        } else {
                            message_error(data.error);
                        }
                    }).fail(function(jqXHR, textStatus, errorThrown){
                        alert(textStatus + ':'+ errorThrown);
                    }).always(function(data){
        
                    })
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    })
}

function alert_action(title, content, callback){
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function (){
                    callback()
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    })
}

function campos_tipo_servicio(elements){
        var selectField = $('select[name="tiposervicio"]');
        
        function updateFields(option) {
            switch (option) {
                case "IP estatica":
                    elements.ipddres.style.display = 'block';
                    elements.idperfilpppoe.style.display = 'none';
                    elements.labelperfilpppoe.style.display = 'none';
                    elements.idpasswordppp.style.display = 'none';
                    elements.labelpasswordppp.style.display = 'none';
                    elements.ipuserppp.style.display = 'none';
                    elements.labeluserpp.style.display = 'none';
                    break;
                case "PPPoE":
                    elements.idperfilpppoe.style.display = 'block';
                    elements.idperfilpppoe.required = true;
                    elements.labelperfilpppoe.style.display = 'block';
                    elements.idpasswordppp.style.display = 'block';
                    elements.labelpasswordppp.style.display = 'block';
                    elements.idpasswordppp.required = true;
                    elements.ipuserppp.style.display = 'block';
                    elements.labeluserpp.style.display = 'block';
                    elements.ipuserppp.required = true;
                    elements.ipddres.style.display = 'none';
                    break;
                default:
                    elements.idperfilpppoe.style.display = 'none';
                    elements.labelperfilpppoe.style.display = 'none';
                    elements.idpasswordppp.style.display = 'none';
                    elements.labelpasswordppp.style.display = 'none';
                    elements.ipuserppp.style.display = 'none';
                    elements.labeluserpp.style.display = 'none';
                    elements.ipddres.style.display = 'none';
                    break;
            }
        }
        updateFields(selectField.val());
        
        selectField.on('change', function() {
            updateFields($(this).val());
        });
    }