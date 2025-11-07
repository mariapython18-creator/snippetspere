from django import forms
from .models import CollaborationRequest


from django import forms
from .models import CollaborationRequest

from django import forms
from .models import Expert

class ExpertForm(forms.ModelForm):
    class Meta:
        model = Expert
        fields = [
            'full_name',
            'designation',
            'email_id',
            'contact',
            'linkedin',
            'skill',
            'experience',
            'bio',
            'available',
            'profile_image',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a short professional bio...'}),
            'linkedin': forms.URLInput(attrs={'placeholder': 'https://www.linkedin.com/in/yourprofile'}),
        }

class CollaborationRequestForm(forms.ModelForm):
    class Meta:
        model = CollaborationRequest
        exclude = ['sender', 'receiver', 'created_at']  # ✅ don't show these in the form

        labels = {
            'project_title': 'Project Title',
            'project_description': 'Project Description',
            'looking_for': 'Looking For',
            'need':'Need',
            'required_skills': 'Required Skills',
            'collaboration_type': 'Collaboration Type',
            'estimated_timeline': 'Estimated Timeline',
            'contact_email': 'Contact Email',
            'location': 'Location',
            'message': 'Additional Message (Optional)',
        }

        widgets = {
            'project_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your project title'}),
            'project_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Briefly describe your project idea and goals...'}),
            'looking_for': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Frontend Developer, UI Designer'}),
            'required_skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Python, Django, React'}),
            'collaboration_type': forms.Select(attrs={'class': 'form-select'}),
            'estimated_timeline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2 months, ongoing'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your contact email'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Kochi, India'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Say something to attract collaborators...'}),
        }
