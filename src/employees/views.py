from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from food.models import Order,Ingredient,Category,Invoice,InvoiceItem
from customers.models import Customer
from suppliers.models import Supplier
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from django.db import transaction
from xhtml2pdf import pisa
from django.core import serializers
from datetime import date
from django.db.models import Q 
from suppliers.forms import SupplierForm
import datetime
from django.db.models import Sum
from .models import Employee

#Cashier functions
def cashierDashboardHome(request):
    orders = Order.objects.all()
    ordered_orders = orders.filter(status = 'Ordered').count()
    preparing_orders = orders.filter(status = 'Preparing').count()
    in_progress_orders = orders.filter(status = 'InProgress').count()
    delivered_orders = orders.filter(status = 'Delivered').count()
    canceled_orders = orders.filter(status = 'Canceled').count()
    context = {'ordered_orders':ordered_orders,
                'preparing_orders':preparing_orders,
                'in_progress_orders':in_progress_orders,
                'delivered_orders':delivered_orders,
                'canceled_orders':canceled_orders}
    return render(request, 'employees/cashier/cashierDashboardHome.html', context)

def cashierDashboardOrderDetails(request,pk):
    order = Order.objects.get(pk = pk)
    context = {'order':order}
    return render(request, 'employees/cashier/cashierDashboardOrderDetails.html', context)

def cashierDashboardOrders(request,status):
    orders = Order.objects.filter(status = status)
    context = {'orders':orders}
    return render(request, 'employees/cashier/cashierDashboardOrders.html', context)

def cashierDashboardSendToKitchen(request,pk):
    prevPath = request.META.get('HTTP_REFERER')
    order = Order.objects.get(pk=pk)
    order.status = 'Preparing'
    order.save()
    return HttpResponseRedirect(prevPath)
    
def cashierDashboardSendToDelivary(request,pk):
    prevPath = request.META.get('HTTP_REFERER')
    order = Order.objects.get(pk=pk)
    order.status = 'InProgress'
    order.save()
    return HttpResponseRedirect(prevPath)


def dashboard_filter_data_view(request,status):
    name = request.GET['customer']
    if status == 'all':
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(status = status)
    print('*******************************************************************************')
    print(orders)
    if len(orders)>0 and  name != "":
        orders = orders.filter(customer__first_name__contains=name)
    
    t=render_to_string('employees/cashier/dashboard_orders_list.html',{'orders':orders})
    return JsonResponse({'orders': t})


#warehouseGuard functions
def warehouseGuardDashboardHome(request):
    ingredients = Ingredient.objects.all()
    ingredients_quantity = ingredients.aggregate(Sum('quantity'))
    ingredients_price = ingredients.aggregate(Sum('price'))
    all_invoices = Invoice.objects.all()
    Pending_invoices = all_invoices.filter(status = 'Pending').count()
    ToAccepting_invoices = all_invoices.filter(status = 'ToAccepting').count()
    Accepted_invoices = all_invoices.filter(status = 'Accepted').count()
    InProgress_invoices = all_invoices.filter(status = 'InProgress').count()
    Delivered_invoices = all_invoices.filter(status = 'Delivered').count()
    Canceled_invoices = all_invoices.filter(status = 'Canceled').count()
    suppliers = Supplier.objects.all()
    suppliers_count = suppliers.count()
    context = {'ingredients_quantity':ingredients_quantity,
               'ingredients_price':ingredients_price,
               'Pending_invoices':Pending_invoices,
               'ToAccepting_invoices':ToAccepting_invoices,
               'Accepted_invoices':Accepted_invoices,
               'InProgress_invoices':InProgress_invoices,
               'Delivered_invoices':Delivered_invoices,
               'Canceled_invoices':Canceled_invoices,
               'suppliers_count':suppliers_count,
               }
    return render(request, 'employees/warehouseGuard/warehouseGuardDashboardHome.html', context)

def warehouseGuardDashboardIngredientDetails(request,pk):
    ingredient = Ingredient.objects.get(pk = pk)
    context = {'ingredient':ingredient}
    return render(request, 'employees/warehouseGuard/warehouseGuardDashboardIngredientDetails.html', context)

def warehouseGuardDashboardIngredients(request):
    if request.is_ajax():
        categories = request.GET.getlist('category[]')
        print(categories)
        ingrediant_name = request.GET['ingrediant_name']
        print(ingrediant_name)
        ingredients = Ingredient.objects.all()
        if len(categories)>0:
            ingredients = ingredients.filter(category__name__in = categories).distinct()
        if ingrediant_name != "":
            ingredients = ingredients.filter(name__contains=ingrediant_name)
        t=render_to_string('employees/warehouseGuard/dashboard_ingredients_list.html',{'ingredients':ingredients})
        return JsonResponse({'ingredients': t})
        
        
    else:
        ingredients = Ingredient.objects.all()
        categories = Category.objects.all()
        context = {'ingredients':ingredients,'categories':categories}
        return render(request, 'employees/warehouseGuard/warehouseGuardDashboardIngredients.html', context)

def warehouseGuardDashboardInvoices(request,status):
    if request.is_ajax():
        supplier_name = request.GET['supplier']
        fromDate = request.GET['fromDate']
        toDate = request.GET['toDate']
        minPrice = request.GET['minPrice']
        maxPrice = request.GET['maxPrice']
        invoices = Invoice.objects.filter(status = status)
        #filter by date
        if fromDate != '' and toDate != '':
            invoices = invoices.filter(created__range=[fromDate, toDate])
        elif fromDate != '' and toDate == '':
            toDate = date.today()
            invoices = invoices.filter(created__range=[fromDate, toDate])
        elif fromDate == '' and toDate != '':
            fromDate = "2001-01-01"
            invoices = invoices.filter(created__range=[fromDate, toDate])
        else:
            pass
        #filter by price
        if minPrice != '' and maxPrice != '':
            minP = float(minPrice)
            maxP = float(maxPrice)
            print("minPrice",type(minP))
            print("maxPrice",type(maxP))
            if maxP > minP:
                invoices = invoices.filter(price__gte = minP, price__lte = maxP)
        elif minPrice == '' and maxPrice != '':
            maxP = float(maxPrice)
            print("maxPrice",maxP)
            invoices = invoices.filter(price__lte=maxP)
        elif minPrice != '' and maxPrice == '':
            minP = float(minPrice)
            print("minPrice",minP)
            invoices = invoices.filter(price__gte=minP)
        else:
            pass
        
        if supplier_name != '':
            invoices = invoices.filter(Q(supplier__first_name__icontains = supplier_name) | Q(supplier__last_name__icontains = supplier_name))
        t=render_to_string('employees/warehouseGuard/dashboard_invoices_list.html',{'invoices':invoices})
        return JsonResponse({'invoices': t})
        
        
    else:
        invoices = Invoice.objects.filter(status = status)
        context = {'invoices':invoices}
        return render(request, 'employees/warehouseGuard/warehouseGuardDashboardInvoices.html', context)

def warehouseGuardDashboardInvoiceDetails(request,pk):
    invoice = Invoice.objects.get(pk = pk)
    context = {'invoice':invoice}
    return render(request, 'employees/warehouseGuard/warehouseGuardDashboardInvoiceDetails.html', context)

def warehouseGuardDashboardCreateInvoice(request):
    if request.method =='GET':
        suppliers = Supplier.objects.all()
        categories = Category.objects.all()
        context = {'suppliers':suppliers,'categories':categories}
        return render(request, 'employees/warehouseGuard/warehouseGuardDashboardInvoice.html', context)
    elif request.method =="POST":
        supplier_id = int(request.POST['supplier'])
        supplier = Supplier.objects.get(id = supplier_id)
        description = request.POST['description']
        names = request.POST.getlist('item')
        categories = request.POST.getlist('category')
        quantities = request.POST.getlist('quantity')
        prices = request.POST.getlist('price')
        if '' in names or '' in quantities or '' in prices:
            prevPath = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(prevPath)
        else:
            invoice = Invoice.objects.create(supplier = supplier, description = description)
            #add items to invoice
            for i in range(len(names)):
                name = names[i]
                category_id = int(categories[i])
                category = Category.objects.get(id = category_id)
                category_name = category.name
                quantity = float(quantities[i])
                price = float(prices[i])
                item = InvoiceItem.objects.create(invoice = invoice, name = name, price = price, category = category_name, quantity = quantity)
                item.save()
                transaction.commit()
            invoice.save()
            transaction.commit()
            return HttpResponseRedirect(reverse('employees:warehouseGuardDashboardInvoices' , args=(invoice.status ,)))


    else:
        context = {}
        return render(request, 'employees/warehouseGuard/warehouseGuardDashboardInvoice.html', context)

def warehouseGuardDashboardEditInvoice(request,pk):
    if request.method =='GET':
        suppliers = Supplier.objects.all()
        categories = Category.objects.all()
        invoice = Invoice.objects.get(id = pk)
        items = InvoiceItem.objects.filter(invoice = invoice)
        context = {'suppliers':suppliers, 'categories':categories, 'invoice':invoice, 'items':items}
        return render(request, 'employees/warehouseGuard/warehouseGuardDashboardEditInvoice.html', context)
    elif request.method =="POST":
        supplier_id = int(request.POST['supplier'])
        supplier = Supplier.objects.get(id = supplier_id)
        description = request.POST['description']
        ids = request.POST.getlist('id')
        names = request.POST.getlist('item')
        categories = request.POST.getlist('category')
        quantities = request.POST.getlist('quantity')
        prices = request.POST.getlist('price')
        if '' in names or '' in quantities or '' in prices:
            prevPath = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(prevPath)
        else:
            invoice = Invoice.objects.get(id = pk)
            invoice.supplier = supplier
            invoice.description = description
            #add items to invoice
            for i in range(len(names)):
                name = names[i]
                category_id = int(categories[i])
                category = Category.objects.get(id = category_id)
                category_name = category.name
                quantity = float(quantities[i])
                price = float(prices[i])
                idd = int(ids[i])
                item = InvoiceItem.objects.get(id = idd)
                item.invoice = invoice
                item.name = name
                item.category = category_name
                item.quantity = quantity
                item.price = price
                item.save()
                transaction.commit()
            status = invoice.status
            invoice.save()
            transaction.commit()
            return HttpResponseRedirect(reverse('employees:warehouseGuardDashboardInvoices' , args=(status ,)))

def warehouseGuardDashboardToAcceptingInvoice(request, pk):
    invoice = Invoice.objects.get(id = pk)
    old_status = invoice.status
    invoice.status = 'ToAccepting'
    invoice.save()
    transaction.commit()
    return HttpResponseRedirect(reverse('employees:warehouseGuardDashboardInvoices' , args=(old_status ,)))

def warehouseGuardDashboardAcceptedInvoice(request, pk):
    invoice = Invoice.objects.get(id = pk)
    old_status = invoice.status
    invoice.status = 'InProgress'
    invoice.save()
    transaction.commit()
    return HttpResponseRedirect(reverse('employees:warehouseGuardDashboardInvoices' , args=(old_status ,)))

def warehouseGuardDashboardDeleteInvoice(request,pk):
    invoice = Invoice.objects.get(id = pk)
    status = invoice.status
    invoice.delete()
    return HttpResponseRedirect(reverse('employees:warehouseGuardDashboardInvoices' , args=(status ,)))

def warehouseGuardDashboardAddCategory(request):
    category_name = request.GET['category']
    print(category_name)
    if category_name != "":
        category = Category.objects.create(name = category_name)
        category.save()
        transaction.commit()
        print(type(category.id))
        ser_instance = serializers.serialize('json', [ category, ])
            # send to client side.
        return JsonResponse({"instance": ser_instance}, status=200)
    else:
        # some form errors occured.
        return JsonResponse({"error":"You do not entered any category name"}, status=400)

def warehouseGuardDashboardAddItem(request):
    if request.is_ajax():
        suppliers = Supplier.objects.all()
        categories = Category.objects.all()
        context = {'suppliers':suppliers,'categories':categories}
        t=render_to_string('employees\warehouseGuard\warehouseGuardDashboardItem.html',context)
        return JsonResponse({'data': t})
    else:
        return JsonResponse({})

def warehouseGuardDashboardSuppliers(request):
    suppliers = Supplier.objects.all()
    if request.is_ajax():
        supplier_name = request.GET['supplier']
        if supplier_name != '':
            suppliers = suppliers.filter(Q(first_name__icontains = supplier_name) | Q(last_name__icontains = supplier_name))
        t=render_to_string('employees/warehouseGuard/dashboard_suppliers_list.html',{'suppliers':suppliers})
        return JsonResponse({'suppliers': t})
    else:
        context = {'suppliers':suppliers}
        return render(request, 'employees/warehouseGuard/warehouseGuardDashboardSuppliers.html', context)

def warehouseGuardDashboardAddSupplier(request):
    if request.method =='POST':
        supplierForm = SupplierForm(request.POST)
        if supplierForm.is_valid:
            supplierForm.save()
            return redirect('employees:warehouseGuardDashboardSuppliers')
    else:
        supplierForm = SupplierForm()
        context = {'form': supplierForm}
        return render(request, 'employees/warehouseGuard/warehouseGuardDashboardSupplier.html', context)

def warehouseGuardDashboardEditSupplier(request, pk):
    supplier = Supplier.objects.get(id = pk)
    supplierForm = SupplierForm(instance = supplier)
    if request.method == 'POST':
        supplierForm = SupplierForm(request.POST, instance = supplier)
        if supplierForm.is_valid:
            supplierForm.save()
            return redirect('employees:warehouseGuardDashboardSuppliers')

    context = {'form': supplierForm}
    return render(request, 'employees/warehouseGuard/warehouseGuardDashboardSupplier.html', context)

def warehouseGuardDashboardDeleteSupplier(request,pk):
    supplier = Supplier.objects.get(id = pk)
    supplier.delete()
    return redirect('employees:warehouseGuardDashboardSuppliers')


#Manager function 
def  managerDashboardHome(request):
    context = {} 
    return render(request, 'employees/manager/managerDashboardHome.html', context)

def  managerDashboardEmployees(request):
    employees = Employee.objects.all()
    context = {'employees':employees} 
    return render(request, 'employees/manager/managerDashboardEmployees.html', context)

def  managerDashboardEmployeeDetails(request,pk):
    employee = Employee.objects.get(id = pk)
    context = {'employee':employee} 
    return render(request, 'employees/manager/managerDashboardEmployeeDetails.html', context)

def managerDashboardDeleteEmployee(request, pk):
    employee = Employee.objects.get(id = pk)
    employee.delete()
    return redirect('employees:managerDashboardEmployees')
    
#from django.utils import timezone
# def warehouseGuardDashboardCharts(request):
#         sorting = request.GET['sorting']
#         ingredients = Ingredient.objects.all()
#         print(sorting)
        
        
#         if sorting == "this_week":
#             today = timezone.now()
#             # Define a list of weekday names
#             days = ['Sunday','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
#             labels = []
#             for i in range(7):
#                 labels.append(days[(today.weekday()+i)%7])
#             print('labels',labels)
            
#             start_week = today - datetime.timedelta(days=6)
        
#             ingredients = ingredients.filter(updated__range=[start_week, today])
#             context = {'ingredients':ingredients, 'labels':labels}
#             ser_instance = serializers.serialize('json', context)
#             return JsonResponse({"data": ser_instance}, status=200)
#         elif sorting == "this_month":
            
#             ser_instance = serializers.serialize('json', ingredients)
#                 # send to client side.
#             return JsonResponse({"data": ser_instance}, status=200)
#         elif sorting == "this_year":
#             ser_instance = serializers.serialize('json', ingredients)
#                 # send to client side.
#             return JsonResponse({"data": ser_instance}, status=200)
#         else:
#             # some form errors occured.
#             return JsonResponse({"error":"You do not entered any category name"}, status=400)



# def render_pdf_view(request,pk):
#     template_path = 'employees/cashier/pdfOrder.html'
#     order = Order.objects.get(pk = pk)
#     context = {'order':order}
#     # Create a Django response object, and specify content_type as pdf
#     response = HttpResponse(content_type='application/pdf')
#     #if downlod
#     #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
#     #if display
#     response['Content-Disposition'] = 'filename="order.pdf"'
#     # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(context)

#     # create a pdf
#     pisa_status = pisa.CreatePDF(
#        html, dest=response)
#     # if error then show some funy view
#     if pisa_status.err:
#        return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response

# def ordersReport(request, status):
#     template_path = 'employees/cashier/ordersReport.html'
#     orders = Order.objects.filter(status = status)
#     context = {'orders':orders}
#     # Create a Django response object, and specify content_type as pdf
#     response = HttpResponse(content_type='application/pdf')
#     #if downlod
#     #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
#     #if display
#     response['Content-Disposition'] = 'filename="orders2.pdf"'
#     # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(context)

#     # create a pdf
#     pisa_status = pisa.CreatePDF(
#        html, dest=response)
#     # if error then show some funy view
#     if pisa_status.err:
#        return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response
