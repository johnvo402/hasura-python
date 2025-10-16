CREATE TABLE account (
    id              BIGSERIAL PRIMARY KEY,
    username        VARCHAR(100) NOT NULL UNIQUE,
    email           VARCHAR(255) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    full_name       VARCHAR(255),
    role            VARCHAR(50) DEFAULT 'any',
    is_active       BOOLEAN DEFAULT TRUE,
    last_login_at   timestamptz ,
    created_at      timestamptz  DEFAULT NOW(),
    updated_at      timestamptz  DEFAULT NULL
);
