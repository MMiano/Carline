
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save


import uuid

# Create your models here.

def upload_location(instance, filename):
	
		model_upload = str(instance)
		uploc = "%s/%s" %(model_upload, filename)

		return uploc


class UserProfile(models.Model):

	user = models.OneToOneField(User)
	profile_pic = models.ImageField(upload_to=upload_location, blank=True, null=True)
	pin = models.CharField(max_length=10, blank=False, null=False, unique=True)
	is_verified = models.BooleanField(default=False)

	def __str__(self):
		return self.user.email

	def get_absolute_url_view(self):
		return reverse('mainapp:view-profile', kwargs={'username':self.user.username})

	
	def get_absolute_url_edit(self):
		return reverse('mainapp:edit-profile', kwargs={'username':self.user.username})


class Product(models.Model):

	owner = models.ForeignKey(User)
	title = models.CharField(max_length=120, blank=False, null=False)
	# slug = models.SlugField(unique=True)
	description = models.TextField(blank=False, null=False)

	image1 = models.ImageField(upload_to=upload_location, blank=True, null=True)
	videofile= models.FileField(upload_to=upload_location, blank=True, null=True)

	is_available = models.BooleanField(default=True)
	is_active = models.BooleanField(default=True)

	timestamp = models.DateField(auto_now_add=True, auto_now=False)
	updated = models.DateField(auto_now_add=False, auto_now=True)

	class Meta:
		ordering =['-updated']


	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('mainapp:view-product', kwargs={'pk':self.pk})

	def get_absolute_url_delete(self):
		return reverse('mainapp:delete-product', kwargs={'pk':self.pk})





class TransactionItem(models.Model):
	recepient = models.ForeignKey(User) 
	product = models.OneToOneField(Product)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	class Meta:
		unique_together = ("recepient", "product")

	def __str__(self):
		return self.recepient.email


def generate_pin():
	pin_code = str(uuid.uuid4())[:11].replace("-","").lower()

	try:
		pin_qs_exist = UserProfile.objects.filter(pin=pin_code)
		generate_pin()
	except:
		return pin_code

	return pin_code



def pre_save_user_profile_receiver(sender, instance, *args, **kwargs):

	if not instance.pin:
		instance.pin = generate_pin()
		print("New Pin Generated. Pin is: " + str(instance.pin))


pre_save.connect(pre_save_user_profile_receiver, sender=UserProfile)