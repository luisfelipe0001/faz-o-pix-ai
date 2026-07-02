-- Adicionar coluna cartao_id à tabela emprestimos
ALTER TABLE emprestimos
ADD COLUMN cartao_id UUID;

-- Adicionar foreign key para cartoes
ALTER TABLE emprestimos
ADD CONSTRAINT fk_emprestimos_cartao_id
FOREIGN KEY (cartao_id) REFERENCES cartoes(id) ON DELETE SET NULL;

-- Adicionar index
CREATE INDEX idx_emprestimos_cartao_id ON emprestimos(cartao_id);
