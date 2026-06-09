from django.core.mail import send_mail

send_mail(
    subject='Library Test',
    message='Email configuration works!',
    from_email='roshankarki549@gmail.com',
    recipient_list=['rosan123ab@gmail.com'],
    fail_silently=False,
)