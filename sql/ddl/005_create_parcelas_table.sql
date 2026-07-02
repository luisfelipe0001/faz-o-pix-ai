CREATE TABLE IF NOT EXISTS parcelas (
    id UUID PRIMARY KEY,
    emprestimo_id UUID NOT NULL,
    numero_parcela INT NOT NULL,
    valor_parcela DECIMAL(10, 2) NOT NULL,
    data_vencimento DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'pendente',
    data_recebimento DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (emprestimo_id) REFERENCES emprestimos(id) ON DELETE CASCADE
);

CREATE INDEX idx_parcelas_emprestimo_id ON parcelas(emprestimo_id);
CREATE INDEX idx_parcelas_status ON parcelas(status);
