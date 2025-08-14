### 使用技术栈：
python, django, celery

### 笔试题目：
1. 设计一个主机管理系统，用于管理企业内部的主机，包含主机、城市、机房等模型
2. 提供对应模型的增删改查接口；提供一个 API，用于探测主机是否 ping 可达
3. 需维护每台主机的 root 密码，每隔8小时真实地随机修改每台主机的密码并加密记录
4. 每天 00:00 按城市和机房维度统计主机数量，并把统计数据写入数据库
5. 实现一个中间件，统计每个请求的请求耗时

### 已完成
- **环境**: 创建虚拟环境，安装 Django、DRF、Celery、Redis、Cryptography、django-environ、django-celery-beat、ping3、pytest。
- **项目结构**: 初始化 `host_manager` 项目与 `hosts` 应用。
- **模型**: `City`、`IDC`、`Host`、`HostStats`。
- **接口**:
  - CRUD: `cities/`、`idcs/`、`hosts/`、统计只读 `stats/`
  - Ping: `POST /api/hosts/{id}/ping/`
- **中间件**: 统计耗时，响应头 `X-Request-Time-ms`。
- **密码管理**: 对称加密保存 root 密码，提供创建/更新时写入；定时任务每 8 小时轮换（本地同步执行）。
- **统计任务**: 每天 00:00 生成城市+机房维度主机数量。
- **管理后台**: 注册所有模型。
- **测试**: 端到端用例覆盖 CRUD、Ping、密码轮换与统计、耗时中间件。结果：`1 passed in 0.61s`

### 如何运行
- 启动
  - 创建/激活虚拟环境，安装依赖：
    ```bash
    cd /Users/a1-6/Documents/Cursor/腾讯后端题_host_manager
    source .venv/bin/activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver
    ```
- API 前缀为 `/api/`：
  - `POST /api/cities/`，`POST /api/idcs/`
  - `POST /api/hosts/`，字段示例：`{"hostname":"web-1","ip":"192.168.1.10","city":1,"idc":1,"root_password":"Init@123"}`
  - `POST /api/hosts/{id}/ping/`
  - `GET /api/stats/`
- 手动触发 Celery 任务（本地同步执行）：
  ```bash
  python manage.py shell -c "from hosts.tasks import rotate_all_host_passwords, aggregate_daily_host_counts; rotate_all_host_passwords.delay(); aggregate_daily_host_counts.delay()"
  ```

### 提交
- 已准备 `README.md` 与 `requirements.txt`，你可直接初始化 git 并推送：
  ```bash
  cd /Users/a1-6/Documents/Cursor/腾讯后端题_host_manager
  git init
  git add .
  git commit -m "host_manager: 初始实现(模型/API/中间件/任务/测试)"
  git branch -M main
  git remote add origin <你的仓库URL>
  git push -u origin main
  ```

- 代码位置（关键文件）：
  - `host_manager/settings.py`：启用 DRF、定时任务、中间件与时区
  - `host_manager/celery.py`：Celery 应用
  - `hosts/models.py`、`hosts/serializers.py`、`hosts/views.py`、`hosts/urls.py`
  - `hosts/tasks.py`：密码轮换与每日统计
  - `hosts/middleware.py`：请求耗时
  - `hosts/tests.py`：端到端测试

- 说明：
  - 生产环境建议将加解密密钥使用 `KMS/HSM` 或独立密钥，不要由 `SECRET_KEY` 派生。
  - 定时策略在生产中用 `django-celery-beat` 面板配置：密码轮换每 8 小时、统计每天 00:00。