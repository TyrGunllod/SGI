-- Database initialization script for SGI (Sistema de Gestão Integrado)
-- This script creates all necessary tables for the application.
-- Run this script on a fresh PostgreSQL database to set up the schema.

-- Enable UUID extension for generating unique identifiers
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Users table: Stores user accounts and authentication data
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),  -- Unique user identifier
    username VARCHAR(50) UNIQUE NOT NULL,            -- Login username
    hashed_password TEXT NOT NULL,                    -- Secure password hash
    full_name VARCHAR(100),                           -- User's full name
    is_active BOOLEAN DEFAULT TRUE,                   -- Account active status
    is_admin BOOLEAN DEFAULT FALSE,                   -- Administrative privileges
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,  -- Creation timestamp
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP   -- Last update timestamp
);

-- 2. Applications table: Defines the mini-apps available in the system
CREATE TABLE applications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),  -- Unique app identifier
    name VARCHAR(100) UNIQUE NOT NULL,               -- Display name
    slug VARCHAR(100) UNIQUE NOT NULL,                -- URL-friendly identifier (e.g., 'financeiro', 'rh')
    description TEXT,                                 -- App description
    icon VARCHAR(50),                                 -- Icon name from Lucide/Radix
    is_active BOOLEAN DEFAULT TRUE,                   -- App active status
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP  -- Creation timestamp
);

-- 3. Pages table: Stores pages within applications
CREATE TABLE pages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),  -- Unique page identifier
    app_id UUID REFERENCES applications(id) ON DELETE CASCADE,  -- Parent application
    title VARCHAR(100) NOT NULL,                      -- Page title
    path VARCHAR(255) NOT NULL,                       -- Internal route or imported HTML URL
    is_external BOOLEAN DEFAULT FALSE,                -- If true, loads via iframe
    html_content TEXT,                                -- HTML content if imported
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP  -- Creation timestamp
);

-- 4. Permissions table: Access Control List (ACL) for users on apps/pages
CREATE TABLE permissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),  -- Unique permission identifier
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,        -- User with permission
    app_id UUID REFERENCES applications(id) ON DELETE CASCADE,   -- Application
    page_id UUID REFERENCES pages(id) ON DELETE CASCADE,         -- Specific page (optional)
    can_view BOOLEAN DEFAULT TRUE,               -- View permission
    can_edit BOOLEAN DEFAULT FALSE,              -- Edit permission
    can_delete BOOLEAN DEFAULT FALSE,            -- Delete permission
    UNIQUE(user_id, app_id, page_id)             -- Prevent duplicate permissions
);

-- 5. Future: Session management and audit logs can be added here
CREATE TABLE refresh_tokens (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    token TEXT UNIQUE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(255) NOT NULL,
    resource VARCHAR(100),
    details JSONB,
    ip_address VARCHAR(45),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para performance
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_permissions_user ON permissions(user_id);
CREATE INDEX idx_pages_app ON pages(app_id);