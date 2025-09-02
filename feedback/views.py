from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.translation import get_language
from django.shortcuts import get_object_or_404
from .models import FeedbackAction, FeedbackSubmission

@require_POST
def feedback_submit(request):
    action_slug = request.POST.get("action_slug") or ""
    name = (request.POST.get("name") or "").strip()
    phone = (request.POST.get("phone") or "").strip()
    page = request.POST.get("page") or request.META.get("HTTP_REFERER") or ""

    if not name or not phone:
        return HttpResponseBadRequest("name/phone required")

    action = FeedbackAction.objects.filter(slug=action_slug).first()

    sub = FeedbackSubmission.objects.create(
        action=action,
        name=name,
        phone=phone,
        page=page,
        locale=get_language() or "",
    )

    msg = (action.success_message if action and action.success_message else "Спасибо! Мы свяжемся с вами.")
    return JsonResponse({"ok": True, "message": msg})
