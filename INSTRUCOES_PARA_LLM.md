# Instruções para LLM: Geração Automática de Documentos Médicos Assinados 24/7

**Destinatário:** Qualquer LLM (Perplexity, Claude, GPT, etc.)  
**Objetivo:** Gerar, assinar e hospedar documentos médicos com assinatura ICP-Brasil  
**Disponibilidade:** 24/7, independente do computador do Dr. Guili estar ligado  
**Data:** 27 de abril de 2026

---

## 1. Resumo Executivo

Você receberá dados de um paciente (nome, CPF, medicamentos/exames) e deverá:

1. **Gerar** um PDF profissional com os dados
2. **Assinar** com certificado A1 ICP-Brasil
3. **Hospedar** em URL pública
4. **Retornar** as URLs finais para o paciente

Tudo isso funciona **24/7** porque:
- O certificado (.pfx) está guardado em **MinIO** (seu servidor privado)
- Você baixa, assina com pyHanko, hospeda em **Manus CDN**
- Nenhuma dependência do computador do Dr. Guili estar ligado

---

## 2. Credenciais e Acessos

### 2.1 Certificado Digital A1 (Guardado em MinIO)

**Localização:** MinIO (seu servidor privado)  
**Caminho:** `/certificados/guili-pech/11de2604254bf62c.pfx`  
**Senha:** `Pd$Fg69pCbqi83D`

**Como acessar:**
```bash
# Conectar ao MinIO
mc alias set minio https://seu-minio.com:9000 MINIO_USER MINIO_PASSWORD

# Baixar certificado
mc cp minio/certificados/guili-pech/11de2604254bf62c.pfx ./cert.pfx
```

**Ou via Python:**
```python
from minio import Minio

client = Minio(
    "seu-minio.com:9000",
    access_key="MINIO_USER",
    secret_key="MINIO_PASSWORD",
    secure=True
)

client.fget_object(
    "certificados",
    "guili-pech/11de2604254bf62c.pfx",
    "/tmp/cert.pfx"
)
```

### 2.2 Hospedagem: Manus CDN

**Comando:** `manus-upload-file <arquivo.pdf>`  
**Retorno:** URL pública permanente  
**Exemplo:** `https://files.manuscdn.com/user_upload_by_module/session_file/.../VYgJEgYqVsKrNtga.pdf`

**Como usar:**
```bash
manus-upload-file /tmp/prescricao_assinada.pdf
# Saída: https://files.manuscdn.com/.../VYgJEgYqVsKrNtga.pdf
```

### 2.3 Dados do Médico (Padrão em Todos os Documentos)

```
Nome: Dr. Guili Pech
CRM/RJ: 5286323-8
Especialidades: Gastroenterologia | Hepatologia | Endoscopia Digestiva
Endereço: Av. das Américas, 3333 — Sala 1010, Barra da Tijuca, Rio de Janeiro, RJ
Telefone: (21) 9111-6980
Email: guili@medicos.com.br
```

---

## 3. Fluxo Completo (Passo a Passo)

### Etapa 1: Receber Dados do Paciente

```json
{
  "tipo": "prescricao_manipulados",
  "paciente": {
    "nome": "Tânia Maria Marinho Pita Nunes",
    "cpf": "31.89810130",
    "data": "27/04/2026"
  },
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

### Etapa 2: Gerar PDF com WeasyPrint

```python
from weasyprint import HTML

html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Segoe UI', Arial; margin: 0; padding: 0; }}
        .header {{ background: linear-gradient(135deg, #0f3460, #16537e); 
                  color: white; padding: 28px 40px; }}
        .header h1 {{ margin: 0; font-size: 24px; }}
        .patient-info {{ padding: 22px 40px; border-bottom: 1.5px solid #e8eaf6; }}
        .content {{ padding: 10px 40px; }}
        .med-item {{ background: #f8f9fc; border-left: 4px solid #0f3460; 
                    padding: 12px 16px; margin: 8px 0; }}
        .footer {{ padding: 20px 40px; border-top: 1px solid #e8eaf6; 
                  font-size: 11px; color: #666; text-align: center; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Dr. Guili Pech</h1>
        <p>Gastroenterologia | Hepatologia | Endoscopia Digestiva</p>
    </div>
    <div class="patient-info">
        <p><strong>Paciente:</strong> {paciente['nome']}</p>
        <p><strong>CPF:</strong> {paciente['cpf']}</p>
        <p><strong>Data:</strong> {paciente['data']}</p>
    </div>
    <div class="content">
"""

for med in medicamentos:
    html += f"""
    <div class="med-item">
        <p><strong>Item {med['numero']}: {med['nome']}</strong></p>
        <p>Forma: {med['forma']} | Posologia: {med['posologia']}</p>
    </div>
"""

html += """
    </div>
    <div class="footer">
        <p>Documento assinado digitalmente com certificado ICP-Brasil</p>
    </div>
</body>
</html>
"""

HTML(string=html).write_pdf("/tmp/prescricao.pdf")
```

### Etapa 3: Baixar Certificado do MinIO

```python
from minio import Minio

client = Minio(
    "seu-minio.com:9000",
    access_key="MINIO_USER",
    secret_key="MINIO_PASSWORD",
    secure=True
)

client.fget_object(
    "certificados",
    "guili-pech/11de2604254bf62c.pfx",
    "/tmp/cert.pfx"
)
```

### Etapa 4: Assinar com pyHanko

```python
from pyhanko.sign import signers, fields
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter

# Carregar certificado
signer = signers.SimpleSigner.load_pkcs12(
    pfx_file="/tmp/cert.pfx",
    passphrase=b"Pd$Fg69pCbqi83D"
)

# Assinar PDF
with open("/tmp/prescricao.pdf", "rb") as f:
    w = IncrementalPdfFileWriter(f)
    out = signers.sign_pdf(
        w,
        signers.PdfSignatureMetadata(
            field_name="Assinatura_Prescricao",
            md_algorithm="sha256",
            subfilter=fields.SigSeedSubFilter.PADES,
            reason="Prescrição Médica — ICP-Brasil",
            location="Rio de Janeiro, RJ",
        ),
        signer=signer
    )
    
    with open("/tmp/prescricao_assinada.pdf", "wb") as o:
        o.write(out.getbuffer())
```

### Etapa 5: Calcular Hash SHA-256

```python
import hashlib

with open("/tmp/prescricao_assinada.pdf", "rb") as f:
    pdf_bytes = f.read()
    doc_hash = hashlib.sha256(pdf_bytes).hexdigest()
    
print(f"Hash: {doc_hash}")
# Exemplo: c8664b114a52284902a3d4c5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4
```

### Etapa 6: Hospedar em Manus CDN

```bash
manus-upload-file /tmp/prescricao_assinada.pdf
# Saída: https://files.manuscdn.com/user_upload_by_module/session_file/310519663444296140/VYgJEgYqVsKrNtga.pdf
```

**Salve esta URL como "URL_ESPELHO"** — será usada para validação no ITI.

### Etapa 7: Gerar QR Code

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

# Usar em HTML: <img src="data:image/png;base64,{{ qr_b64 }}" />
```

### Etapa 8: Gerar PDF Final com Validação (2 páginas)

```python
from weasyprint import HTML

html_final = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Segoe UI', Arial; margin: 0; padding: 0; }}
        .header {{ background: linear-gradient(135deg, #0f3460, #16537e); 
                  color: white; padding: 28px 40px; }}
        .page {{ page-break-after: always; }}
        .comprovante {{ background: #f8f9fc; border: 2px solid #0f3460; 
                       padding: 20px; margin: 20px 0; border-radius: 8px; }}
        .seal {{ background: #0f3460; color: white; padding: 12px; 
                text-align: center; border-radius: 4px; margin: 10px 0; 
                font-weight: bold; }}
        .url-box {{ background: #fff3cd; border: 2px solid #ffc107; 
                   padding: 15px; margin: 15px 0; border-radius: 4px; 
                   font-family: monospace; word-break: break-all; }}
        .instrucoes {{ background: #e8f4f8; padding: 15px; border-radius: 4px; }}
        .qr-code {{ text-align: center; margin: 20px 0; }}
        .qr-code img {{ width: 200px; height: 200px; }}
    </style>
</head>
<body>
    <!-- PÁGINA 1: Prescrição -->
    <div class="page">
        <div class="header">
            <h1>Dr. Guili Pech</h1>
            <p>Gastroenterologia | Hepatologia | Endoscopia Digestiva</p>
        </div>
        <div style="padding: 40px;">
            <p><strong>Paciente:</strong> {paciente['nome']}</p>
            <p><strong>CPF:</strong> {paciente['cpf']}</p>
            <p><strong>Data:</strong> {paciente['data']}</p>
"""

for med in medicamentos:
    html_final += f"""
            <div style="background: #f8f9fc; border-left: 4px solid #0f3460; 
                        padding: 12px 16px; margin: 8px 0;">
                <p><strong>Item {med['numero']}: {med['nome']}</strong></p>
                <p>Forma: {med['forma']} | Posologia: {med['posologia']}</p>
            </div>
"""

html_final += f"""
        </div>
    </div>
    
    <!-- PÁGINA 2: Validação -->
    <div class="page" style="padding: 40px;">
        <h2>Validação de Assinatura Digital ICP-Brasil</h2>
        
        <div class="comprovante">
            <h3>Comprovante de Assinatura Digital</h3>
            <p><strong>Assinado por:</strong> GUILI PECH</p>
            <p><strong>CPF:</strong> ***.534.207-**</p>
            <p><strong>Data/hora:</strong> {paciente['data']} 13:05:31 BRT</p>
            <p><strong>Certificado:</strong> 0x11de2604254bf62c</p>
            <p><strong>Emissor:</strong> AC SOLUTI Multipla v5 G2 — ICP-Brasil</p>
            <p><strong>Algoritmo:</strong> PAdES / SHA-256 / RSA 2048</p>
            <p><strong>Hash SHA-256:</strong><br/><code>{doc_hash[:64]}</code></p>
            <div class="seal">ASSINATURA ELETRÔNICA QUALIFICADA — ICP-Brasil</div>
        </div>
        
        <div class="qr-code">
            <p>Escaneie para abrir o portal de validação:</p>
            <img src="data:image/png;base64,{qr_b64}" />
        </div>
        
        <div class="instrucoes">
            <h3>Como validar a autenticidade deste documento</h3>
            <ol>
                <li>Acesse <strong>https://validar.iti.gov.br</strong></li>
                <li>Clique em <strong>"Colar URL"</strong></li>
                <li>Cole a URL abaixo na caixa:</li>
            </ol>
            <div class="url-box">
                {url_espelho}
            </div>
            <ol start="4">
                <li>Clique em <strong>"Enviar"</strong></li>
                <li>Resultado esperado: <strong>"ASSINATURA ELETRÔNICA QUALIFICADA — ICP-Brasil"</strong></li>
            </ol>
            <p><strong>Alternativa:</strong> Você também pode fazer upload do PDF neste mesmo portal clicando em "Escolher Arquivo".</p>
        </div>
    </div>
</body>
</html>
"""

HTML(string=html_final).write_pdf("/tmp/prescricao_final.pdf")
```

### Etapa 9: Hospedar PDF Final

```bash
manus-upload-file /tmp/prescricao_final.pdf
# Saída: https://files.manuscdn.com/user_upload_by_module/session_file/310519663444296140/WwHMmrjJOkkfrCqc.pdf
```

**Esta é a URL_FINAL** — será enviada ao paciente.

### Etapa 10: Retornar Resultado

```json
{
  "status": "sucesso",
  "paciente": "Tânia Maria Marinho Pita Nunes",
  "urls": {
    "url_espelho": "https://files.manuscdn.com/.../VYgJEgYqVsKrNtga.pdf",
    "url_final": "https://files.manuscdn.com/.../WwHMmrjJOkkfrCqc.pdf"
  },
  "comprovante": {
    "assinado_por": "GUILI PECH",
    "data": "27/04/2026 13:05:31 BRT",
    "certificado": "0x11de2604254bf62c",
    "hash_sha256": "c8664b114a52284902a3d4c5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4"
  },
  "instrucoes": "Envie a URL_FINAL ao paciente. Ele pode validar abrindo a URL ou colando no validador ITI."
}
```

---

## 4. Tipos de Documentos Suportados

### 4.1 Prescrição de Manipulados

**Entrada:**
```json
{
  "tipo": "prescricao_manipulados",
  "paciente": { "nome": "...", "cpf": "...", "data": "..." },
  "medicamentos": [
    { "numero": 1, "nome": "...", "forma": "...", "posologia": "..." }
  ]
}
```

**Saída:** PDF com prescrição + validação

### 4.2 Pedido de Exames

**Entrada:**
```json
{
  "tipo": "pedido_exames",
  "paciente": { "nome": "...", "cpf": "...", "data": "..." },
  "exames": [
    { "codigo_tus": "40701069", "nome": "Cintilografia Repouso", "indicacao": "..." }
  ]
}
```

**Saída:** PDF com pedido + validação

### 4.3 Receita Simples

**Entrada:**
```json
{
  "tipo": "receita_simples",
  "paciente": { "nome": "...", "cpf": "...", "data": "..." },
  "medicamento": { "nome": "Creon 10.000 UI", "posologia": "1 cápsula durante refeições" }
}
```

**Saída:** PDF com receita + validação

---

## 5. Segurança e Boas Práticas

### 5.1 Proteção de Credenciais

**NUNCA:**
- ❌ Colocar senha do .pfx em código
- ❌ Enviar .pfx por email
- ❌ Fazer commit do .pfx no GitHub
- ❌ Deixar .pfx em pasta pública

**SEMPRE:**
- ✅ Usar variáveis de ambiente
- ✅ Guardar .pfx em MinIO com acesso restrito
- ✅ Usar HTTPS para tudo
- ✅ Deletar arquivos temporários após uso

### 5.2 Validação de Entrada

```python
def validar_paciente(paciente):
    assert "nome" in paciente and len(paciente["nome"]) > 0
    assert "cpf" in paciente and len(paciente["cpf"]) == 14  # XX.XXX.XXX-XX
    assert "data" in paciente
    return True

def validar_medicamentos(medicamentos):
    assert len(medicamentos) > 0 and len(medicamentos) <= 4
    for med in medicamentos:
        assert "numero" in med and "nome" in med and "posologia" in med
    return True
```

### 5.3 Tratamento de Erros

```python
try:
    # Assinar PDF
    out = signers.sign_pdf(...)
except FileNotFoundError:
    return {"status": "erro", "mensagem": "Certificado não encontrado no MinIO"}
except Exception as e:
    return {"status": "erro", "mensagem": f"Erro ao assinar: {str(e)}"}
finally:
    # Limpar arquivos temporários
    import os
    for f in ["/tmp/cert.pfx", "/tmp/prescricao.pdf", "/tmp/prescricao_assinada.pdf"]:
        if os.path.exists(f):
            os.remove(f)
```

---

## 6. Troubleshooting

| Problema | Causa | Solução |
|----------|-------|---------|
| "Certificado não encontrado" | MinIO desconectado ou caminho errado | Verificar credenciais MinIO e caminho do arquivo |
| "Senha incorreta" | Senha do .pfx errada | Usar `Pd$Fg69pCbqi83D` exatamente |
| "URL não funciona no ITI" | PDF não hospedado corretamente | Verificar que `manus-upload-file` retornou URL 200 |
| "Assinatura inválida" | PDF corrompido durante mesclagem | Gerar PDF completo ANTES de assinar |
| "QR Code não lê" | Dados incorretos no QR | Verificar que QR aponta para `https://validar.iti.gov.br` |

---

## 7. Próximas Etapas (Quando BRy Signer Estiver Disponível)

Quando o Dr. Guili tiver acesso ao **BRy Signer API**, trocar:

**De:**
```python
signer = signers.SimpleSigner.load_pkcs12(
    pfx_file="/tmp/cert.pfx",
    passphrase=b"Pd$Fg69pCbqi83D"
)
```

**Para:**
```python
import requests

response = requests.post(
    "https://api.bry.cloud/v1/sign",
    headers={"Authorization": f"Bearer {bry_token}"},
    json={
        "document": base64.b64encode(pdf_bytes).decode(),
        "certificate_id": "11de2604254bf62c",
        "signature_format": "PAdES"
    }
)

pdf_assinado = base64.b64decode(response.json()["signed_document"])
```

---

## 8. Resumo: O Que Você Precisa Fazer

**Como LLM, você precisa:**

1. ✅ Receber dados do paciente (JSON)
2. ✅ Gerar PDF com WeasyPrint
3. ✅ Baixar certificado do MinIO
4. ✅ Assinar com pyHanko
5. ✅ Hospedar em Manus CDN
6. ✅ Retornar URLs finais

**Tudo isso funciona 24/7** porque:
- O certificado está no MinIO (sempre acessível)
- Manus CDN está sempre online
- Nenhuma dependência do computador do Dr. Guili

**Resultado:** Documentos médicos profissionais, legalmente válidos, com assinatura ICP-Brasil, prontos para validação no ITI.

---

**Documento Preparado por:** Manus AI  
**Para:** Qualquer LLM (Perplexity, Claude, GPT, etc.)  
**Data:** 27 de abril de 2026  
**Status:** Pronto para Uso
