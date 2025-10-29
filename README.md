# 🚀 hasura-python

`hasura-python` là một project tích hợp **Hasura GraphQL Engine** với **Python FastAPI**,  
cho phép mở rộng logic backend thông qua **Actions**, **Events**, và **Scheduled Triggers**.  
Mục tiêu của project là giúp Hasura có thể gọi đến các hàm Python để xử lý nghiệp vụ phức tạp  
mà database không đảm nhiệm được.

---

## 📦 Tổng quan

- Hasura: Quản lý metadata, migration, trigger, action, và schema GraphQL.  
- FastAPI (webhook): Xử lý logic khi Hasura gọi webhook.  
- Scripts: Bộ script hỗ trợ thao tác nhanh như migrate, rollback, seed, dump database, v.v.  
- Gateway (Traefik): Reverse proxy cho các service.  

---

## 📂 Cấu trúc thư mục

```
hasura-python
├── hasura/                     # Cấu hình metadata & migration của Hasura
│   ├── metadata/               # Toàn bộ metadata của Hasura
│   │   ├── databases/          # Định nghĩa database, tables và metadata liên quan
│   │   │   ├── database/
│   │   │   │   ├── tables/
│   │   │   │   │   ├── public_account.yaml
│   │   │   │   │   └── tables.yaml
│   │   │   └── databases.yaml
│   │   ├── actions.graphql     # Khai báo schema GraphQL cho Actions
│   │   ├── actions.yaml        # Cấu hình mapping endpoint webhook
│   │   ├── cron_triggers.yaml  # Định nghĩa các cron job (scheduled events)
│   │   ├── remote_schemas.yaml # (Tùy chọn) Kết nối với các GraphQL schema bên ngoài
│   │   ├── rest_endpoints.yaml # (Tùy chọn) Định nghĩa REST endpoints
│   │   └── version.yaml        # Phiên bản metadata
│   ├── migrations/             # Thư mục chứa các migration SQL
│   │   └── database/
│   │       └── 1760615777829_create_account/
│   │           ├── up.sql
│   │           └── down.sql
│   ├── seeds/                  # Dữ liệu mẫu (seed)
│   └── config.yaml             # Cấu hình Hasura CLI
│
├── scripts/                    # Các script tiện ích
│   ├── bootstrap               # Script khởi tạo ban đầu
│   ├── docker-entrypoint-initdb.d/
│   │   └── 000_createdb.sql    # Tạo database khi container khởi động
│   ├── console.sh              # Mở Hasura console
│   ├── migrate.sh              # Chạy migration
│   ├── migrate-rollback.sh     # Rollback migration
│   ├── pgdump.sh               # Xuất dữ liệu PostgreSQL
│   ├── test.sh                 # Chạy test đơn giản
│   └── get-version.sh          # Lấy version Hasura
│
├── src/
│   ├── gateway/                # Gateway reverse proxy (Traefik)
│   │   ├── acme.json
│   │   ├── Dockerfile
│   │   └── traefik.yml
│   │
│   └── webhook/                # Ứng dụng FastAPI xử lý webhook từ Hasura
│       ├── actions/            # Action handlers (Hasura Actions)
│       │   ├── login_action/
│       │   │   ├── handler.py
│       │   │   └── models.py
│       │   ├── profile/
│       │   │   └── handler.py
│       │   ├── handler.py
│       │   ├── models.py
│       │   └── wrapper.py
│       │
│       ├── event/              # Event triggers (insert/update/delete)
│       │   ├── create_account/
│       │   │   └── handler.py
│       │   ├── handler.py
│       │   ├── models.py
│       │   └── wrapper.py
│       │
│       ├── scheduled/          # Scheduled (cron triggers)
│       │   ├── test_cron/
│       │   │   └── handler.py
│       │   ├── handler.py
│       │   ├── models.py
│       │   └── wrapper.py
│       │
│       ├── auth/               # Xử lý xác thực người dùng
│       │   └── handler.py
│       │
│       ├── models/             # Định nghĩa các model Pydantic
│       │   └── account.py
│       │
│       ├── pkgs/               # Các package phụ trợ
│       │   └── session_variable.py
│       │
│       ├── utils/              # Hàm tiện ích: logging, database, result
│       │   ├── logger.py
│       │   ├── database.py
│       │   └── result.py
│       │
│       ├── main.py             # Entry point FastAPI
│       ├── routes.py           # Khai báo routes webhook
│       └── config.py           # Cấu hình ứng dụng
│
├── docker-compose.yaml          # Docker Compose chính
├── docker-compose.dev.yaml      # Docker Compose môi trường phát triển
├── docker-compose.staging.yaml  # Docker Compose môi trường staging
├── docker-compose.postgres.yaml # Docker Compose chỉ cho PostgreSQL
├── Makefile                     # Tập hợp lệnh tiện dụng
├── pyproject.toml               # Cấu hình Poetry
├── poetry.lock                  # Lock dependencies
├── .env.example                 # File mẫu biến môi trường
├── .gitignore                   # Bỏ qua file không cần commit
└── README.md                    # Tài liệu dự án
```

---

## ⚙️ Cách chạy dự án

1. Cài đặt Docker & Docker Compose.  
2. Sao chép file `.env.example` thành `.env` và chỉnh sửa thông tin.  
3. Chạy lệnh:
   ```bash
   make dev SERVICE="hasura webhook"
   ```
4. Truy cập:
   - Hasura Console: http://localhost:8080
   - FastAPI Webhook: http://localhost:8080

---

## 🧩 Thành phần chính

| Thành phần | Mô tả |
|-------------|--------|
| Hasura | Xây dựng GraphQL tự động từ database |
| FastAPI | Xử lý webhook Actions, Events, và Cron |
| PostgreSQL | Database chính |
| Traefik | Reverse proxy và SSL management |

---

## 🧠 Ghi chú

- Logic nghiệp vụ nên đặt trong `src/webhook/`.  
- Không nên viết logic phức tạp trong Hasura, hãy để Hasura gọi webhook FastAPI.  
- Có thể mở rộng thành microservice bằng cách tách các action/event riêng.
