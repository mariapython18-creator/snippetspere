from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CollaborationRequestForm
from django.http import HttpResponseForbidden, JsonResponse
from sharing.models import CustomUser
from .models import CollaborationRequest, DiscussionSpace, DiscussionMessage

from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseForbidden
from .forms import ExpertForm
from .models import Expert


class Experts(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.role not in ['developer', 'collaborator']:
            return HttpResponseForbidden("Access Denied: You do not have permission to view this page.")

        expert, created = Expert.objects.get_or_create(
            user=request.user,
            defaults={
                'full_name': request.user.get_full_name() or '',
                'designation': '',
                'email_id': request.user.email or '',
                'contact': '',
                'linkedin': '',
                'skill': '',
                'experience': 0,  # ✅ Give default numeric value
                'bio': '',
                'available': True,
            }
        )
        form = ExpertForm(instance=expert)
        return render(request, 'expert.html', {'form': form})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.role not in ['developer', 'collaborator']:
            return HttpResponseForbidden("Access Denied: You do not have permission to perform this action.")

        expert = Expert.objects.filter(user=request.user).first()
        form = ExpertForm(request.POST,request.FILES, instance=expert)
        if form.is_valid():
            expert = form.save(commit=False)
            expert.user = request.user
            expert.save()
            return render(request,'reply.html')
        return render(request, 'expert.html', {'form': form})


class Expertslist(View):
    def get(self, request):
        experts = Expert.objects.all()
        return render(request, 'expertslist.html', {'experts': experts})


class Collab(View):
    def get(self, request):
        form = CollaborationRequestForm()
        return render(request, 'collab.html', {'form': form})

    def post(self, request):
        form = CollaborationRequestForm(request.POST)
        if form.is_valid():
            collab = form.save(commit=False)
            collab.sender = request.user
            collab.receiver = request.user
            collab.save()
            return render(request, 'reply.html', {'message': 'Collaboration request submitted successfully!'})
        return render(request, 'collab.html', {'form': form})


class SenderDashboardView(View):
    def get(self, request):
        collaboration_requests = CollaborationRequest.objects.all()
        return render(request, 'sender_dashboard.html', {'collaboration_requests': collaboration_requests})


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import CollaborationRequest, DiscussionSpace, DiscussionMessage

@method_decorator(login_required, name='dispatch')
class DiscussionView(View):
    def get(self, request, id):
        collab_request = get_object_or_404(CollaborationRequest, id=id)
        space, _ = DiscussionSpace.objects.get_or_create(request=collab_request)

        if request.user not in space.participants.all():
            space.participants.add(request.user)

        messages = space.messages.select_related('sender').order_by('created_at')

        return render(request, 'discussion.html', {
            'request_obj': collab_request,
            'space': space,
            'messages': messages
        })

    def post(self, request, id):
        collab_request = get_object_or_404(CollaborationRequest, id=id)
        space, _ = DiscussionSpace.objects.get_or_create(request=collab_request)

        if request.user not in space.participants.all():
            space.participants.add(request.user)

        message_type = request.POST.get('message_type', '').strip()
        content = request.POST.get('content', '').strip()

        if not content:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)

        if message_type not in ['comment', 'suggestion', 'code']:
            return JsonResponse({'error': 'Invalid message type'}, status=400)

        msg = DiscussionMessage.objects.create(
            discussion=space,
            sender=request.user,
            message_type=message_type,
            content=content
        )

        return JsonResponse({
            'id': msg.id,
            'sender': msg.sender.username,
            'message_type': msg.message_type,
            'content': msg.content,
            'created_at': msg.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

