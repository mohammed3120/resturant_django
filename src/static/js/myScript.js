$(document).ready(function(){
    order_search = $(".order_search");
    var order_typeKey=order_search.data('status');
    var filterObj={};

    $(".order_search").on("input", function(){
        filterObj['customer'] = order_search.val();        
        $.ajax({
            url:'/dashboard/cashier/dashboard_filter_data/'+order_typeKey,
            data:filterObj,
            dataType:'json',
            beforeSend:function(){
            },
            success:function(res){
                $("#dashboard_orders_list").html(res.orders);
            }
        });
    });

       
            

            
});
        
       


    