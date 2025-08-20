from django.shortcuts import render, redirect

# Hashing the password.
from django.contrib.auth.hashers import make_password

# Importing the model RegisterUser
from .models import RegisterUser, Product

# importing a class that lets me return a plain text.
from django.http import HttpResponse

# Using django's built in messaging system.
from django.contrib import messages

# Create your views here.


# Register user view.
def register_view(request):
    # Collect data from the user.
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if the user exists first.
        # This .exists() checks if any result was found.
        if RegisterUser.objects.filter(username=username).exists():
            return HttpResponse("user already already exists")

        # Hashing the password.
        hashed_password = make_password(password)

        # Save the user manually.
        """using the .create shortcut. BUT 
        user = RegisterUser(username=username, email=email,
          password=hashed_password)user.save()"""
        RegisterUser.objects.create(
            username=username,
            email=email,
            password=hashed_password,  # (Hashed password)
        )

        """Show success message and redirect,
        the user will see the message on the next page."""
        messages.success(request, "User registered successfully!")
        return redirect("login/")

    return render(request, "register.html")


# Login view.
def login_view(request):
    return render(request, "login_activity.html")


# Dashboard view.
def dashboard_view(request):
    return render(request, "dashboard.html")


# logout view.
def logout_view(request):
    return render(request)

# Product entry.
def product_entry(request):
    # Check if it's a POST request (user submitted a form).
    if request.method == 'POST':
        # Get form data from the request.
        name = request.POST.get('name') # Product name.
        price = request.POST.get('price') # Price of the product.
        supplier = request.POST.get('supplier')
        expiry_date = request.POST.get('expiry_date')
        category = request.POST.get('category')
        serial_number = request.POST.get('serial_number')

        # Get file upload (Image).
        image = request.FILES.get('image') # You use request.Files for uploading an image.

        # Check if all fields a provided. (not empty).
        if all([name, price, supplier, expiry_date, category, serial_number, image]):
            # Create and save the product
            Product.objects.create(
                name = name, 
                price = price, 
                supplier = supplier,
                expiry_date = expiry_date,
                category = category,
                serial_number = serial_number,
                image = image # Save the uploaded image.
            )
            # Return a success message.
            return HttpResponse('Product addedd successfully!')
        else:
            # Return error if missing.
            return HttpResponse('All fields are required', status=400)
    return render(request)
