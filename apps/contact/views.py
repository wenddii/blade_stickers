from django.views.generic import FormView
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from .forms import ContactForm
from .models import ContactMessage


class ContactView(FormView):
    template_name = 'contact/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact:contact')

    def form_valid(self, form):
        contact_msg = form.save()
        
        # Handle AJAX requests
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Thank you! Your message has been received. We will contact you shortly on WhatsApp or Phone.'
            })

        messages.success(
            self.request, 
            'Thank you! Your message has been sent successfully. We will get back to you shortly.'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors.as_json()
            }, status=400)
            
        messages.error(
            self.request,
            'Please fix the errors in the form below.'
        )
        return super().form_invalid(form)
