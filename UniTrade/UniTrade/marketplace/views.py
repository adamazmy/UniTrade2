from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from .models import Department, Photo, Product, Productimage, Comment
from accounts.models import CustomUser
import os
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse


# Create your views here.


"""
                    ###   AUTHOR: ADAM AZMY   ###
                    
current function:
    Displays the user's current listings (authenticated user required).

    Context:
        - departments (all departments)
        - productimages (all product images)
        - products (user's listings)
"""
def current(request):
    departments = Department.objects.all()
    productimages = Productimage.objects.all()
    products = Product.objects.filter(seller=request.user)


    context = {'departments':departments, 'productimages':productimages, 'products': products}
    return render(request, 'marketplace/currentListing.html', context)




"""
                    ###   AUTHOR: ADAM AZMY   ###
                    
inputCondition function:
Renders a page for users to input product condition (functionality unclear).
"""
def inputCondition(request):
    return render(request, 'marketplace/condition.html')





"""
                    ###   AUTHOR: ADAM AZMY   ###
                    
additem function:
Handles form submission for adding a new product listing (authenticated user required).

POST request:
    - Creates a new Product object with user data and uploaded images.
    - Redirects to 'current' view after successful creation.

GET request or form errors:
    - Renders the 'add.html' template with available departments.
"""
@login_required
def addItem(request):
    print("POST 1")
    print(request.method)
    if request.method == 'POST':
        print("POST")
        title = request.POST.get('title')

        print(title)

        brand = request.POST.get('brand', '')
        print(brand)

        department = request.POST.get('department')
        print(department)

        price = request.POST['price']
        print(price)

        condition = request.POST['condition']
        print(condition)

        description = request.POST['description']

        print(title, brand, department, price, condition, description)

        images = request.FILES.getlist('image')  # for single file upload
       
      
        # Create and save the new object to the database

        new_object = Product(
            title=title,
            brand=brand,
            department_id=department,  # assuming department is a ForeignKey
            price=price,
            condition=condition,
            description=description,
            seller = request.user
        )
        new_object.save()

        auto_generated_key = new_object.pk
        save_path = 'static/images/' +str(auto_generated_key)
        os.makedirs(save_path)

        
        for image in images:
            image_object = Productimage(
            imageURL = image,
            product_id = auto_generated_key
            )
            image_object.save()
        
        return redirect('current')  # Redirect after POST
    # If not POST method or there are form errors
    departments = Department.objects.all()  # Assuming you have a Department model
    
    return render(request, 'marketplace/add.html', {'departments': departments})

    



"""
                    ###   AUTHOR: ZIYAD ELGYZIRI   ###
                    
edit_item function:
Handles editing an existing product listing (authenticated user required).

**Permissions:**
    - Only the seller of the product can edit it.

POST request:
    - Updates the product details with new data.
    - Handles potential department ID validation errors.
    - Optionally handles image uploads (implementation details omitted).
    - Redirects to the product detail page ('item') after successful update.

GET request:
    - Retrieves the product to be edited.
    - Populates the edit form with existing product data.
    - Renders the 'edit.html' template with available departments.
"""
@login_required
def edit_item(request, product_id):
  # Check if user has permission to edit this product (e.g., is the owner)
  product = get_object_or_404(Product, pk=product_id, seller=request.user)  

  if request.method == 'POST':
    title = request.POST.get('title')
    brand = request.POST.get('brand', '')
    department_id = request.POST.get('department')
    try:
        department = Department.objects.get(pk=department_id)
    except Department.DoesNotExist:
    # Handle case where department ID is invalid (e.g., raise a form error)
        pass

    price = request.POST['price']
    condition = request.POST['condition']
    description = request.POST['description']
    images = request.FILES.getlist('image')  # for multiple image uploads

    # Update product data
    product.title = title
    product.brand = brand
    product.department = department
    product.price = price
    product.condition = condition
    product.description = description
    product.save()

    # Handle image uploads (optional)
    # You can modify this section based on your preferred image storage strategy
    if images:
      for image in images:
        image_object = Productimage(imageURL=image, product=product)
        image_object.save()

    return redirect('item', product_id=product.product_id)  # Redirect to product detail page after edit

  # If not POST method, pre-populate the edit form with existing product data
  departments = Department.objects.all()  # Assuming you have a Department model
  context = {
      'product': product,
      'departments': departments,
  }
  return render(request, 'marketplace/edit.html', context)




"""
                    ###   AUTHORS: ADAM AZMY & ZIYAD ELGYZIRI   ###
                    
viewItem function:
Displays details of a specific product listing.

Retrieves the product, its images, and any associated comments.

Context:
    - product
    - productimages (images associated with the product)
    - comments (comments left on the product)
"""
def viewItem(request, product_id):
    product = get_object_or_404(Product, pk=product_id)  # Get specific listing by ID (or raise 404)
    productimages = Productimage.objects.filter(product=product_id)
    comments = product.comments.all()  # Fetch comments for this product


    context = {'product': product, 'productimages' : productimages, 'comments' : comments}
    
    return render(request, 'marketplace/item.html', context)


@login_required
def remove_item(request, product_id):
    if request.method == 'DELETE':
        product = get_object_or_404(Product, pk=product_id, seller=request.user)
        product.delete()
        # Handle successful deletion (e.g., redirect to user's listings page)
        return redirect('current')  # Assuming 'current' redirects to user's listings
    else:
        return redirect('item', product_id=product_id)  # Redirect back to product detail page on non-DELETE requests




"""
                    ###   AUTHOR: ZIYAD ELGYZIRI   ###
                    
account function:
Renders the user account details page (authenticated user required).

Context:
    - user (currently logged-in user)
"""
@login_required
def account(request):
  return render(request, 'marketplace/account.html', context={'user': request.user})




"""
                    ###   AUTHOR: ZIYAD ELGYZIRI   ###

add_comment function:
Handles form submission for adding a comment to a product (authenticated user required).

POST request:
    - Creates a new Comment object with the submitted content.
    - Redirects to the product detail page ('item') after successful comment creation.

GET request (not recommended):
    - Redirects back to the product detail page.
"""
@login_required
def add_comment(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        content = request.POST['content']
        # Create a new comment object
        comment = Comment(content=content, product=product, author=request.user)
        comment.save()
        # Redirect to the product page after successful comment submission
        return redirect('item', product_id=product.product_id)
    else:
        # Handle potential GET requests (not recommended for adding comments)
        return redirect('item', product_id=product_id)



"""
                    ###   AUTHOR: ADAM AZMY & ZIYAD ELGYZIRI   ###

productPage function:
Displays a page with all available products.

Context:
    - products (all listings)
    - productimages (all product images)
"""
def productPage(request):
    products = Product.objects.all()
    productimages = Productimage.objects.all()

  # Pass products context to the template
    context = {'products': products, 'productimages' : productimages}

    return render(request, 'marketplace/products.html', context)




"""
                    ###   AUTHOR: ADAM AZMY   ###

Renders the 'about us' page.
"""
def aboutUs(request):

    return render(request,'marketplace/aboutus.html')




"""
                    ###   AUTHOR: ADAM AZMY   ###

Renders the 'frequently asked questions' page.
"""
def faq(request):

    return render(request, 'marketplace/faq.html')



"""                    ###   AUTHOR: ZIYAD ELGYZIRI   ###

Renders the 'terms and conditions' page.
"""
def termsandcond(request):

    return render(request, 'marketplace/Terms_and_Conditions.html')



"""
                    ###   AUTHOR: ZIYAD ELGYZIRI   ###

Renders the 'privacy policy' page.
"""
def privacypolicy(request):

    return render(request, 'marketplace/PrivacyPolicy.html')




"""
                    ###   AUTHOR: ZIYAD ELGYZIRI   ###

Displays products in the 'Technology' department.

Context:
    - departments (all departments)
    - productimages (all product images)
    - products (products belonging to the 'Tech' department)
"""
def technology(request):

    departments = Department.objects.all()
    productimages = Productimage.objects.all()
    products = Product.objects.filter(department__name='Tech')

    context = {'departments':departments, 'productimages':productimages, 'products': products}
    return render(request, 'marketplace/Technology.html',context)





"""
                    ###   AUTHOR: ADAM AZMY & ZIYAD ELGYZIRI   ###

Displays products in the 'Books and Literature' department.

Context:
    - departments (all departments)
    - productimages (all product images)
    - products (products belonging to the 'Books and Literature' department)
"""
def books(request):

    departments = Department.objects.all()
    productimages = Productimage.objects.all()
    products = Product.objects.filter(department__name='Books & Literature')

    context = {'departments':departments, 'productimages':productimages, 'products': products}
    return render(request, 'marketplace/books.html', context)





"""
                    ###   AUTHOR: ADAM AZMY & ZIYAD ELGYZIRI   ###

Displays products in the 'Sports and Leisure' department.

Context:
    - departments (all departments)
    - productimages (all product images)
    - products (products belonging to the 'Sports' department)
"""
def sportsLeisure(request):

    departments = Department.objects.all()
    productimages = Productimage.objects.all()
    products = Product.objects.filter(department__name='Sports & Leisure')

    context = {'departments':departments, 'productimages':productimages, 'products': products}
    return render(request, 'marketplace/Sportsleisure.html',context)





"""
                    ###   AUTHOR: ADAM AZMY & ZIYAD ELGYZIRI   ###

Displays products in the 'Electronics & Computers' department.

Context:
    - departments (all departments)
    - productimages (all product images)
    - products (products belonging to the 'Electronics & Computers' department)
"""
def electronicsComputer(request):

    departments = Department.objects.all()
    productimages = Productimage.objects.all()
    products = Product.objects.filter(department__name='Electronics & Computers')

    context = {'departments':departments, 'productimages':productimages, 'products': products}
    return render(request, 'marketplace/ElectronicsComputers.html',context)





"""
                    ###   AUTHOR: ADAM AZMY & ZIYAD ELGYZIRI   ###

Displays products in the 'Education' department.

Context:
    - departments (all departments)
    - productimages (all product images)
    - products (products belonging to the 'Education' department)
"""
def education(request):

    departments = Department.objects.all()
    productimages = Productimage.objects.all()
    products = Product.objects.filter(department__name='Education')

    context = {'departments':departments, 'productimages':productimages, 'products': products}
    return render(request, 'marketplace/Education.html',context)






"""
                    ###   AUTHOR: ADAM AZMY & ZIYAD ELGYZIRI   ###

Displays products in the 'Home Equipment' department.

Context:
    - departments (all departments)
    - productimages (all product images)
    - products (products belonging to the 'Home Equipment' department)
"""
def homeEquipment(request):

    departments = Department.objects.all()
    productimages = Productimage.objects.all()
    products = Product.objects.filter(department__name='Home Equipments')

    context = {'departments':departments, 'productimages':productimages, 'products': products}
    return render(request, 'marketplace/homeEquipment.html',context)






"""
                    ###   AUTHOR: ADAM AZMY & ZIYAD ELGYZIRI   ###

Displays products in the 'Film, Tv, Music' department.

Context:
    - departments (all departments)
    - productimages (all product images)
    - products (products belonging to the 'Film, Tv, Music' department)
"""
def filmTvMusic(request):

    departments = Department.objects.all()
    productimages = Productimage.objects.all()
    products = Product.objects.filter(department__name='Film, Tv, Music')

    context = {'departments':departments, 'productimages':productimages, 'products': products}
    return render(request, 'marketplace/filmTvMusic.html',context)





"""
                    ###   AUTHOR: SHAHRAD ZEINALI   ###

Handles product search by title or department name.

POST request:
    - Performs a search using the provided query string.
    - Filters products and images based on title or department name.

GET request or invalid search:
    - Renders the search page with an empty context.

Context (on successful search):
    - query (search query string)
    - posts (products matching the search)
    - images (product images matching the search)
    - categories (departments matching the search)
    - photos (potentially additional images based on search, functionality unclear)
"""
def search_action(request):
    
    if request.method =='POST':
        search_query = request.POST['search_query']
        posts = Product.objects.filter(Q(title__icontains=search_query))
        categories = Product.objects.filter(Q(department__name__icontains=search_query))
        
        images = Productimage.objects.filter(Q(product__title__icontains=search_query))
        photos = Productimage.objects.filter(Q(product__department__name__icontains=search_query))
        return render(request, 'marketplace/Search_2.html', {'query':search_query, 'posts':posts, 'images':images, 'categories':categories, 'photos':photos})
    else:
        return render(request, 'marketplace/Search_2.html', {})
    
    


    
    
    