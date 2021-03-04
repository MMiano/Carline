from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.core.mail import send_mail

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q

from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from django.template.loader import render_to_string


from django.contrib.auth import (
	authenticate, 
	get_user_model, 
	login,
	logout,
	)



from .forms import (
	
	ProductForm,
	UserEditForm,
	UserLoginForm,
	UserRegistrationForm,
	UserProfileForm,
	UserProfileEditForm,
	VerificationForm,
	TransactionForm,
	RevokeForm,


	)

from .models import (

	UserProfile,
	Product,
	TransactionItem,

	)


from crispy_forms.utils import render_crispy_form

from django.template.context_processors import csrf

User = get_user_model()




def login_user(request, template_name="login.html"):


	next = request.GET.get("next")

	login_form = UserLoginForm(request.POST or None)

	if request.POST and login_form.is_valid():
		user = login_form.login(request)
		if user:
			login(request, user)

			if next:
				return redirect(next)
			return redirect('mainapp:home')

	return render(request, template_name, {'form':login_form})


def logout_user(request):
	logout(request)
	return redirect('/login/')


def register_user(request, template_name="register.html"):

	next = request.GET.get('next')

	user_form = UserRegistrationForm(request.POST or None)
	user_profile_form = UserProfileForm(request.POST or None, request.FILES or None)


	if user_form.is_valid() and user_profile_form.is_valid():

		username = user_form.cleaned_data.get("username")
		password = user_form.cleaned_data.get("password")
		email = user_form.cleaned_data.get('email')

		member = user_form.save(commit=False)
		member.username = username
		member.email = email
		member.set_password(password)
		member.save()
		member_profile = user_profile_form.save(commit=False)
		member_profile.user = member
		member_profile.save()

		send_mail(
    			'Account Verification Code',
			    'Dear user, you have receive this email a result of registering to our site.' + '\n' +
			    'Copy the verification code below to the site verify your account.' + '\n' +
			    member_profile.pin,
   				settings.EMAIL_HOST_USER,
    			[email],
    			fail_silently=False,
			)

		return redirect('mainapp:verify')


		
	return render(request, template_name, {'user_form':user_form, 'profile_form':user_profile_form})



def verify_user(request, template_name='verify.html'):

	verification_form = VerificationForm(request.POST or None)

	if verification_form.is_valid():

		return redirect('login')

	return render(request, template_name, {'form':verification_form})


def home(request, template_name="home.html"):

	product_list = Product.objects.filter(is_active=True)

	latest_products = product_list.order_by('-timestamp')[:8]

	my_transaction_list = TransactionItem.objects.all()
	
	query = request.GET.get("q")

	if query:
		product_list = product_list.filter(
			Q(title__icontains=query) | 
			Q(description__icontains=query) |
			Q(owner__username__icontains=query) |
			Q(owner__email__icontains=query) |
			Q(owner__first_name__icontains=query) |
			Q(owner__last_name__icontains=query)).distinct()
		
	paginator = Paginator(product_list, 8)
	page_request_var = "page"
	page = request.GET.get(page_request_var)

	page = request.GET.get('page')

	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)

	

	return render(request, template_name, {'products':queryset,
		'transactions':my_transaction_list,
		'page_request_var':page_request_var,
		'latest':latest_products})


def product_list(request, template_name="product_list.html"):



	return render(request, template_name, {'object_list':queryset, 'page_request_var':page_request_var})



def view_profile(request, template_name="view-profile.html", username=None):

	profile_owner = User.objects.get(username=username)

	if not request.user.is_authenticated() or request.user != profile_owner:
		raise Http404


	user_obj = get_object_or_404(User, username=username)
	profile_obj = get_object_or_404(UserProfile, user=user_obj)

	first_name = user_obj.first_name
	last_name = user_obj.last_name
	email = user_obj.email
	username = user_obj.username

	owned_qs = Product.objects.filter(owner=user_obj, is_active=True)
	owned_count = owned_qs.count()
	unavailable_qs = owned_qs.filter(is_available = False)
	unavailable_count = unavailable_qs.count()


	requested_qs = TransactionItem.objects.filter(recepient=user_obj)
	requested_count = requested_qs.count()

	return render(request, template_name, {'profile_obj':profile_obj, 
		'first_name':first_name, 
		'last_name':last_name,
		'email':email,
		'username':username,
		'owned':owned_qs,
		'requested':requested_qs,
		'owned_count':owned_count,
		'requested_count':requested_count,
		'unavailable_count':unavailable_count,
		})

def edit_profile(request, template_name="edit-profile.html", username=None):

	profile_owner = User.objects.get(username=username)

	if not request.user.is_authenticated() or request.user != profile_owner:
		raise Http404

	user_obj = get_object_or_404(User, username=username)
	profile_obj = get_object_or_404(UserProfile, user=user_obj)

	
	user_form = UserEditForm(request.POST or None, instance=user_obj)
	profile_form = UserProfileEditForm(request.POST or None, request.FILES or None, instance=profile_obj)

	if user_form.is_valid() and profile_form.is_valid():
		user = user_form.save(commit=False)
		profile = profile_form.save(commit=False)
		user.save()
		profile.user = user
		profile.save()
		messages.success(request, "Profile successfully updated")

		return redirect(profile.get_absolute_url_view())



	return render(request, template_name, {'user_form':user_form, 'profile_form':profile_form})



def owned_parts(request, template_name="owned-parts.html"):

	if not request.user.is_authenticated():
		raise Http404



	owned_parts = Product.objects.filter(owner=request.user, is_active=True)


	return render(request, template_name, {'owned':owned_parts})


def view_product(request, template_name="view-product.html", pk=None):

	if not request.user.is_authenticated():
		raise Http404


	product_obj = get_object_or_404(Product, pk=pk)
	
	

	product_form = ProductForm(request.POST or None, request.FILES or None, instance=product_obj)

	try:
		requested_by = TransactionItem.objects.get(product=product_obj)
	except:
		requested_by=None

	if product_form.is_valid():

		product_form.save()
		messages.success(request, "Product saved")
		return redirect('mainapp:owned-parts')
		
	return render(request, template_name, {'form':product_form, 'requested_by':requested_by, 'product':product_obj})

def requested_parts(request, template_name="requested-parts.html"):

	requested_parts = TransactionItem.objects.filter(recepient=request.user)

	return render(request, template_name, {'requested':requested_parts})


def request_product(request):
	if not request.user.is_authenticated():
		raise Http404
	
	data=dict()

	product_id = request.GET.get('product_id')
	requested_part = get_object_or_404(Product, pk=product_id)

	if requested_part.is_active:
		if not requested_part.is_available:
			
			try:

				transaction_item = TransactionItem.objects.get(product=requested_part)
				data['has_error'] = False

				if transaction_item.recepient == request.user:
					data['withdraw_request'] = True
					data['make_request'] = False
					data['has_error'] = False
					requested_part.is_available = True
					requested_part.save()
				else:
					data['requested_by'] = transaction_item.recepient.username
					data['has_error'] = True
					transaction_item=None

			except:
				transaction_item=None

			if transaction_item is not None:
				transaction_item.delete()

		else:
			 data['make_request'] = True
			 data['withdraw_request'] = False 
			 data['has_error'] = False
			 requested_part.is_available = False
			 requested_part.save()
			 transaction_item = TransactionItem()
			 transaction_item.recepient = request.user
			 transaction_item.product = requested_part
			 transaction_item.save()

	return JsonResponse(data)





def confirm_request(request):

	if not request.user.is_authenticated:
		raise Http404

	data = dict()

	if request.method == "POST":
		product_id_obj = None
		
		try:
			product_id_obj = request.session['product_id_ref']
			product_obj = Product.objects.get(id=product_id_obj)
			form = TransactionForm(request, request.POST, instance=product_obj)
		except:
			product_id_obj = None
		
		if form.is_valid():
			part = form.save(commit=False)
			part.is_available=False
			part.is_active = False
			part.save()
			data['form_is_valid'] = True

		else:
			data['form_is_valid'] = False
			data['form-errors'] = form.errors
			


	else:
		
		product_id = request.GET['product_id']
		if product_id:
			product_obj = Product.objects.get(id=int(product_id))

			form = TransactionForm(request, instance=product_obj)

			if product_obj:
				transaction = TransactionItem.objects.get(product=product_obj)

				if transaction:
					data['title'] = product_obj.title
					data['description'] = product_obj.description
					data['recepient_names'] = transaction.recepient.first_name + " " + transaction.recepient.last_name
					data['recepient_email'] = transaction.recepient.email
					data['recepient_username'] = transaction.recepient.username


	data['html_form'] = render_to_string('transaction_form.html', {'form':form}, request=request)


	return JsonResponse(data)


def revoke_request(request):
	if not request.user.is_authenticated:
		raise Http404

	data = dict()
	if request.method == "POST":
		product_id_obj = None
		
		try:
			product_id_obj = request.session['product_id_ref']
			product_obj = Product.objects.get(id=product_id_obj)
			form = RevokeForm(request, request.POST, instance=product_obj)
			trans_obj = TransactionItem.objects.get(product=product_obj)
		except:
			product_id_obj = None
		
		if form.is_valid():
			part = form.save(commit=False)
			part.is_available=True
			part.is_active = True
			trans_obj.delete()
			part.save()
			data['form_is_valid'] = True

		else:
			data['form_is_valid'] = False
			data['form-errors'] = form.errors
			


	else:
		
		product_id = request.GET['product_id']
		if product_id:
			product_obj = Product.objects.get(id=int(product_id))

			form = RevokeForm(request, instance=product_obj)

			if product_obj:
				transaction = TransactionItem.objects.get(product=product_obj)

				if transaction:
					data['title'] = product_obj.title
					data['description'] = product_obj.description
					data['recepient_names'] = transaction.recepient.first_name + " " + transaction.recepient.last_name
					data['recepient_email'] = transaction.recepient.email
					data['recepient_username'] = transaction.recepient.username


	data['html_form'] = render_to_string('revoke_form.html', {'form':form}, request=request)



	return JsonResponse(data)



def add_product(request, template_name="view-product.html"):


	if not request.user.is_authenticated():
		raise Http404

	form = ProductForm(request.POST or None, request.FILES or None)


	if form.is_valid():
		product = form.save(commit=False)
		product.owner = request.user
		product.save()
		messages.success(request, "Product Saved")

		return redirect('mainapp:owned-parts')



	return render(request, template_name, {'form':form})

def delete_product(request, pk=None):

	product_obj = get_object_or_404(Product, pk=pk)

	if not request.user.is_authenticated() and product_obj.owner != request.user:
		raise Http404

	trans_obj = None
	try:
		trans_obj = TransactionItem.objects.get(product=product_obj)
		trans_obj.delete()
	except:
		trans_obj = None

	product_obj.is_active = False
	product_obj.is_available = False
	product_obj.save()

	messages.success(request, "Product Deleted")



	return redirect('mainapp:owned-parts')

	