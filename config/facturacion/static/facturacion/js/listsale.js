var tblSale;
// $(function () {
//     tblSale=$('#data').DataTable({
//         responsive: true,
//         autoWidth: false,
//         destroy: true,
//         deferRender: true,
//         ajax:{
//             url: window.location.pathname,
//             type: 'POST',
//             data: {
//                 'action' : 'detail_products',
//             },
//             dataSrc:""
//         },
//         columns: [
//             { 'data': 'nombre' },
//             { 'data': 'precioventa' },
//             { 'data': 'cantidad' },
//             { 'data': 'subtotal' },
//         ],
//         columnDefs: [
//             {
//                 targets: [0],
//                 class: 'text-center',
//                 orderable: false,
                
//             },
//             {
//                 targets: [1, 2, 3],
//                 class: 'text-center',
//                 orderable: false,
//                 render: function (data, type, row) {
//                     return '$'+parseFloat(data).toFixed(2);
//                 }              
//             }
//         ]
//     });
//     $('#data tbody')
//     .on('click', 'a[rel="details"]', function(){
//         var tr = tblSale.cell($(this).closest('td, li')).index();
//         var data = tblSale.row(tr.row).data()
//         //alert_action("Notificacion", "¿Estas seguro de eliminar el item de la factura?", function(){});
//     })
// })




