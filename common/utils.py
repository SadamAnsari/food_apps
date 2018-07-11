import random
import string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader, Context
from django.utils.html import strip_tags
# from apps.emails.models import Email


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def send_templated_email(subject, email_template_name, email_context, recipients,
                         sender=None, bcc=None, fail_silently=True, files=None):

    c = Context(email_context)
    if not sender:
        sender = settings.DEFAULT_FROM_EMAIL

    template = loader.get_template(email_template_name)

    text_part = strip_tags(template.render(c))
    html_part = template.render(c)

    if type(recipients) == str:
        if recipients.find(','):
            recipients = recipients.split(',')
    elif type(recipients) != list:
        recipients = [recipients, ]

    msg = EmailMultiAlternatives(subject,
                                 text_part,
                                 sender,
                                 recipients,
                                 bcc=bcc)
    msg.attach_alternative(html_part, "text/html")

    if files:
        if type(files) != list:
            files = [files, ]
        for file in files:
            msg.attach_file(file)
    # email_record = Email.objects.create(sender=sender, receiver='; '.join(msg.recipients()),
    #                                     subject=msg.subject, body=msg.body)
    sent_flag = msg.send(fail_silently)
    if sent_flag:
        return True
    else:
        # email_record.sent = False
        # email_record.save()
        return False



