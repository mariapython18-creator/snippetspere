from django.db import models
from sharing.models import CustomUser

from django.db import models
from django.conf import settings  # ✅ Best practice for referencing custom user

class Expert(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    email_id = models.EmailField()
    contact = models.CharField(max_length=15)
    linkedin = models.URLField(blank=True, null=True)
    skill = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    bio = models.TextField()
    available = models.BooleanField(default=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} - {self.skill}"


class CollaborationRequest(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_requests', on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    project_title = models.CharField(max_length=150)
    project_description = models.TextField()
    looking_for = models.CharField(max_length=150)
    required_skills = models.CharField(max_length=250)
    collaboration_type = models.CharField(
        max_length=50,
        choices=[
            ('Open Source', 'Open Source'),
            ('Startup Idea', 'Startup Idea'),
            ('College Project', 'College Project'),
            ('Learning Project', 'Learning Project'),
            ('Freelance', 'Freelance')
        ],
        default='Learning Project'
    )
    estimated_timeline = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_title


class DiscussionSpace(models.Model):
    request = models.OneToOneField(CollaborationRequest, on_delete=models.CASCADE, related_name='discussion_space')
    participants = models.ManyToManyField(CustomUser, related_name='discussion_spaces')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Discussion for: {self.request.project_title}"


class DiscussionMessage(models.Model):
    MESSAGE_TYPES = (
        ('comment', 'Comment'),
        ('suggestion', 'Suggestion'),
        ('code', 'Code'),
    )
    discussion = models.ForeignKey(DiscussionSpace, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender} [{self.message_type}] - {self.created_at}"
