# 主机管理系统 (Django + DRF + Celery)

功能点：
- 城市、机房、主机模型及 CRUD API
- 主机 ping 探测 API：POST /api/hosts/{id}/ping/
- 维护 root 密码，使用对称加密保存；每 8 小时自动轮换
- 每天 00:00 按城市+机房统计主机数量写入数据库
- 中间件统计每个请求耗时，返回头 `X-Request-Time-ms`

## 快速开始

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 任务执行
- 本地默认 `CELERY_TASK_ALWAYS_EAGER=True`，调用即执行。
- 手动触发：
```bash
python manage.py shell -c "from hosts.tasks import rotate_all_host_passwords, aggregate_daily_host_counts; rotate_all_host_passwords.delay(); aggregate_daily_host_counts.delay()"
```

## API 示例
- 创建城市：POST /api/cities/ {"name":"深圳"}
- 创建机房：POST /api/idcs/ {"name":"A1","city":1}
- 创建主机：POST /api/hosts/ {"hostname":"web-1","ip":"192.168.1.10","city":1,"idc":1,"root_password":"Init@123"}
- Ping 主机：POST /api/hosts/{id}/ping/
- 统计查询：GET /api/stats/

## 测试
```bash
pytest -q
``` 