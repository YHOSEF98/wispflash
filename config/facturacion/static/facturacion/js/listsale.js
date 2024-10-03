var tblSale;
$(function () {

    tblSale = $('#data').DataTable({
        //responsive: true,
        scrollX: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            { 'data': 'id' },
            { 'data': 'cliente' },
            { 'data': 'date_joined' },
            { 'data': 'subtotal' },
            { 'data': 'iva' },
            { 'data': 'total' },
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a rel="remove" type="button" class="btn btn-danger btn-xs btn-flat""><i class="fas fa-trash-alt"></i></a>';
                    buttons += '<a rel="details" type="button" class="btn btn-success btn-xs btn-flat""><i class="fas fa-search"></i></a>';
                    return buttons;
                }
                
            },
            {
                targets: [2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$'+parseFloat(data).toFixed(2);
                }              
            },
            {
                targets: [3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<input type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="'+row.cantidad+'">';
                }              
            },
            {
                targets: [4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$'+parseFloat(data).toFixed(2);
                }              
            }
        ],
        rowCallback( row, data, displayNum, displayIndex, dataIndex){
            $(row).find('input[name="cantidad"]').TouchSpin({
                min: 0,
                max: 999999999,
                step: 1,
            })
        }
    });

    $('#data tbody')
    .on('click', 'a[rel="details"]', function(){
        var tr = tblSale.cell($(this).closest('td, li')).index();
        var data = tblSale.row(tr.row).data()
        //alert_action("Notificacion", "¿Estas seguro de eliminar el item de la factura?", function(){});
    })
})




