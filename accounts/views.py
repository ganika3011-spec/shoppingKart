# from email.message import EmailMessage (Removed redundant import)
# from pyexpat.errors import messages (Removed incorrect import)
import logging
logger = logging.getLogger(__name__)
from django.shortcuts import redirect, render,get_object_or_404

from accounts.forms import RegistrationForm,LoginForm,UserForm,UserProfileForm
from accounts.models import Account,UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

## verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponse
from carts.models import Cart, CartItem
from carts.views import _cart_id
import requests
from orders.models import Order
from store.models import Product, Wishlist

def register(request):
    form= RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username= email.split('@')[0]

            user= Account.objects.create_user(first_name=first_name, last_name=last_name, email=email,username=username, password=password)
            user.phone_number= phone_number
            user.save()
            #  user Activation
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            try:
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()
                messages.success(request, 'Thank you for registering! Please check your email for the activation link.')
            except Exception as e:
                logger.error(f"Email delivery failed: {e}")
                messages.warning(request, "Registration successful, but we couldn't send the activation email. Please contact support.")
            
            return redirect('/accounts/login/?command=verification&email='+email)

    else:
        form= RegistrationForm()
    context = {'form': form}
    return render(request, 'accounts/register.html', context)



from django.contrib import messages, auth
from django.contrib.auth.models import User

def login(request):
    print("LOGIN VIEW HIT")  # 🔥 debug proof
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        

        user = auth.authenticate(
            email=email,
            password=password
        )

        if user is not None:
            try:
                cart= Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists= CartItem.objects.filter(cart= cart).exists()
                if is_cart_item_exists:
                    cart_item= CartItem.objects.filter(cart= cart)
                    product_variation= []
                    for item in cart_item:
                        variation= item.variations.all()
                        product_variation.append(list(variation))
                    cart_item= CartItem.objects.filter(user= user)
                    ex_var_list= []
                    id= []  
                    for item in cart_item:
                        existing_variation= item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                    print(ex_var_list)
                   # product_variation=[1,2,3,4,5]
                   # ex_var_list=[4,6,7,8,9]
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index= ex_var_list.index(pr)
                            item_id= id[index]
                            item= CartItem.objects.get(product= item.product, id= item_id)
                            item.quantity += 1
                            item.user= user
                            item.save()
                        else:
                            cart_item= CartItem.objects.filter(cart= cart)

                            for item in cart_item:
                                item.user=user
                                item.save()

                

            except:   
                pass
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')

    return render(request, 'accounts/login.html')



@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')    
    return redirect('login')

def activate(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None 
        return HttpResponse('ok')
      
    if user is not None and default_token_generator.check_token(user, token):
          user.is_active = True
          user.save()
          messages.success(request, 'Congratulations! Your account is activated.')
          return redirect('login')
    else:
          messages.error(request, 'Invalid activation link')
          return redirect('register')
@login_required(login_url='login')
def dashboard(request):
   # orders= Order.objects.order_by("-created_at").filter(user_id=request,is_ordered=True)
   # orders_count=orders.count()
   # context={
   #     "orders_count":orders_count,
   # }
   return render(request, 'accounts/dashboard.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')
    
def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful.')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('reset_password')
    else:
        return render(request, 'accounts/reset_password.html')       
    
@login_required(login_url='login')
def my_orders(request):
    """Display user's order history."""
    orders = Order.objects.filter(
        user=request.user,
        is_ordered=True
    ).order_by('-created_at')
    
    context = {
        'orders': orders,
        'orders_count': orders.count(),
    }
    return render(request, "accounts/my_orders.html", context)

@login_required(login_url='login')
def edit_profile(request):
    #userprofile=get_object_or_404(UserProfile,user=request.user)
    #if request.method=="POST":
    #    user_form= UserForm(request.POST,instance=request.user)
   #     profile_form= UserProfileForm(request.POST,request.FILES,isinstance=userprofile)
   #     if user_form.is_valid() and profile_form.is_valid() :
   #         user_form.save()
   #         profile_form.save()
   #         messages.success(request,"Your Profile has been updated!")
   #         return redirect("edit_profile")
    #else:
     #   user_form= UserForm(instance=request.user)
     #   profile_form= UserProfile(instance= userprofile)
     #   context={
     #       'user_form':user_form,
     #       "profile_form":profile_form,
     #       'userprofile':userprofile,
      #  }
    return render(request,"accounts/edit_profile.html")
@login_required(login_url='login')
def change_password(request):   
    if request.method=="POST":
        current_password= request.POST['current_password']
        new_password= request.POST['create_new_password']
        confirm_new_password= request.POST['confirm_new_password']
        user= Account.objects.get(username__exact=request.user.username)
        if new_password== confirm_new_password:
            success= user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request,"Password updated successfully!")
                return redirect("change_password")
            else:
                messages.error(request,"Please enter valid current password!")
                return redirect("change_password")
        else:
            messages.error(request,"Password does not match!")
            return redirect("change_password")
    return render(request,"accounts/change_password.html")


def order_detail(request, order_id):
    '''
    order_detail=OrderProduct.objects.filter(order__order_number=order_id)
    order= Order.objects.get(order_number=order_id)
    subtotal=0
    for i in order_detail:
        subtotal += i.product_price * i.quantity
    context={
        'order_detail':order_detail,
        'order':order,
        'subtotal':subtotal,
    }
    '''
    return render(request, 'accounts/order_detail.html')


@login_required(login_url='login')
def wishlist(request):
    """Display user's wishlist."""
    try:
        wishlist_obj = Wishlist.objects.get(user=request.user)
        products = wishlist_obj.products.all()
        product_count = products.count()
    except Wishlist.DoesNotExist:
        wishlist_obj = None
        products = Product.objects.none()
        product_count = 0
    
    context = {
        'wishlist': wishlist_obj,
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'accounts/wishlist.html', context)


@login_required(login_url='login')
def add_to_wishlist(request, product_id):
    """Add product to wishlist."""
    product = get_object_or_404(Product, id=product_id)
    wishlist_obj, created = Wishlist.objects.get_or_create(user=request.user)
    
    if wishlist_obj.products.filter(id=product_id).exists():
        messages.warning(request, f'{product.product_name} is already in your wishlist!')
    else:
        wishlist_obj.products.add(product)
        messages.success(request, f'{product.product_name} added to wishlist!')
    
    return redirect(request.META.get('HTTP_REFERER', 'store'))


@login_required(login_url='login')
def remove_from_wishlist(request, product_id):
    """Remove product from wishlist."""
    product = get_object_or_404(Product, id=product_id)
    
    try:
        wishlist_obj = Wishlist.objects.get(user=request.user)
        if wishlist_obj.products.filter(id=product_id).exists():
            wishlist_obj.products.remove(product)
            messages.success(request, f'{product.product_name} removed from wishlist!')
        else:
            messages.warning(request, f'{product.product_name} is not in your wishlist!')
    except Wishlist.DoesNotExist:
        messages.warning(request, 'Wishlist not found!')
    
    return redirect(request.META.get('HTTP_REFERER', 'wishlist'))