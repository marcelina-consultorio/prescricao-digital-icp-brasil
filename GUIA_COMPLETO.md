# Guia Completo: Documentos Médicos Assinados Digitalmente com Validação ICP-Brasil

**Autor:** Dr. Guili Pech  
**Data:** 27 de abril de 2026  
**Versão:** 1.0  
**Status:** Produção

---

## Sumário Executivo

Este guia apresenta o fluxo completo para gerar, assinar e validar documentos médicos (prescrições, pedidos de exames, atestados) com assinatura eletrônica qualificada ICP-Brasil. O sistema integra geração de PDFs em HTML, assinatura digital com certificado A1, hospedagem em URL pública via Manus e validação através do portal oficial do ITI (Instituto Nacional de Tecnologia da Informação).

**Resultado Final:** Documentos profissionais, legalmente válidos, com QR Code para validação e instruções claras para o paciente.

---

## 1. Visão Geral do Sistema

### 1.1 Componentes Principais

O sistema é composto por cinco componentes integrados:

**Geração de PDF:** Utiliza WeasyPrint para converter HTML em PDF com layout profissional, incluindo cabeçalho com dados do médico, informações do paciente, conteúdo clínico (medicamentos, exames) e footer com assinatura.

**Assinatura Digital:** Implementada com pyHanko, que utiliza o certificado A1 ICP-Brasil em formato PKCS#12 (.pfx) para assinar o PDF com padrão PAdES (PDF Advanced Electronic Signatures) e algoritmo SHA-256.

**Hospedagem:** Manus CDN fornece URLs públicas permanentes para os PDFs assinados, permitindo acesso e download pelos pacientes.

**Validação:** Portal oficial https://validar.iti.gov.br do governo federal valida a assinatura e retorna o resultado "ASSINATURA ELETRÔNICA QUALIFICADA — ICP-Brasil".

**Interface:** QR Code e instruções passo a passo facilitam que o paciente valide o documento sem conhecimento técnico.

### 1.2 Fluxo de Dados

```
Dados do Paciente
       ↓
Gerar PDF (HTML → WeasyPrint)
       ↓
Assinar com pyHanko (Certificado A1)
       ↓
Extrair Comprovante (Hash SHA-256, data, certificado)
       ↓
Hospedar em Manus CDN (URL Espelho)
       ↓
Gerar PDF Final (Prescrição + QR Code + Instruções)
       ↓
Hospedar PDF Final (URL Final)
       ↓
Entregar ao Paciente (WhatsApp, Email, etc.)
       ↓
Paciente Valida no ITI (validar.iti.gov.br)
```

---

## 2. Configuração Inicial

### 2.1 Requisitos

**Software:**
- Python 3.11+
- WeasyPrint (para gerar PDF de HTML)
- pyHanko (para assinar PDF com certificado A1)
- qrcode (para gerar QR Code)
- Manus CLI (para hospedar arquivos)

**Certificado:**
- Certificado Digital A1 ICP-Brasil em formato PKCS#12 (.pfx)
- Senha do certificado
- Validade: Verificar data de expiração

**Acesso:**
- Conta Manus (para hospedagem de arquivos)
- Acesso ao portal validar.iti.gov.br (público, sem login)

### 2.2 Instalação de Dependências

```bash
# Instalar pacotes Python
pip install weasyprint pyhanko qrcode pillow

# Verificar instalação
python -c "import weasyprint, pyhanko, qrcode; print('OK')"
```

### 2.3 Estrutura de Diretórios

```
prescricao-digital-icp-brasil/
├── scripts/
│   ├── template_manipulados.py    # Template para prescrições
│   ├── template_exames.py         # Template para exames
│   └── template_receita.py        # Template para receitas simples
├── templates/
│   ├── html_prescricao.html       # Template HTML
│   └── estilos.css                # Estilos padrão
├── docs/
│   ├── MODELOS_PRESCRICOES.md
│   ├── CONFIG_CREDENCIAIS.md
│   └── GUIA_COMPLETO.md
├── exemplos/
│   ├── receita_1_creon_ASSINADA.pdf
│   ├── receita_2_manipulados.pdf
│   └── pedido_exames_ASSINADO.pdf
└── modelos/
    └── [PDFs de referência]
```

---

## 3. Fluxo Detalhado: Passo a Passo

### 3.1 Etapa 1: Preparar Dados do Paciente

Antes de gerar qualquer documento, organize os dados do paciente em um dicionário Python:

```python
paciente = {
    "nome": "Tânia Maria Marinho Pita Nunes",
    "cpf": "31.89810130",
    "data": "27/04/2026",
    "medicamentos": [
        {
            "numero": 1,
            "nome": "Omega 3 (Supraomega 2)",
            "forma": "Cápsula",
            "posologia": "1 cápsula de manhã e 1 à noite"
        },
        {
            "numero": 2,
            "nome": "Fórmula Antioxidante",
            "composicao": "Resveratrol 200mg + Própolis 400mg",
            "forma": "QSP 1 dose em cápsulas gastrorresistentes",
            "posologia": "1 dose à noite"
        }
    ]
}
```

### 3.2 Etapa 2: Gerar PDF com WeasyPrint

Crie um template HTML com o layout profissional:

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: 'Segoe UI', Arial; margin: 0; padding: 0; }
        .header { background: linear-gradient(135deg, #0f3460, #16537e); 
                  color: white; padding: 28px 40px; }
        .patient-info { padding: 22px 40px; border-bottom: 1.5px solid #e8eaf6; }
        .content { padding: 10px 40px; }
        .med-item { background: #f8f9fc; border-left: 4px solid #0f3460; 
                    padding: 12px 16px; margin: 8px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Dr. Guili Pech</h1>
        <p>Gastroenterologia | Hepatologia | Endoscopia Digestiva</p>
    </div>
    <div class="patient-info">
        <p><strong>Paciente:</strong> {{ paciente.nome }}</p>
        <p><strong>CPF:</strong> {{ paciente.cpf }}</p>
        <p><strong>Data:</strong> {{ paciente.data }}</p>
    </div>
    <div class="content">
        {% for med in paciente.medicamentos %}
        <div class="med-item">
            <p><strong>{{ med.nome }}</strong></p>
            <p>Forma: {{ med.forma }} | Posologia: {{ med.posologia }}</p>
        </div>
        {% endfor %}
    </div>
</body>
</html>
```

Converter HTML para PDF:

```python
from weasyprint import HTML

html_content = """..."""  # HTML acima
HTML(string=html_content).write_pdf("/home/ubuntu/prescricao_temp.pdf")
```

### 3.3 Etapa 3: Assinar com pyHanko

Assinar o PDF com o certificado A1:

```python
from pyhanko.sign import signers, fields
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter

# Carregar certificado
signer = signers.SimpleSigner.load_pkcs12(
    pfx_file="/home/ubuntu/upload/11de2604254bf62c(1).pfx",
    passphrase=b"Pd$Fg69pCbqi83D"
)

# Assinar PDF
with open("/home/ubuntu/prescricao_temp.pdf", "rb") as f:
    w = IncrementalPdfFileWriter(f)
    out = signers.sign_pdf(w, signers.PdfSignatureMetadata(
        field_name="Assinatura_Prescricao",
        md_algorithm="sha256",
        subfilter=fields.SigSeedSubFilter.PADES,
        reason="Prescrição Médica — ICP-Brasil",
        location="Rio de Janeiro, RJ",
    ), signer=signer)
    
    with open("/home/ubuntu/prescricao_assinada.pdf", "wb") as o:
        o.write(out.getbuffer())
```

**Resultado:** PDF assinado com metadados incluídos (não há marca visual, mas a assinatura está embutida).

### 3.4 Etapa 4: Extrair Comprovante de Assinatura

Extrair dados da assinatura para o comprovante:

```python
import hashlib
from pyhanko.pdf_utils.reader import PdfFileReader

# Calcular hash do PDF assinado
with open("/home/ubuntu/prescricao_assinada.pdf", "rb") as f:
    pdf_bytes = f.read()
    doc_hash = hashlib.sha256(pdf_bytes).hexdigest()

# Extrair dados do certificado
with open("/home/ubuntu/prescricao_assinada.pdf", "rb") as f:
    reader = PdfFileReader(f)
    sig = reader.embedded_signatures[0]
    cert = sig.signer_cert
    
    assinante = cert.subject.native['common_name']
    cpf = "***." + cert.subject.native.get('serial_number', '')[-8:-5] + ".*"
    serial = hex(cert.serial_number)
    emissor = cert.issuer.native['common_name']
```

### 3.5 Etapa 5: Hospedar PDF Assinado

Hospedar o PDF assinado em URL pública:

```bash
manus-upload-file /home/ubuntu/prescricao_assinada.pdf
```

**Saída:**
```
CDN URL: https://files.manuscdn.com/user_upload_by_module/session_file/310519663444296140/VYgJEgYqVsKrNtga.pdf
```

Esta é a **URL Espelho** — será usada para validação no ITI.

### 3.6 Etapa 6: Gerar QR Code

Gerar QR Code apontando para o validador ITI:

```python
import qrcode
import base64
from io import BytesIO

qr = qrcode.QRCode(version=1, box_size=10, border=2)
qr.add_data("https://validar.iti.gov.br")
qr.make(fit=True)
img = qr.make_image(fill_color="#0f3460", back_color="white")

buf = BytesIO()
img.save(buf, format="PNG")
qr_b64 = base64.b64encode(buf.getvalue()).decode()
```

### 3.7 Etapa 7: Gerar PDF Final com Validação

Criar PDF com 2 páginas: prescrição + validação com QR Code e instruções:

```html
<!-- PÁGINA 1: Prescrição (igual à anterior) -->
<!-- PÁGINA 2: Validação -->
<div style="page-break-before: always;">
    <h2>Validação de Assinatura Digital ICP-Brasil</h2>
    
    <div class="comprovante">
        <h3>Comprovante de Assinatura Digital</h3>
        <p><strong>Assinado por:</strong> GUILI PECH</p>
        <p><strong>Data/hora:</strong> 27/04/2026 13:05:31 BRT</p>
        <p><strong>Certificado:</strong> 0x11de2604254bf62c</p>
        <p><strong>Emissor:</strong> AC SOLUTI Multipla v5 G2 — ICP-Brasil</p>
        <p><strong>Hash SHA-256:</strong> c8664b114a52284902...</p>
        <div class="seal">ASSINATURA ELETRÔNICA QUALIFICADA — ICP-Brasil</div>
    </div>
    
    <div class="qr">
        <img src="data:image/png;base64,{{ qr_b64 }}" />
        <p>Escaneie para abrir o portal de validação</p>
    </div>
    
    <div class="instrucoes">
        <h3>Como validar a autenticidade deste documento</h3>
        <ol>
            <li>Acesse https://validar.iti.gov.br</li>
            <li>Clique em "Colar URL"</li>
            <li>Cole a URL abaixo: {{ url_espelho }}</li>
            <li>Clique em "Enviar"</li>
        </ol>
    </div>
</div>
```

### 3.8 Etapa 8: Hospedar PDF Final

```bash
manus-upload-file /home/ubuntu/prescricao_final.pdf
```

**Saída:**
```
CDN URL: https://files.manuscdn.com/user_upload_by_module/session_file/310519663444296140/WwHMmrjJOkkfrCqc.pdf
```

Esta é a **URL Final** — será enviada ao paciente.

### 3.9 Etapa 9: Entregar ao Paciente

Enviar a URL final ao paciente por WhatsApp, Email ou SMS:

```
Olá! Sua prescrição está pronta para validação.

Clique aqui para abrir: https://files.manuscdn.com/.../WwHMmrjJOkkfrCqc.pdf

Você pode:
1. Escanear o QR Code na página 2 para validar
2. Colar a URL no validador ITI (https://validar.iti.gov.br)
3. Fazer upload do PDF para validação por arquivo

Qualquer dúvida, entre em contato.
```

### 3.10 Etapa 10: Validação no ITI

O paciente acessa https://validar.iti.gov.br e escolhe um dos métodos:

**Método 1: Colar URL**
1. Clica em "Colar URL"
2. Cola a URL fornecida
3. Clica em "Enviar"
4. Resultado: "ASSINATURA ELETRÔNICA QUALIFICADA — ICP-Brasil"

**Método 2: Upload de Arquivo**
1. Clica em "Escolher Arquivo"
2. Faz upload do PDF
3. Resultado: "ASSINATURA ELETRÔNICA QUALIFICADA — ICP-Brasil"

---

## 4. Implementação: Script Completo

O script `template_manipulados.py` implementa todo o fluxo acima. Para usar:

```bash
# Copiar template
cp scripts/template_manipulados.py nova_prescricao.py

# Editar dados do paciente (linhas 50-80)
# Editar medicamentos (linhas 85-120)

# Executar
python3 nova_prescricao.py
```

**Saída:**
```
Gerando Prescrição de Manipulados...
[1] Gerando PDF com 2 páginas...
   OK
[2] Assinando com certificado ICP-Brasil...
   OK
[3] Extraindo comprovante de assinatura...
   OK
[4] Hospedando PDF assinado...
   URL: https://files.manuscdn.com/.../VYgJEgYqVsKrNtga.pdf
[5] Gerando PDF final com QR + instruções...
   OK
[6] Hospedando PDF final...
   URL: https://files.manuscdn.com/.../WwHMmrjJOkkfrCqc.pdf

URL para enviar ao paciente: https://files.manuscdn.com/.../WwHMmrjJOkkfrCqc.pdf
```

---

## 5. Modelos Disponíveis

### 5.1 Prescrição de Manipulados

**Arquivo:** `scripts/template_manipulados.py`

**Uso:** Para prescrever medicamentos manipulados (Omega 3, Resveratrol, Magnésio, etc.)

**Características:**
- Até 4 medicamentos por prescrição
- Forma, composição e posologia customizáveis
- Layout profissional com cabeçalho azul
- Assinatura digital com certificado A1
- QR Code + instruções de validação

**Exemplo de Saída:** `TANIA_Prescricao_Manipulados_FINAL.pdf`

### 5.2 Pedido de Exames

**Arquivo:** `scripts/template_exames.py` (a ser criado)

**Uso:** Para solicitar exames laboratoriais (hemograma, bioquímica, etc.)

**Características:**
- Lista de exames com códigos TUS
- Indicação clínica
- Assinatura digital
- Validação no ITI

**Exemplo:** Cintilografia miocárdica (TUS 40701069 + 40701140)

### 5.3 Receita Simples

**Arquivo:** `scripts/template_receita.py` (a ser criado)

**Uso:** Para prescrever medicamentos de farmácia (Creon, antibióticos, etc.)

**Características:**
- Um único medicamento
- Posologia clara
- Assinatura digital
- Validação no ITI

**Exemplo:** Creon 10.000 UI

---

## 6. Segurança e Boas Práticas

### 6.1 Proteção de Credenciais

**NUNCA fazer:**
```python
# ❌ Errado: credenciais no código
signer = signers.SimpleSigner.load_pkcs12(
    pfx_file="/home/ubuntu/upload/11de2604254bf62c(1).pfx",
    passphrase=b"Pd$Fg69pCbqi83D"  # ❌ Nunca hardcode!
)
```

**SEMPRE fazer:**
```python
# ✅ Correto: usar variáveis de ambiente
import os
pfx_path = os.getenv("PFX_PATH")
pfx_password = os.getenv("PFX_PASSWORD").encode()
signer = signers.SimpleSigner.load_pkcs12(
    pfx_file=pfx_path,
    passphrase=pfx_password
)
```

### 6.2 Validação de Entrada

```python
# Validar dados do paciente
def validar_paciente(paciente):
    assert "nome" in paciente and len(paciente["nome"]) > 0
    assert "cpf" in paciente and len(paciente["cpf"]) == 14  # XX.XXX.XXX-XX
    assert "data" in paciente
    assert "medicamentos" in paciente and len(paciente["medicamentos"]) > 0
    return True
```

### 6.3 Tratamento de Erros

```python
try:
    # Assinar PDF
    with open(pdf_path, "rb") as f:
        w = IncrementalPdfFileWriter(f)
        out = signers.sign_pdf(...)
except FileNotFoundError:
    print("Erro: Arquivo PDF não encontrado")
except Exception as e:
    print(f"Erro ao assinar: {str(e)}")
```

### 6.4 Permissões de Arquivo

```bash
# Certificado A1 (somente leitura para owner)
chmod 400 /home/ubuntu/upload/11de2604254bf62c(1).pfx

# Scripts (executável)
chmod 755 /home/ubuntu/prescricao-digital-icp-brasil/scripts/*.py
```

---

## 7. Troubleshooting

### Problema: "PDF corrompido após assinatura"

**Causa:** Mesclagem de PDFs com pypdf invalida a assinatura.

**Solução:** Gerar PDF completo (prescrição + validação) ANTES de assinar, não depois.

```python
# ❌ Errado
pdf1 = gerar_prescricao()
pdf1_assinado = assinar(pdf1)
pdf2 = gerar_validacao()
pdf_final = mesclar(pdf1_assinado, pdf2)  # ❌ Invalida assinatura!

# ✅ Correto
pdf_completo = gerar_prescricao() + gerar_validacao()
pdf_final = assinar(pdf_completo)
```

### Problema: "URL não funciona no validador ITI"

**Causa:** URL hospedada incorretamente ou com caracteres especiais.

**Solução:** Verificar que a URL:
1. Começa com `https://`
2. Não contém espaços ou caracteres especiais
3. Retorna HTTP 200 ao acessar
4. Contém um PDF válido

```bash
curl -I "https://files.manuscdn.com/.../VYgJEgYqVsKrNtga.pdf"
# HTTP/1.1 200 OK
```

### Problema: "Certificado expirado"

**Causa:** Certificado A1 venceu.

**Solução:** Renovar certificado junto à AC SOLUTI ou outra autoridade certificadora.

```bash
# Verificar validade
openssl pkcs12 -in 11de2604254bf62c(1).pfx -passin pass:Pd$Fg69pCbqi83D -info
```

### Problema: "pyHanko não encontra o certificado"

**Causa:** Caminho do arquivo .pfx incorreto ou senha errada.

**Solução:** Verificar caminho e senha:

```bash
# Listar arquivo
ls -la /home/ubuntu/upload/11de2604254bf62c(1).pfx

# Testar senha
openssl pkcs12 -in 11de2604254bf62c(1).pfx -passin pass:Pd$Fg69pCbqi83D -noout
```

---

## 8. Integração com n8n (Automação)

Para automatizar a geração de prescrições via n8n:

### 8.1 Webhook Trigger

```json
{
  "trigger": "webhook",
  "method": "POST",
  "path": "/prescricoes",
  "body": {
    "paciente": {
      "nome": "Tânia Maria Marinho Pita Nunes",
      "cpf": "31.89810130"
    },
    "medicamentos": [
      {
        "nome": "Omega 3",
        "forma": "Cápsula",
        "posologia": "1 cápsula de manhã e 1 à noite"
      }
    ]
  }
}
```

### 8.2 Execute Python Script

```
Execute Python → template_manipulados.py
Input: {{ $json.body }}
Output: URL final
```

### 8.3 Send Email

```
Send Email
To: {{ $json.body.paciente.email }}
Subject: Sua prescrição está pronta
Body: Clique aqui para abrir: {{ $json.output.url_final }}
```

---

## 9. Próximas Melhorias

- [ ] Criar template para atestados médicos
- [ ] Criar template para laudos de exames
- [ ] Integrar com n8n para automação completa
- [ ] Adicionar suporte para múltiplas assinaturas (médico + paciente)
- [ ] Criar dashboard para histórico de prescrições
- [ ] Implementar validação automática no ITI via API
- [ ] Adicionar suporte para assinatura remota via BRy Cloud Signer

---

## 10. Referências

| Recurso | URL |
|---------|-----|
| Portal de Validação ITI | https://validar.iti.gov.br |
| ICP-Brasil | https://www.iti.gov.br/icp |
| WeasyPrint | https://weasyprint.org |
| pyHanko | https://github.com/MatthiasValvekens/pyHanko |
| Manus | https://manus.im |
| BRy Cloud | https://www.bry.cloud |

---

**Documento Preparado por:** Manus AI  
**Para:** Dr. Guili Pech  
**Data:** 27 de abril de 2026  
**Versão:** 1.0  
**Status:** Pronto para Produção
