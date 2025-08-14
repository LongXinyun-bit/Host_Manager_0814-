## Host Manager（后端 API，Django + Celery）

### Introduction
一个可靠的主机管理后端，提供城市/机房/主机的增删改查、主机连通性探测（ping）、定时密码轮换与统计、请求耗时统计等能力，开箱即用并附带自动化测试。

### 技术栈
- Python 3
- Django 4 + Django Admin
- Django REST framework（DRF）
- Celery + django-celery-beat（定时任务），Redis 作为 broker/result（本地默认 eager 同步执行便于测试）
- cryptography（对称加密存储 root 密码）
- ping3（ICMP 探测）
- pytest + pytest-django（测试）

### Implementation
1) 设计主机管理系统（城市、机房、主机等模型）
   - 模型文件：`hosts/models.py`
   - 模型：`City`、`IDC`、`Host`、`HostStats`（按城市+机房维度的每日统计数据）

2) 提供对应模型的增删改查接口；提供一个 API 用于探测主机是否 ping 可达
   - 路由前缀：`/api/`
   - CRUD：
     - 城市：`/api/cities/`
     - 机房：`/api/idcs/`
     - 主机：`/api/hosts/`
     - 统计只读：`/api/stats/`
   - Ping API（动作接口）：
     - `POST /api/hosts/{id}/ping/`，返回 `ok`、`rtt_ms` 并回写至主机表
   - 代码位置：`hosts/views.py`、`hosts/serializers.py`、`hosts/urls.py`

3) 维护每台主机的 root 密码，每隔 8 小时真实地随机修改每台主机的密码并加密记录
   - 创建/更新主机时，使用 `root_password` 明文入参；后端用对称加密写入 `Host.root_password_encrypted`，不会保存明文
   - 定时任务：`hosts.tasks.rotate_all_host_passwords` 随机生成新密码并加密保存（本地 eager 可立即调用；生产由 beat 每 8 小时触发）
   - 加/解密与随机密码工具：`hosts/utils.py`（基于 `cryptography.Fernet`）
   - 说明：笔试默认要求为“随机轮换并加密记录在库”；如需“SSH 登入目标机实际修改系统密码”，可按需扩展

4) 每天 00:00 按城市和机房维度统计主机数量，并把统计数据写入数据库
   - 定时任务：`hosts.tasks.aggregate_daily_host_counts` 写入 `HostStats`
   - 查询接口：`GET /api/stats/`

5) 实现一个中间件，统计每个请求的请求耗时
   - 中间件：`hosts.middleware.RequestTimingMiddleware`
   - 效果：每个响应添加头 `X-Request-Time-ms: <耗时毫秒>`

