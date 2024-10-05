var tblSale;
$(function() {
    $.ajax({
        url: window.location.pathname, // URL a la que se enviará la solicitud
        type: 'POST', // Método de la solicitud
        data: {
            'action': 'detail_products', // Acción a realizar en el servidor
        },
        dataType: 'json', // Tipo de datos que se espera recibir
    })
    .done(function(data) {
        tblSale = $('#data').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            data:data,
            columns: [
                { 'data': 'producto.nombre' },
                { 'data': 'precio' },
                { 'data': 'cantidad' },
                { 'data': 'subtotal' },
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    
                },
                {
                    targets: [2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return parseInt(data);
                    }          
                },
                {
                    targets: [1, 3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$'+parseFloat(data).toFixed(2);
                    }              
                }
            ]
        });
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        // Manejo de errores
        console.error("Error en la solicitud:", textStatus, errorThrown);
    })
    .always(function() {
    });
});
$(function () {
    
    $('#data tbody')
    .on('click', 'a[rel="details"]', function(){
        var tr = tblSale.cell($(this).closest('td, li')).index();
        var data = tblSale.row(tr.row).data()
        //alert_action("Notificacion", "¿Estas seguro de eliminar el item de la factura?", function(){});
    })
})




