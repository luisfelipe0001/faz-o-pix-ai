CREATE TABLE IF NOT EXISTS tipos_pagamento (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    nome VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_tipos_pagamento_user_id ON tipos_pagamento(user_id);
