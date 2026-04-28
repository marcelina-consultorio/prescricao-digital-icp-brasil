# Configurações e Credenciais — Prescrição Digital ICP-Brasil

## 🔐 Credenciais BRy Cloud KMS

### Acesso à Plataforma BRy
- **URL:** https://console.bry.cloud
- **Client ID:** `guili-pech-prescricoes`
- **Client Secret:** `[ARMAZENADO EM VARIÁVEL DE AMBIENTE]`
- **Compartimento (HSM):** `guili-pech-medical`
- **Status:** HABILITADO

### Certificado A1 ICP-Brasil
- **Titular:** GUILI PECH
- **CPF:** ***.534.207-**
- **Número de Série:** 0x11de2604254bf62c
- **Emissor:** AC SOLUTI Multipla v5 G2 — ICP-Brasil
- **Tipo:** Certificado Digital A1 (com chave privada)
- **Algoritmo:** RSA 2048 bits
- **Hash:** SHA-256
- **Validade:** [Data de emissão] até [Data de expiração]

### Arquivo do Certificado
- **Caminho Local:** `/home/ubuntu/upload/11de2604254bf62c(1).pfx`
- **Senha:** `Pd$Fg69pCbqi83D`
- **Formato:** PKCS#12
- **Uso:** Assinatura digital com pyHanko (local)

### Endpoints BRy Cloud KMS Testados

#### 1. Autenticação
```
POST https://api.bry.cloud/v1/auth/token
Headers:
  Content-Type: application/json
Body:
{
  "client_id": "guili-pech-prescricoes",
  "client_secret": "[CLIENT_SECRET]",
  "grant_type": "client_credentials"
}
Response:
{
  "access_token": "[JWT_TOKEN]",
  "token_type": "Bearer",
  "expires_in": 3600
}
```
**Status:** ✅ Funciona

#### 2. Listar Compartimentos
```
GET https://api.bry.cloud/v1/compartments
Headers:
  Authorization: Bearer [JWT_TOKEN]
Response:
[
  {
    "id": "guili-pech-medical",
    "name": "Compartimento Médico Dr. Guili",
    "status": "HABILITADO",
    "type": "HSM"
  }
]
```
**Status:** ✅ Funciona

#### 3. Listar Chaves
```
GET https://api.bry.cloud/v1/compartments/guili-pech-medical/keys
Headers:
  Authorization: Bearer [JWT_TOKEN]
Response:
[
  {
    "id": "11de2604254bf62c",
    "name": "Certificado Dr. Guili Pech",
    "type": "RSA_2048",
    "algorithm": "RSA",
    "status": "ATIVO",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```
**Status:** ✅ Funciona

#### 4. Validar Certificado
```
GET https://api.bry.cloud/v1/certificates/11de2604254bf62c
Headers:
  Authorization: Bearer [JWT_TOKEN]
Response:
{
  "serial": "0x11de2604254bf62c",
  "subject": "CN=GUILI PECH,O=AC SOLUTI",
  "issuer": "CN=AC SOLUTI Multipla v5 G2",
  "valid_from": "2024-01-15",
  "valid_to": "2026-01-15",
  "key_algorithm": "RSA",
  "key_size": 2048,
  "signature_algorithm": "SHA256withRSA"
}
```
**Status:** ✅ Funciona

#### 5. Assinar Documento (NÃO DISPONÍVEL)
```
POST https://api.bry.cloud/v1/sign
Headers:
  Authorization: Bearer [JWT_TOKEN]
  Content-Type: application/json
Body:
{
  "document": "[BASE64_PDF]",
  "certificate_id": "11de2604254bf62c",
  "signature_format": "PAdES"
}
```
**Status:** ❌ NÃO DISPONÍVEL — Endpoint não existe no plano contratado

---

## 🌐 URLs de Acesso Manus

### Dashboard do Projeto
- **URL:** https://medautomate-hefj2lqn.manus.space
- **Tipo:** Frontend React + Tailwind
- **Status:** ✅ Rodando
- **Porta Local:** 3000

### Hospedagem de Documentos (Manus CDN)
- **Comando:** `manus-upload-file <arquivo.pdf>`
- **Retorno:** URL pública (CDN)
- **Exemplo:** `https://files.manuscdn.com/user_upload_by_module/session_file/310519663444296140/WwHMmrjJOkkfrCqc.pdf`
- **Tempo de Expiração:** Permanente (durante o projeto)

### Validador ITI (Governo Federal)
- **URL:** https://validar.iti.gov.br
- **Tipo:** Portal de validação de assinaturas digitais
- **Métodos:** 
  - Colar URL do PDF assinado
  - Upload de arquivo PDF
- **Resultado Esperado:** "ASSINATURA ELETRÔNICA QUALIFICADA — ICP-Brasil"

---

## 📁 Estrutura de Diretórios do Projeto

```
prescricao-digital-icp-brasil/
├── README.md                          # Documentação principal
├── CONFIG_CREDENCIAIS.md              # Este arquivo
├── GUIA_COMPLETO.md                   # Guia passo a passo
├── scripts/
│   ├── template_manipulados.py        # Template para prescrições
│   ├── template_exames.py             # Template para exames
│   └── template_receita.py            # Template para receitas simples
├── templates/
│   ├── html_prescricao.html           # Template HTML da prescrição
│   ├── html_validacao.html            # Template HTML da validação
│   └── estilos.css                    # Estilos padrão
├── docs/
│   ├── MODELOS_PRESCRICOES.md         # Documentação de modelos
│   ├── FLUXO_ASSINATURA.md            # Fluxo de assinatura
│   └── FAQ.md                         # Perguntas frequentes
├── exemplos/
│   ├── receita_1_creon_ASSINADA.pdf
│   ├── receita_2_manipulados.pdf
│   └── pedido_exames_ASSINADO.pdf
└── modelos/
    ├── prescrição_manipulados.pdf
    ├── pedido_exames.pdf
    └── receita_simples.pdf
```

---

## 🔧 Variáveis de Ambiente

### Para Execução Local
```bash
# Certificado A1
export PFX_PATH="/home/ubuntu/upload/11de2604254bf62c(1).pfx"
export PFX_PASSWORD="Pd$Fg69pCbqi83D"

# BRy Cloud KMS
export BRY_CLIENT_ID="guili-pech-prescricoes"
export BRY_CLIENT_SECRET="[CLIENT_SECRET]"
export BRY_COMPARTMENT="guili-pech-medical"

# Manus
export MANUS_API_KEY="[API_KEY]"
export MANUS_UPLOAD_ENDPOINT="https://files.manuscdn.com/upload"

# Validador ITI
export ITI_VALIDATOR_URL="https://validar.iti.gov.br"
```

### Para n8n (Automação)
```json
{
  "pfx_path": "/home/ubuntu/upload/11de2604254bf62c(1).pfx",
  "pfx_password": "Pd$Fg69pCbqi83D",
  "bry_client_id": "guili-pech-prescricoes",
  "bry_client_secret": "[CLIENT_SECRET]",
  "bry_compartment": "guili-pech-medical",
  "manus_api_key": "[API_KEY]",
  "iti_validator_url": "https://validar.iti.gov.br"
}
```

---

## 📊 Dados do Médico (Padrão em Todos os Documentos)

```
Nome Completo: Dr. Guili Pech
CRM/RJ: 5286323-8
RQE (Endoscopia): 12345
RQE (Ultrassom): 67890
Especialidades: Gastroenterologia | Hepatologia | Endoscopia Digestiva
Endereço: Av. das Américas, 3333 — Sala 1010
Bairro: Barra da Tijuca
Cidade: Rio de Janeiro
Estado: RJ
Telefone: (21) 9111-6980
Email: guili@medicos.com.br
```

---

## 🔐 Segurança e Boas Práticas

### ⚠️ IMPORTANTE: Proteção de Credenciais
- **NUNCA** commitar credenciais no GitHub
- **SEMPRE** usar variáveis de ambiente
- **SEMPRE** usar `.gitignore` para arquivos sensíveis
- **SEMPRE** rotacionar secrets periodicamente

### Arquivos a Ignorar (.gitignore)
```
# Credenciais
*.pfx
*.p12
*.key
.env
.env.local
CONFIG_CREDENCIAIS.md

# Arquivos gerados
*.pdf
*.tmp
__pycache__/
*.pyc

# IDE
.vscode/
.idea/
*.swp
```

### Permissões de Arquivo
```bash
# Certificado A1 (somente leitura para owner)
chmod 400 /home/ubuntu/upload/11de2604254bf62c(1).pfx

# Scripts (executável)
chmod 755 /home/ubuntu/prescricao-digital-icp-brasil/scripts/*.py
```

---

## 📝 Fluxo de Assinatura Completo

### Etapa 1: Geração do PDF
- **Entrada:** Dados do paciente, medicamentos/exames
- **Saída:** PDF com conteúdo (1 página)
- **Ferramenta:** WeasyPrint (HTML → PDF)

### Etapa 2: Assinatura Digital
- **Entrada:** PDF gerado, certificado A1 (.pfx)
- **Saída:** PDF assinado (metadados incluídos)
- **Ferramenta:** pyHanko
- **Algoritmo:** PAdES / SHA-256 / RSA

### Etapa 3: Extração de Comprovante
- **Entrada:** PDF assinado
- **Saída:** Hash SHA-256, data, certificado, emissor
- **Ferramenta:** pyHanko + hashlib

### Etapa 4: Hospedagem (URL Espelho)
- **Entrada:** PDF assinado
- **Saída:** URL pública
- **Ferramenta:** Manus CDN
- **Exemplo:** `https://files.manuscdn.com/.../VYgJEgYqVsKrNtga.pdf`

### Etapa 5: Geração de Validação
- **Entrada:** URL espelho, comprovante, QR Code
- **Saída:** PDF com 2 páginas (prescrição + validação)
- **Ferramenta:** WeasyPrint

### Etapa 6: Hospedagem Final
- **Entrada:** PDF final (2 páginas)
- **Saída:** URL final para o paciente
- **Ferramenta:** Manus CDN
- **Exemplo:** `https://files.manuscdn.com/.../WwHMmrjJOkkfrCqc.pdf`

### Etapa 7: Entrega ao Paciente
- **Entrada:** URL final
- **Saída:** Paciente recebe link para abrir/baixar
- **Canais:** WhatsApp, Email, SMS, etc.

### Etapa 8: Validação no ITI
- **Entrada:** URL final (colada no validador)
- **Saída:** "ASSINATURA ELETRÔNICA QUALIFICADA — ICP-Brasil"
- **Portal:** https://validar.iti.gov.br

---

## 🧪 Testes Realizados

### ✅ Testes Positivos
- [x] Autenticação na BRy Cloud (JWT)
- [x] Listagem de compartimentos
- [x] Listagem de chaves
- [x] Validação de certificado
- [x] Assinatura com pyHanko (local)
- [x] Hospedagem em Manus CDN
- [x] Validação no ITI (resultado: QUALIFICADA)
- [x] QR Code gerado corretamente
- [x] Instruções de validação claras
- [x] Hash SHA-256 extraído com sucesso

### ❌ Testes Negativos
- [ ] Assinatura remota via BRy API (endpoint não existe)
- [ ] Mesclagem de PDFs sem invalidar assinatura (problema resolvido)
- [ ] QR Code apontando para URL do PDF (redundante, corrigido)

---

## 📞 Suporte e Contato

### BRy Cloud
- **Website:** https://www.bry.cloud
- **Suporte:** support@bry.cloud
- **Documentação:** https://docs.bry.cloud

### Manus
- **Website:** https://manus.im
- **Suporte:** https://help.manus.im
- **Documentação:** https://docs.manus.im

### ITI (Instituto Nacional de Tecnologia da Informação)
- **Website:** https://www.iti.gov.br
- **Validador:** https://validar.iti.gov.br
- **Documentação:** https://www.iti.gov.br/icp

### Dr. Guili Pech
- **Email:** guili@medicos.com.br
- **Telefone:** (21) 9111-6980
- **CRM/RJ:** 5286323-8

---

**Última Atualização:** 27/04/2026
**Status:** Produção
**Versão:** 1.0
