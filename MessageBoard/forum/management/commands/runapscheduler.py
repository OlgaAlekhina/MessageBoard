import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from datetime import datetime, timedelta
from forum.models import Post
from accounts.models import OneTimeCode
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


def weekly_mail():
    from_date = datetime.now() - timedelta(days=7)
    posts = Post.objects.filter(post_time__gte=from_date)
    if posts.exists():
        recipients = [user.email for user in User.objects.all()]
        msg = EmailMultiAlternatives(
            subject=f'Все объявления за прошедшую неделю на форуме гиков',
            from_email='olga-olechka-5@yandex.ru',
            to=recipients
        )

        html_content = render_to_string(
            'weekly_mail.html',
            {'posts': posts})

        msg.attach_alternative(html_content, "text/html")

        msg.send()

def clear_old():
    old_codes = OneTimeCode.objects.all().exclude(code_time__gt = datetime.now() - timedelta(minutes = 5))
    old_codes.delete()

def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            weekly_mail,
            trigger=CronTrigger(day_of_week="mon", hour="15", minute="00"),
            id="weekly_mail",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'weekly_mail'.")

        scheduler.add_job(
            clear_old,
            trigger=CronTrigger(minute="*/5"),
            id="clear_old",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'clear_old'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")