from django.utils.deprecation import MiddlewareMixin
from mainapp.models import Product

class ReferMiddleware(MiddlewareMixin):


	def process_request(self, request):
		
		product_id = request.GET.get('product_id')
		
		
		try:
			obj = Product.objects.get(id=product_id)
			
		except:
			obj = None

		if obj:
			request.session['product_id_ref'] = obj.id
			print("Session Variable Created. Id Number: " + str(request.session['product_id_ref']))

			
