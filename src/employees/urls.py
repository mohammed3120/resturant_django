from django.urls import path
from . import views
app_name = "employees"
urlpatterns = [
    #cashier urls
    path('cashier/',views.cashierDashboardHome, name="cashierDashboardHome"),
    path('cashier/orders/<str:status>',views.cashierDashboardOrders, name="cashierDashboardOrders"),
    path('cashier/orders/sentToKitchen/<int:pk>',views.cashierDashboardSendToKitchen, name="cashierDashboardSendToKitchen"),
    path('cashier/orders/sentToDelivary/<int:pk>',views.cashierDashboardSendToDelivary, name="cashierDashboardSendToDelivary"),
    path('cashier/order/<int:pk>',views.cashierDashboardOrderDetails, name="cashierDashboardOrderDetails"),
    path('cashier/dashboard_filter_data/<str:status>',views.dashboard_filter_data_view, name='dashboard_filter_data'),
    #warehouseGuard urls  
    path('warehouseGuard/',views.warehouseGuardDashboardHome, name="warehouseGuardDashboardHome"),
    path('warehouseGuard/ingredient/<int:pk>',views.warehouseGuardDashboardIngredientDetails, name="warehouseGuardDashboardIngredientDetails"),
        
    path('warehouseGuard/ingredients/',views.warehouseGuardDashboardIngredients, name="warehouseGuardDashboardIngredients"),

    path('warehouseGuard/spesificInvoices/<str:status>',views.warehouseGuardDashboardInvoices, name="warehouseGuardDashboardInvoices"),


    path('warehouseGuard/invoice/edit/<int:pk>',views.warehouseGuardDashboardEditInvoice, name="warehouseGuardDashboardEditInvoice"),

    path('warehouseGuard/invoice/delete/<int:pk>',views.warehouseGuardDashboardDeleteInvoice, name="warehouseGuardDashboardDeleteInvoice"),



    path('warehouseGuard/invoice/<int:pk>',views.warehouseGuardDashboardInvoiceDetails, name="warehouseGuardDashboardInvoiceDetails"),

    path('warehouseGuard/invoices/create',views.warehouseGuardDashboardCreateInvoice, name="warehouseGuardDashboardCreateInvoice"),

    path('warehouseGuard/categories/create/',views.warehouseGuardDashboardAddCategory, name="warehouseGuardDashboardAddCategory"),

    path('warehouseGuard/invoices/addItem/',views.warehouseGuardDashboardAddItem, name="warehouseGuardDashboardAddItem"),

    path('warehouseGuard/invoices/ToAccepting/<int:pk>',views.warehouseGuardDashboardToAcceptingInvoice, name="warehouseGuardDashboardToAcceptingInvoice"),

    path('warehouseGuard/invoices/Accepted/<int:pk>',views.warehouseGuardDashboardAcceptedInvoice, name="warehouseGuardDashboardAcceptedInvoice"),


    path('warehouseGuard/suppliers/',views.warehouseGuardDashboardSuppliers, name="warehouseGuardDashboardSuppliers"),

    path('warehouseGuard/suppliers/create',views.warehouseGuardDashboardAddSupplier, name="warehouseGuardDashboardAddSupplier"),

    path('warehouseGuard/suppliers/edit/<int:pk>',views.warehouseGuardDashboardEditSupplier, name="warehouseGuardDashboardEditSupplier"),

    path('warehouseGuard/suppliers/delete/<int:pk>',views.warehouseGuardDashboardDeleteSupplier, name="warehouseGuardDashboardDeleteSupplier"),


    #Manager Dashboard
    path('manager/',views.managerDashboardHome, name="managerDashboardHome"),
    path('manager/employees/',views.managerDashboardEmployees, name="managerDashboardEmployees"),
    path('manager/employees/<int:pk>',views.managerDashboardEmployeeDetails, name="managerDashboardEmployeeDetails"),
    path('manager/employees/delete/<int:pk>',views.managerDashboardDeleteEmployee, name="managerDashboardDeleteEmployee"),

    


    # path('warehouseGuard/charts/',views.warehouseGuardDashboardCharts, name="warehouseGuardDashboardCharts"),


    # path('cashier/orders/report/<str:status>',views.ordersReport, name="ordersReport"),
    # path('cashier/orders/pdf/<int:pk>',views.render_pdf_view, name="render_pdf_view"),
]

