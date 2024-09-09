from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .models import UserData
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from payment.models import Payment


@login_required
def home(request):
    user_count = UserData.objects.count()
    return render(request, 'index.html', 
    {
        'user_count': user_count
    }) # Render the home template

@login_required
def table(request):
    return render(request, 'tables.html')



@login_required
def InsertInformation(request):
    return render(request,'information.html')

@login_required
def user_data_view(request):
    if request.method == 'POST':
        name = request.POST.get('my_name')
        email = request.POST.get('email')
        mobile_no = request.POST.get('mobile_no')

        # Check if all required fields are filled
        if not name or not email or not mobile_no:
            messages.error(request, 'All fields are required.')
            return render(request, 'information.html', {
                'name': name,
                'email': email,
                'mobile_no': mobile_no
            })

        # Create a new UserData instance and save it
        user_data = UserData(name=name, email=email, mobile_no=mobile_no)
        user_data.save()

        # Add a success message
        messages.success(request, 'Your data has been saved successfully.')
        
        # Redirect to the same page with the success message
        return redirect('information')
    
    return render(request, 'information.html')

@login_required
def view_information(request):
    users = UserData.objects.all()
    return render(request, 'view_information.html', {'users': users})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(UserData, id=user_id)
    user.delete()
    messages.success(request, 'User has been deleted successfully.')
    return redirect('view-info')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def update_user(request, user_id):
    user = get_object_or_404(UserData, id=user_id)

    if request.method == 'POST':
        # Get data from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile_no = request.POST.get('mobile_no')

        # Update user fields
        user.name = name
        user.email = email
        user.mobile_no = mobile_no
        user.save()

        messages.success(request, 'User information updated successfully!')
        return redirect('view-info')  # Redirect to the list view after saving

    return render(request, 'update_user.html', {'user': user})

@login_required
def payment_list(request):
    payments = Payment.objects.all()  # Retrieve all payment records
    context = {
        'payments': payments
    }
    return render(request, 'payment_details.html', context)