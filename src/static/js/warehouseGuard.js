$(document).ready(function(){ 
    filterCheckbox = $(".filter-checkbox"); 
    ingrediant_search = $(".ingrediant_search");
    add_item_btn = $(".add_item_btn");

    var filterObj={};

    $(".filter-checkbox,.ingrediant_search").on("click input", function(){
        filterObj['ingrediant_name'] = ingrediant_search.val();
        var _filterKey = filterCheckbox.data('filter');
        filterObj[_filterKey]=Array.from(document.querySelectorAll('input[data-filter='+_filterKey+']:checked')).map(function(el){
            return el.value;
        });
        
        $.ajax({
            url:'/dashboard/warehouseGuard/ingredients/',
            data:filterObj,
            dataType:'json',
            beforeSend:function(){
            },
            success:function(res){
                $("#dashboard_ingredients_list").html(res.ingredients);
            }
        });
    });
      
    
    $("#addCategory_form").on('submit', function(event){
        event.preventDefault();
        var category_name = $('#add_category_name');
        var categories = $('.categories');
        var _obj ={};
        
        _obj['category'] = category_name.val();
        $.ajax({
            url:'/dashboard/warehouseGuard/categories/create/',
            data:_obj,
            dataType:'json',
            beforeSend:function(){
            },
            success:function(response){
                var instance = JSON.parse(response["instance"]);
                var fields = instance[0]["fields"]
                var pk = instance[0]["pk"]
                console.log(pk)
                console.log(fields);
                var opt = `<option value="${pk}" name='category'>${fields["name"]}</option>`
                categories.append(opt);
            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["responseJSON"]["error"]);
            }
        });
                    
    });
    
    $(".add_item_btn").on('click', function(event){
        event.preventDefault();
        var items = $('#items');
        var _obj ={};
        $.ajax({
            url:'/dashboard/warehouseGuard/invoices/addItem/',
            data:_obj,
            dataType:'json',
            beforeSend:function(){
            },
            success:function(response){
                items.append(response.data);
            }
        });
                    
    });


    $(".supplier_search, .filter_fromDate, .filter_toDate, .filter_minPrice, .filter_maxPrice").on('input', function(event){
        event.preventDefault();
        status_search = $(".status_search");
        var invoice_type=status_search.data('status');
        console.log(invoice_type)
        var _obj ={};
        supplier_search = $(".supplier_search");
        filter_fromDate = $(".filter_fromDate");
        filter_toDate = $(".filter_toDate");
        filter_minPrice = $(".filter_minPrice");
        filter_maxPrice = $(".filter_maxPrice");
        var supplier = supplier_search.val();
        var fromDate = filter_fromDate.val();
        var toDate = filter_toDate.val();
        var minPrice = filter_minPrice.val();
        var maxPrice = filter_maxPrice.val();
        _obj['supplier'] = supplier;
        _obj['fromDate'] = fromDate;
        _obj['toDate'] = toDate;
        _obj['minPrice'] = minPrice;
        _obj['maxPrice'] = maxPrice;
        
        console.log(_obj);

        $.ajax({
            url:`/dashboard/warehouseGuard/spesificInvoices/${invoice_type}`,
            data:_obj,
            dataType:'json',
            beforeSend:function(){
            },
            success:function(response){
                $("#dashboard_invoices_list").html(response.invoices);
            }
        });
    });

    $(".just_supplier_search").on('input', function(event){
        event.preventDefault();
        var _obj ={};
        just_supplier_search = $(".just_supplier_search");
        var supplier = just_supplier_search.val();
        _obj['supplier'] = supplier;
        console.log(_obj);
        $.ajax({
            url:'/dashboard/warehouseGuard/suppliers/',
            data:_obj,
            dataType:'json',
            beforeSend:function(){
            },
            success:function(response){
                $("#dashboard_suppliers_list").html(response.suppliers);
            }
        });
    });
        
    
});

    