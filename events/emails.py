from django.core.mail import send_mail
from django.template.loader import render_to_string

from wanawana.utils import get_base_url


def send_admin_link_on_event_creation(request, event):
    if not event.admin_email:
        return

    email_body = render_to_string("emails/new_event.txt", {
        "url_scheme": request.META["wsgi.url_scheme"],
        "base_url": get_base_url(request),
        "event_slug": event.slug,
        "event_admin_id": event.admin_id
    })

    send_mail("[WanaWana] the admin url for you event '%s'" % (event.title),
              email_body,
              'noreply@%s' % get_base_url(request),
              [event.admin_email]
             )


def send_admin_notification_of_answer_on_event(request, event, event_attending):
    if not event.admin_email or not event.send_notification_emails:
        return

    email_body = render_to_string("emails/event_attending_answer.txt", {
        "url_scheme": request.META["wsgi.url_scheme"],
        "base_url": get_base_url(request),
        "event_attending": event_attending,
        "event": event,
    })

    send_mail("[Wanawana] %s has answer '%s' to your event '%s'" % (event_attending.name, event_attending.choice, event.title),
             email_body,
             "noreply@%s" % get_base_url(request),
             [event.admin_email])


def send_admin_notification_of_answer_modification(request, event, event_attending, modifications):
    if not event.admin_email or not event.send_notification_emails or not modifications:
        return

    email_body = render_to_string("emails/event_attending_answer_modification.txt", {
        "url_scheme": request.META["wsgi.url_scheme"],
        "base_url": get_base_url(request),
        "event_attending": event_attending,
        "event": event,
        "modifications": modifications,
    })

    send_mail("[Wanawana] %s has modify his answer to your event '%s'" % (event_attending.name, event.title),
             email_body,
             "noreply@%s" % get_base_url(request),
             [event.admin_email])


def send_admin_notification_for_new_comment(request, event, comment):
    if not event.admin_email or not event.send_notification_emails:
        return

    email_body = render_to_string("emails/event_for_admin_new_comment.txt", {
        "url_scheme": request.META["wsgi.url_scheme"],
        "base_url": get_base_url(request),
        "event": event,
        "comment": comment,
    })

    send_mail("[Wanawana] new comment by %s to your event '%s'" % (comment.name, event.title),
             email_body,
             "noreply@%s" % get_base_url(request),
             [event.admin_email])
