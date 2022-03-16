from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import Reply


@receiver(post_save, sender=Reply)
def reply_added(sender, instance, created, **kwargs):
    if created:
        msg = EmailMultiAlternatives(
            subject='У вас новое сообщение с форума гиков',
            from_email='olga-olechka-5@yandex.ru',
            to=[f'{instance.reply_post.post_author.email}',]
        )

        html_content = render_to_string(
            'reply_added_letter.html',
            {'reply': instance})

        msg.attach_alternative(html_content, "text/html")
        msg.send()

    else:
        user = instance.reply_author
        subject = f"Ваш комментарий был одобрен и размещен на форуме"
        message = f'Ваш комментарий: "{instance.reply_text}" к объявлению "{instance.reply_post}" был одобрен и размещен на форуме.'
        user.email_user(subject, message)




