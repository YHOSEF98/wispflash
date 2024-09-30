var vents = {
    items : {
        cliente: '',
        date_joined: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        products: []
    },
    calculate_invoice: function (){
        var subtotal = 0.00;
        var iva = $('input[name="iva"]').val();
        $.each(this.items.products, function(pos, dict){
            dict.pos = pos;
            dict.subtotal = dict.cantidad * parseFloat(dict.precioventa);
            subtotal += dict.subtotal;
        });
        this.items.subtotal = subtotal;
        this.items.iva = this.items.subtotal * iva
        this.items.total = this.items.subtotal + this.items.iva

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="ivacalc"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    add: function(item){
        this.items.products.push(item);
        this.list();
    },
    list: function(){
        this.calculate_invoice()

        $('#tblProductos').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            data: this.items.products,
            columns: [
                { 'data': 'id' },
                { 'data': 'nombre' },
                { 'data': 'precioventa' },
                { 'data': 'cantidad' },
                { 'data': 'subtotal' },
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
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
                console.log(data)
                $(row).find('input[name="cantidad"]').TouchSpin({
                    min: 0,
                    max: 999999999,
                    step: 1,
                })
            }
        });
    },
};


$(function(){
    // evento de cantidad
    $('#tblProductos').on('change keyup', 'input[name="cantidad"]', function () {
        console.clear()
        var cant = parseInt($(this).val());
        console.log(cant)
    });
    // evento buscador de productos
    $('.select2').select2({
        theme: "bootstrap4",
        lenguaje: "es",
    });
    //uso de calendario
    $('#date_joined').datetimepicker({
        format: 'DD-MM-YYYY',
        date: moment().format('DD-MM-YYYY'),
        locale: 'es',
    });
    $("input[name='iva']").TouchSpin({
        min: 0,
        max: 100,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    }).on('change', function(){
        vents.calculate_invoice();
    }).val(0.19);
    //search productos
    $("input[name='search_productos']").autocomplete({
        source: function (request, response){
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action':'search_productos',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function(data){
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) { 
            }).always(function (data){

            })
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            ui.item.cantidad = 1;
            ui.item.subtotal = 0.00;
            vents.add(ui.item)
            $(this).val('');
        }
    });
    
    
});