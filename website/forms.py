from django import forms
from .models import ContactMessage, MembershipApplication, NewsletterSubscriber


class ContactForm(forms.ModelForm):
    """Contact form."""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+977-XXXXXXXXXX'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Message subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Your message here...'
            }),
        }


class MembershipForm(forms.ModelForm):
    """Membership application form."""
    
    class Meta:
        model = MembershipApplication
        fields = [
            'full_name', 'date_of_birth', 'gender', 'citizenship_number',
            'phone', 'email', 'address', 'ward_number', 'municipality',
            'district', 'province', 'membership_type', 'occupation',
            'monthly_income', 'nominee_name', 'nominee_relationship',
            'nominee_phone', 'photo', 'citizenship_document'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full name as per citizenship'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'citizenship_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Citizenship number'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mobile number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address (optional)'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Street address'
            }),
            'ward_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ward number'
            }),
            'municipality': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Municipality/Rural municipality'
            }),
            'district': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'District'
            }),
            'province': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Province'
            }),
            'membership_type': forms.Select(attrs={'class': 'form-select'}),
            'occupation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your occupation'
            }),
            'monthly_income': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Monthly income in NPR'
            }),
            'nominee_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nominee full name'
            }),
            'nominee_relationship': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Relationship with nominee'
            }),
            'nominee_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nominee phone number'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'citizenship_document': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
        }


class NewsletterForm(forms.ModelForm):
    """Newsletter subscription form."""
    
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
        }


class SearchForm(forms.Form):
    """Search form."""
    q = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search...',
            'name': 'q'
        })
    )
