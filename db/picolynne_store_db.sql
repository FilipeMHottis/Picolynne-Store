-- =====================================================
-- SISTEMA DE VENDAS DE PICOLÉ (PDV)
-- MODELO BASEADO EM CATEGORIA COM 3 PREÇOS
-- =====================================================

-- =========================
-- CLIENT
-- =========================
CREATE TABLE client (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15),
    cpf_or_cnpj VARCHAR(18) UNIQUE,
    status BOOLEAN NOT NULL DEFAULT TRUE
);

-- =========================
-- CASHIER (CAIXA)
-- =========================
CREATE TABLE cashier (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    status BOOLEAN NOT NULL DEFAULT TRUE
);

-- =========================
-- CATEGORY
-- A categoria CONTÉM toda a regra de preço
-- =========================
CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,

    -- regras de quantidade
    min_quantity INTEGER NOT NULL,
    max_quantity INTEGER NOT NULL,

    -- regras de preço
    price_1 NUMERIC(10,2) NOT NULL, -- abaixo da quantidade mínima
    price_2 NUMERIC(10,2) NOT NULL, -- >= min e < max
    price_3 NUMERIC(10,2) NOT NULL, -- >= max

    status BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT chk_quantity_range
        CHECK (min_quantity < max_quantity)
);

-- =========================
-- PRODUCT
-- Produto NÃO possui preço
-- Produto POSSUI estoque
-- =========================
CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    status BOOLEAN NOT NULL DEFAULT TRUE,

    -- estoque disponível
    stock INTEGER NOT NULL DEFAULT 0,

    category_id INTEGER NOT NULL,

    CONSTRAINT fk_product_category
        FOREIGN KEY (category_id)
        REFERENCES category(id),

    CONSTRAINT chk_stock_non_negative
        CHECK (stock >= 0)
);

-- =========================
-- SALE
-- =========================
CREATE TABLE sale (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL,
    cashier_id INTEGER NOT NULL,
    date TIMESTAMP NOT NULL DEFAULT NOW(),
    total_items INTEGER NOT NULL,
    total_price NUMERIC(10,2) NOT NULL,

    CONSTRAINT fk_sale_client
        FOREIGN KEY (client_id)
        REFERENCES client(id),

    CONSTRAINT fk_sale_cashier
        FOREIGN KEY (cashier_id)
        REFERENCES cashier(id)
);

-- =========================
-- SALE_ITEM
-- Guarda o preço aplicado (histórico)
-- =========================
CREATE TABLE sale_item (
    id SERIAL PRIMARY KEY,
    sale_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    applied_unit_price NUMERIC(10,2) NOT NULL,
    subtotal NUMERIC(10,2) NOT NULL,

    CONSTRAINT fk_sale_item_sale
        FOREIGN KEY (sale_id)
        REFERENCES sale(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_sale_item_product
        FOREIGN KEY (product_id)
        REFERENCES product(id),

    CONSTRAINT chk_quantity_positive
        CHECK (quantity > 0)
);

-- =========================
-- ÍNDICES (performance)
-- =========================
CREATE INDEX idx_product_category ON product(category_id);
CREATE INDEX idx_sale_date ON sale(date);
CREATE INDEX idx_sale_cashier ON sale(cashier_id);
CREATE INDEX idx_sale_client ON sale(client_id);

-- =====================================================
-- FIM DO SCHEMA
-- =====================================================
