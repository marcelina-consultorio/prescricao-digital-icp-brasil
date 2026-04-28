# Modelos de Prescrição Médica Assinada Digitalmente

## Registro de Modelos Disponíveis

Estes são os modelos de prescrição criados e validados para reutilização em futuras prescrições.

---

## 1. Modelo: Receita Médica Simples (Medicamentos)

**Arquivo Template:** `tania_manipulados_corrigido.py`

**Descrição:** Prescrição de medicamentos manipulados com layout profissional, assinatura ICP-Brasil e validação.

**Características:**
- Cabeçalho azul gradiente com dados do médico
- Linha dourada separadora
- Informações do paciente (nome, CPF, data)
- Seção de medicamentos com até 4 itens
- Página 2 com: Comprovante de assinatura + QR Code + Instruções de validação
- Assinatura digital com pyHanko (certificado A1)
- Hash SHA-256 do documento
- URL copiável para validação no ITI

**Fluxo:**
1. Gera PDF com 2 páginas (prescrição + validação)
2. Assina com pyHanko
3. Extrai dados da assinatura (hash, data, certificado)
4. Hospeda PDF assinado
5. Gera PDF final com URL correta na caixa de instruções
6. Hospeda PDF final

**Próximas Prescrições:**
- Copiar o script `tania_manipulados_corrigido.py`
- Substituir dados do paciente (nome, CPF)
- Substituir medicamentos (nome, forma, posologia)
- Executar o script

---

## 2. Modelo: Pedido de Exames Laboratoriais

**Arquivo Template:** `pedido_exames_ASSINADO.pdf` + `pedido_exames_VALIDACAO.pdf`

**Descrição:** Solicitação de exames de sangue com assinatura ICP-Brasil.

**Características:**
- Layout profissional com cabeçalho azul
- Lista de exames solicitados
- Assinatura digital com pyHanko
- Página 2 com QR Code + instruções de validação

**Exames Incluídos (Exemplo - Tânia):**
- Hemograma completo
- Bioquímica básica
- Hepatograma
- Lipidograma
- Apolipoproteína B (ApoB)
- Apolipoproteína A (ApoA)
- TSH, T4 livre
- Ureia, Creatinina
- PCR relativa de alta sensibilidade
- Indican (urinário para disbiose)

---

## 3. Modelo: Receita Creon (Medicamento Específico)

**Arquivo Template:** `receita_1_creon_ASSINADA.pdf` + `receita_1_creon_VALIDACAO.pdf`

**Descrição:** Prescrição de Creon 10.000 UI com assinatura ICP-Brasil.

**Características:**
- Layout profissional com cabeçalho azul
- Medicamento: Creon 10.000 UI
- Posologia: 1 cápsula durante as refeições
- Assinatura digital com pyHanko
- Página 2 com QR Code + instruções de validação

---

## Estrutura Padrão de Prescrição

Todos os modelos seguem esta estrutura:

```
PÁGINA 1 — PRESCRIÇÃO
├── Header (Azul gradiente)
│   ├── Nome do médico
│   ├── Especialidades
│   └── CRM + RQE + Endereço
├── Linha Dourada
├── Informações do Paciente
│   ├── Nome
│   ├── CPF
│   └── Data
├── Título da Seção (Receituário / Solicitação)
├── Conteúdo (Medicamentos / Exames)
└── Footer com Assinatura

PÁGINA 2 — VALIDAÇÃO
├── Título: "Validação de Assinatura Digital ICP-Brasil"
├── Comprovante de Assinatura
│   ├── Assinado por: GUILI PECH
│   ├── CPF: ***.534.207-**
│   ├── Data/hora: DD/MM/YYYY HH:MM:SS BRT
│   ├── Certificado: 0x11de2604254bf62c
│   ├── Emissor: AC SOLUTI Multipla v5 G2 — ICP-Brasil
│   ├── Algoritmo: PAdES / SHA-256 / RSA
│   └── Hash SHA-256: [hash completo]
├── Selo: ASSINATURA ELETRÔNICA QUALIFICADA — ICP-Brasil
├── QR Code → https://validar.iti.gov.br
├── Instruções Passo a Passo (4 passos)
├── URL Copiável (em caixa destacada)
├── Resultado Esperado (verde)
├── Alternativa de Validação (laranja)
└── Footer com Dados do Médico
```

---

## Credenciais e Configurações

**Certificado A1 (pyHanko):**
- Arquivo: `/home/ubuntu/upload/11de2604254bf62c(1).pfx`
- Senha: `Pd$Fg69pCbqi83D`
- Titular: GUILI PECH
- CPF: ***.534.207-**
- Emissor: AC SOLUTI Multipla v5 G2 — ICP-Brasil
- Número de Série: 0x11de2604254bf62c

**Hospedagem:**
- Comando: `manus-upload-file <arquivo.pdf>`
- Retorna: URL pública (CDN)

**Validação:**
- Portal: https://validar.iti.gov.br
- Método 1: Colar URL
- Método 2: Upload de arquivo
- Resultado: ASSINATURA ELETRÔNICA QUALIFICADA — ICP-Brasil

---

## Como Usar os Modelos

### Para Próxima Prescrição de Manipulados:

```bash
cd /home/ubuntu
cp tania_manipulados_corrigido.py nova_prescricao_manipulados.py
# Editar: nome do paciente, CPF, medicamentos
python3 nova_prescricao_manipulados.py
```

### Para Próximo Pedido de Exames:

Usar o mesmo fluxo do `tania_manipulados_corrigido.py`, mas com:
- Título: "SOLICITAÇÃO DE EXAMES"
- Conteúdo: Lista de exames em vez de medicamentos

### Para Próxima Receita Simples:

Usar o mesmo fluxo, mas com:
- Um único medicamento
- Posologia específica

---

## Dados Padrão do Médico

```
Nome: Dr. Guili Pech
CRM/RJ: 5286323-8
RQE: 12345 | RQE: 67890
Especialidades: Gastroenterologia | Hepatologia | Endoscopia Digestiva
Endereço: Av. das Américas, 3333 — Sala 1010, Barra da Tijuca — Rio de Janeiro/RJ
Telefone: (21) 9111-6980
```

---

## Próximas Melhorias

- [ ] Criar script genérico que aceita parâmetros (paciente, medicamentos, etc.)
- [ ] Integrar com n8n para automação
- [ ] Adicionar suporte para atestados médicos
- [ ] Adicionar suporte para laudos
- [ ] Criar dashboard com histórico de prescrições
- [ ] Implementar validação automática no ITI

---

## Registro de Prescrições Geradas

| Data | Paciente | Tipo | Status | URL |
|------|----------|------|--------|-----|
| 25/04/2026 | Tânia Maria Marinho Pita Nunes | Receita Creon | ✅ Assinada | https://files.manuscdn.com/user_upload_by_module/session_file/310519663444296140/aKLYbbSeYzldnEwo.pdf |
| 25/04/2026 | Tânia Maria Marinho Pita Nunes | Pedido Exames | ✅ Assinada | https://files.manuscdn.com/user_upload_by_module/session_file/310519663444296140/ZNAzKFafoRpWWLsz.pdf |
| 27/04/2026 | Tânia Maria Marinho Pita Nunes | Manipulados | ✅ Assinada | https://files.manuscdn.com/user_upload_by_module/session_file/310519663444296140/WwHMmrjJOkkfrCqc.pdf |

---

**Última Atualização:** 27/04/2026
**Status:** Modelos Validados e Prontos para Reutilização
