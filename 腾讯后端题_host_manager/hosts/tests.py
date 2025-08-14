from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone

from .models import City, IDC, Host, HostStats
from .tasks import rotate_all_host_passwords, aggregate_daily_host_counts


class HostManagerE2ETest(APITestCase):
    def setUp(self):
        self.city = City.objects.create(name='深圳')
        self.idc = IDC.objects.create(name='A1', city=self.city)

    def test_city_idc_host_crud_and_ping_and_tasks(self):
        # 创建主机
        resp = self.client.post('/api/hosts/', {
            'hostname': 'web-1',
            'ip': '192.168.1.10',
            'city': self.city.id,
            'idc': self.idc.id,
            'root_password': 'Init@123',
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED, resp.content)
        host_id = resp.data['id']

        # 列表
        resp = self.client.get('/api/hosts/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'] if isinstance(resp.data, dict) and 'count' in resp.data else len(resp.data), 1)

        # Ping（离线网络环境下 rtt 可能为 None，但接口应 200）
        resp = self.client.post(f'/api/hosts/{host_id}/ping/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('ok', resp.data)

        # 轮换密码（任务）
        rotate_all_host_passwords.delay()
        self.assertTrue(Host.objects.get(id=host_id).password_updated_at)

        # 统计数据（任务）
        aggregate_daily_host_counts.delay()
        today = timezone.localdate()
        self.assertTrue(HostStats.objects.filter(stat_date=today, city=self.city, idc=self.idc).exists())

        # 中间件：响应头包含时间
        resp = self.client.get('/api/hosts/')
        self.assertIn('X-Request-Time-ms', resp.headers)
