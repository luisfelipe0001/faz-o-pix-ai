CREATE TABLE IF NOT EXISTS cartoes (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    tipo_pagamento_id UUID NOT NULL,
    banco VARCHAR(255),
    digitos_finais VARCHAR(4),
    apelido VARCHAR(255),
    descricao VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (tipo_pagamento_id) REFERENCES tipos_pagamento(id) ON DELETE RESTRICT
);

CREATE INDEX idx_cartoes_user_id ON cartoes(user_id);
CREATE INDEX idx_cartoes_tipo_pagamento_id ON cartoes(tipo_pagamento_id);
