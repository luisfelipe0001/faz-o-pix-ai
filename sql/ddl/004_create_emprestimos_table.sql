CREATE TABLE IF NOT EXISTS emprestimos (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    pessoa_id UUID NOT NULL,
    tipo_pagamento_id UUID NOT NULL,
    descricao VARCHAR(500) NOT NULL,
    data_compra DATE NOT NULL,
    valor_total DECIMAL(10, 2) NOT NULL,
    qtd_parcelas INT NOT NULL,
    status_geral VARCHAR(50) DEFAULT 'em_andamento',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (pessoa_id) REFERENCES pessoas(id) ON DELETE CASCADE,
    FOREIGN KEY (tipo_pagamento_id) REFERENCES tipos_pagamento(id) ON DELETE RESTRICT
);

CREATE INDEX idx_emprestimos_user_id ON emprestimos(user_id);
CREATE INDEX idx_emprestimos_pessoa_id ON emprestimos(pessoa_id);
