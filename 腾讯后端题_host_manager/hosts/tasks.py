from celery import shared_task
from django.db import transaction
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDate

from .models import Host, HostStats
from .utils import generate_random_password, encrypt_text


@shared_task
def rotate_all_host_passwords():
    now = timezone.now()
    with transaction.atomic():
        for host in Host.objects.select_for_update().all():
            new_password = generate_random_password()
            host.root_password_encrypted = encrypt_text(new_password)
            host.password_updated_at = now
            host.save(update_fields=['root_password_encrypted', 'password_updated_at', 'updated_at'])


@shared_task
def aggregate_daily_host_counts():
    today = timezone.localdate()
    # 统计按城市+机房的数量
    counts = (
        Host.objects.values('city', 'idc')
        .annotate(host_count=Count('id'))
        .order_by('city', 'idc')
    )
    with transaction.atomic():
        for item in counts:
            HostStats.objects.update_or_create(
                stat_date=today,
                city_id=item['city'],
                idc_id=item['idc'],
                defaults={'host_count': item['host_count']},
            ) 