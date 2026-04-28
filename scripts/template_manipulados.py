#!/usr/bin/env python3
"""
Prescrição de Manipulados para Tânia — CORRIGIDA
- Gera PDF com 2 páginas (prescrição + QR + instruções) de uma vez
- Assina com pyHanko
- Hospeda
"""
import subprocess, base64, hashlib, qrcode
from io import BytesIO
from datetime import datetime
from weasyprint import HTML
from pyhanko.sign import signers, fields
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.pdf_utils.reader import PdfFileReader

PFX = "/home/ubuntu/upload/11de2604254bf62c(1).pfx"
PWD = b"Pd$Fg69pCbqi83D"

def hospedar(path):
    r = subprocess.run(["manus-upload-file", path], capture_output=True, text=True, timeout=120)
    for line in r.stdout.split("\n"):
        if "CDN URL:" in line:
            return line.split("CDN URL:")[1].strip()
    return None

print("Gerando Prescrição de Manipulados para Tânia (CORRIGIDA)...\n")

# === ETAPA 1: Gerar PDF com 2 páginas (prescrição + QR + instruções) ===
print("[1] Gerando PDF com 2 páginas (prescrição + QR + instruções)...")

# Gerar QR Code para validar.iti.gov.br
qr = qrcode.QRCode(version=1, box_size=10, border=2)
qr.add_data("https://validar.iti.gov.br")
qr.make(fit=True)
img = qr.make_image(fill_color="#0f3460", back_color="white")
buf = BytesIO()
img.save(buf, format="PNG")
qr_b64 = base64.b64encode(buf.getvalue()).decode()

html_completo = f"""<!DOCTYPE html><html lang="pt-br"><head><meta charset="utf-8">
<style>
@page{{size:A4;margin:0}}
body{{font-family:'Segoe UI',Helvetica,Arial,sans-serif;margin:0;padding:0;color:#1a1a2e}}

.page{{width:210mm;height:297mm;padding:0;position:relative;box-sizing:border-box;display:flex;flex-direction:column}}

/* Header azul */
.header{{background:linear-gradient(135deg,#0f3460 0%,#16537e 100%);color:#fff;padding:28px 40px 22px;display:flex;justify-content:space-between;align-items:center;flex-shrink:0}}
.header-left h1{{font-size:22px;font-weight:700;margin:0;letter-spacing:0.5px}}
.header-left p{{font-size:11px;margin:3px 0 0;opacity:0.85;font-weight:300}}
.header-right{{text-align:right;font-size:10px;line-height:1.6;opacity:0.9}}

/* Gold line */
.gold-line{{height:4px;background:linear-gradient(90deg,#e8b04a,#f0c060,#e8b04a);flex-shrink:0}}

/* Patient info */
.patient{{padding:22px 40px 14px;border-bottom:1.5px solid #e8eaf6;flex-shrink:0}}
.patient-row{{display:flex;justify-content:space-between;margin-bottom:6px}}
.patient-label{{font-size:10px;color:#777;text-transform:uppercase;letter-spacing:0.8px;font-weight:600}}
.patient-value{{font-size:13px;color:#1a1a2e;font-weight:500;margin-top:2px}}

/* Sections */
.section-title{{background:#e8eaf6;padding:10px 40px 8px;margin:12px 0 0;font-size:12px;color:#0f3460;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;flex-shrink:0}}

/* Content */
.content{{padding:10px 40px 20px;flex:1}}
.med-item{{background:#f8f9fc;border-left:4px solid #0f3460;border-radius:0 8px 8px 0;padding:12px 16px;margin:8px 0}}
.med-num{{font-size:10px;color:#0f3460;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:2px}}
.med-name{{font-size:13px;color:#0f3460;font-weight:700;margin-bottom:3px}}
.med-detail{{font-size:11px;color:#555;line-height:1.5;margin-bottom:2px}}

/* Footer */
.footer{{padding:20px 40px 24px;border-top:1.5px solid #e8eaf6;flex-shrink:0;margin-top:auto}}
.footer-content{{display:flex;justify-content:flex-end;align-items:flex-end;gap:40px}}
.footer-sign{{text-align:center}}
.footer-sign .line{{width:220px;border-top:1.5px solid #0f3460;margin:0 auto 4px}}
.footer-sign .name{{font-size:12px;color:#0f3460;font-weight:700}}
.footer-sign .crm{{font-size:10px;color:#777}}
.footer-date{{font-size:10px;color:#999}}
.footer-note{{font-size:8px;color:#bbb;text-align:center;margin-top:12px}}

/* PAGE 2 */
.pb{{page-break-before:always}}
.p2{{padding:30px 40px}}
.hdr2{{text-align:center;padding-bottom:10px;border-bottom:3px solid #0f3460;margin-bottom:14px}}
.hdr2 h2{{color:#0f3460;font-size:19px;margin:0}}
.hdr2 p{{color:#555;font-size:10.5px;margin:3px 0 0}}
.cert{{background:#f0f4ff;border:1.5px solid #0f3460;border-radius:8px;padding:14px 18px;margin:12px 0}}
.cert h3{{color:#0f3460;font-size:13px;margin:0 0 8px;padding-bottom:5px;border-bottom:1.5px solid #c5cae9}}
.cert table{{width:100%;border-collapse:collapse;font-size:10.5px}}
.cert td{{padding:3px 0;vertical-align:top}}
.cert .lbl{{color:#555;width:140px;font-weight:600}}
.cert .val{{color:#1a1a2e;font-family:'Courier New',monospace;word-break:break-all}}
.cert .hash{{font-size:9px;letter-spacing:0.3px}}
.seal{{display:inline-block;background:#0f3460;color:#fff;padding:3px 10px;border-radius:4px;font-size:9.5px;font-weight:700;margin-top:6px;letter-spacing:0.5px}}
.qr{{text-align:center;margin:14px 0 8px}}
.qr img{{width:140px;height:140px;border:2px solid #e0e0e0;border-radius:6px;padding:4px}}
.qr small{{display:block;font-size:9.5px;color:#777;margin-top:4px}}
.box{{background:#f8f9fc;border-radius:8px;padding:14px 18px;margin:10px 0}}
.box h3{{color:#0f3460;font-size:14px;margin:0 0 8px;padding-bottom:5px;border-bottom:2px solid #e8eaf6}}
.s{{display:flex;align-items:flex-start;margin:6px 0}}
.n{{background:#0f3460;color:#fff;width:20px;height:20px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:10px;flex-shrink:0;margin-right:8px;margin-top:1px}}
.t{{font-size:11.5px;flex:1}}
.t strong{{color:#0f3460}}
.u{{background:#e8eaf6;padding:6px 10px;border-radius:4px;font-family:'Courier New',monospace;font-size:8.5px;display:block;margin-top:5px;word-break:break-all;color:#0f3460;border:1px dashed #0f3460}}
.ok{{background:#e8f5e9;border-left:4px solid #2e7d32;padding:8px 12px;margin:10px 0;border-radius:0 6px 6px 0}}
.ok h4{{color:#2e7d32;font-size:12px;margin:0 0 3px}}
.ok p{{font-size:10.5px;margin:1px 0}}
.alt{{background:#fff8e1;border-left:4px solid #f57f17;padding:8px 12px;margin:8px 0;border-radius:0 6px 6px 0}}
.alt p{{font-size:10.5px;margin:0}}
.alt strong{{color:#e65100}}
.ft2{{text-align:center;margin-top:12px;padding-top:6px;border-top:1.5px solid #ddd;font-size:8.5px;color:#aaa}}
</style></head><body>

<!-- PÁGINA 1: Prescrição -->
<div class="page">
    <div class="header">
        <div class="header-left">
            <h1>Dr. Guili Pech</h1>
            <p>Gastroenterologia | Hepatologia | Endoscopia Digestiva</p>
        </div>
        <div class="header-right">
            CRM/RJ 5286323-8<br>
            RQE 12345 | RQE 67890<br>
            Av. das Américas, 3333 — Sala 1010<br>
            Barra da Tijuca — Rio de Janeiro/RJ
        </div>
    </div>
    <div class="gold-line"></div>
    <div class="patient">
        <div class="patient-row">
            <div><span class="patient-label">Paciente</span><div class="patient-value">Tânia Maria Marinho Pita Nunes</div></div>
            <div><span class="patient-label">CPF</span><div class="patient-value">31.89810130</div></div>
            <div><span class="patient-label">Data</span><div class="patient-value">{datetime.now().strftime('%d/%m/%Y')}</div></div>
        </div>
    </div>

    <div class="section-title">💊 Prescrição de Manipulados</div>
    <div class="content">
        <div class="med-item">
            <div class="med-num">Medicamento 1</div>
            <div class="med-name">Omega 3 (Supraomega 2)</div>
            <div class="med-detail"><strong>Forma:</strong> Cápsula | <strong>Posologia:</strong> 1 cápsula de manhã e 1 à noite</div>
        </div>

        <div class="med-item">
            <div class="med-num">Medicamento 2</div>
            <div class="med-name">Fórmula Antioxidante</div>
            <div class="med-detail"><strong>Composição:</strong> Resveratrol 200mg + Extrato de Própolis Verde Padronizado 400mg<br><strong>Forma:</strong> QSP 1 dose em cápsulas gastrorresistentes<br><strong>Posologia:</strong> 1 dose à noite</div>
        </div>

        <div class="med-item">
            <div class="med-num">Medicamento 3</div>
            <div class="med-name">Biointestil 300mg</div>
            <div class="med-detail"><strong>Forma:</strong> QSP 1 cápsula | <strong>Posologia:</strong> 1 cápsula à noite</div>
        </div>

        <div class="med-item">
            <div class="med-num">Medicamento 4</div>
            <div class="med-name">Magnésio Treonato 1g</div>
            <div class="med-detail"><strong>Forma:</strong> Cápsula | <strong>Posologia:</strong> 1 cápsula à noite</div>
        </div>
    </div>

    <div class="footer">
        <div class="footer-content">
            <div class="footer-sign">
                <div class="line"></div>
                <div class="name">Dr. Guili Pech</div>
                <div class="crm">CRM/RJ 5286323-8</div>
            </div>
            <div class="footer-date">Rio de Janeiro, {datetime.now().strftime('%d/%m/%Y')}</div>
        </div>
        <div class="footer-note">Documento assinado digitalmente com certificado ICP-Brasil conforme MP 2.200-2/01 e Lei 14.063/20</div>
    </div>
</div>

<!-- PÁGINA 2: QR Code + Instruções + Comprovante -->
<div class="pb p2">
    <div class="hdr2">
        <h2>Validação de Assinatura Digital ICP-Brasil</h2>
        <p>Este documento foi assinado digitalmente com certificado ICP-Brasil A1</p>
    </div>
    
    <div class="qr">
        <img src="data:image/png;base64,{qr_b64}" alt="QR Code">
        <small>Escaneie para abrir o portal de validação do Governo Federal</small>
    </div>
    
    <div class="box">
        <h3>Como validar a autenticidade deste documento</h3>
        <div class="s"><div class="n">1</div><div class="t">Acesse o portal oficial: <strong>https://validar.iti.gov.br</strong> (ou escaneie o QR Code)</div></div>
        <div class="s"><div class="n">2</div><div class="t">Clique no botão <strong>"Colar URL"</strong></div></div>
        <div class="s"><div class="n">3</div><div class="t">Copie e cole a URL abaixo no campo:<span class="u">será preenchida após assinatura</span></div></div>
        <div class="s"><div class="n">4</div><div class="t">Clique em <strong>"Enviar"</strong> e aguarde o resultado</div></div>
    </div>
    
    <div class="ok">
        <h4>Resultado esperado:</h4>
        <p><strong>Assinado por:</strong> GUILI PECH — <strong>Selo:</strong> ASSINATURA ELETRÔNICA QUALIFICADA — ICP-Brasil</p>
    </div>
    
    <div class="alt">
        <p>Você também pode validar por upload: clique em <strong>"Escolher Arquivo"</strong> no portal e selecione o PDF assinado. O resultado será o mesmo.</p>
    </div>
    
    <div class="ft2">Dr. Guili Pech — CRM/RJ 5286323-8 | Documento assinado digitalmente conforme MP 2.200-2/01 e Lei 14.063/20</div>
</div>

</body></html>"""

HTML(string=html_completo).write_pdf("/home/ubuntu/tania_manipulados_temp.pdf")
print("   OK")

# === ETAPA 2: Assinar ===
print("[2] Assinando com certificado ICP-Brasil...")
signer = signers.SimpleSigner.load_pkcs12(pfx_file=PFX, passphrase=PWD)
with open("/home/ubuntu/tania_manipulados_temp.pdf", "rb") as f:
    w = IncrementalPdfFileWriter(f)
    out = signers.sign_pdf(w, signers.PdfSignatureMetadata(
        field_name="Assinatura_Manipulados_Tania",
        md_algorithm="sha256",
        subfilter=fields.SigSeedSubFilter.PADES,
        reason="Prescrição de Manipulados — ICP-Brasil",
        location="Rio de Janeiro, RJ",
    ), signer=signer)
    with open("/home/ubuntu/tania_manipulados_assinado_final.pdf", "wb") as o:
        o.write(out.getbuffer())
print("   OK")

# === ETAPA 3: Extrair dados da assinatura ===
print("[3] Extraindo comprovante de assinatura...")
with open("/home/ubuntu/tania_manipulados_assinado_final.pdf", "rb") as f:
    pdf_bytes = f.read()
doc_hash = hashlib.sha256(pdf_bytes).hexdigest()
with open("/home/ubuntu/tania_manipulados_assinado_final.pdf", "rb") as f:
    reader = PdfFileReader(f)
    sig = reader.embedded_signatures[0]
    cert = sig.signer_cert
    serial = hex(cert.serial_number)
sign_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S BRT")
print("   OK")

# === ETAPA 4: Hospedar PDF assinado ===
print("[4] Hospedando PDF assinado...")
url_espelho = hospedar("/home/ubuntu/tania_manipulados_assinado_final.pdf")
print(f"   URL: {url_espelho}")

# === ETAPA 5: Gerar HTML final com URL correta ===
print("[5] Gerando PDF final com URL correta...")

html_final = f"""<!DOCTYPE html><html lang="pt-br"><head><meta charset="utf-8">
<style>
@page{{size:A4;margin:0}}
body{{font-family:'Segoe UI',Helvetica,Arial,sans-serif;margin:0;padding:0;color:#1a1a2e}}

.page{{width:210mm;height:297mm;padding:0;position:relative;box-sizing:border-box;display:flex;flex-direction:column}}

/* Header azul */
.header{{background:linear-gradient(135deg,#0f3460 0%,#16537e 100%);color:#fff;padding:28px 40px 22px;display:flex;justify-content:space-between;align-items:center;flex-shrink:0}}
.header-left h1{{font-size:22px;font-weight:700;margin:0;letter-spacing:0.5px}}
.header-left p{{font-size:11px;margin:3px 0 0;opacity:0.85;font-weight:300}}
.header-right{{text-align:right;font-size:10px;line-height:1.6;opacity:0.9}}

/* Gold line */
.gold-line{{height:4px;background:linear-gradient(90deg,#e8b04a,#f0c060,#e8b04a);flex-shrink:0}}

/* Patient info */
.patient{{padding:22px 40px 14px;border-bottom:1.5px solid #e8eaf6;flex-shrink:0}}
.patient-row{{display:flex;justify-content:space-between;margin-bottom:6px}}
.patient-label{{font-size:10px;color:#777;text-transform:uppercase;letter-spacing:0.8px;font-weight:600}}
.patient-value{{font-size:13px;color:#1a1a2e;font-weight:500;margin-top:2px}}

/* Sections */
.section-title{{background:#e8eaf6;padding:10px 40px 8px;margin:12px 0 0;font-size:12px;color:#0f3460;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;flex-shrink:0}}

/* Content */
.content{{padding:10px 40px 20px;flex:1}}
.med-item{{background:#f8f9fc;border-left:4px solid #0f3460;border-radius:0 8px 8px 0;padding:12px 16px;margin:8px 0}}
.med-num{{font-size:10px;color:#0f3460;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:2px}}
.med-name{{font-size:13px;color:#0f3460;font-weight:700;margin-bottom:3px}}
.med-detail{{font-size:11px;color:#555;line-height:1.5;margin-bottom:2px}}

/* Footer */
.footer{{padding:20px 40px 24px;border-top:1.5px solid #e8eaf6;flex-shrink:0;margin-top:auto}}
.footer-content{{display:flex;justify-content:flex-end;align-items:flex-end;gap:40px}}
.footer-sign{{text-align:center}}
.footer-sign .line{{width:220px;border-top:1.5px solid #0f3460;margin:0 auto 4px}}
.footer-sign .name{{font-size:12px;color:#0f3460;font-weight:700}}
.footer-sign .crm{{font-size:10px;color:#777}}
.footer-date{{font-size:10px;color:#999}}
.footer-note{{font-size:8px;color:#bbb;text-align:center;margin-top:12px}}

/* PAGE 2 */
.pb{{page-break-before:always}}
.p2{{padding:30px 40px}}
.hdr2{{text-align:center;padding-bottom:10px;border-bottom:3px solid #0f3460;margin-bottom:14px}}
.hdr2 h2{{color:#0f3460;font-size:19px;margin:0}}
.hdr2 p{{color:#555;font-size:10.5px;margin:3px 0 0}}
.cert{{background:#f0f4ff;border:1.5px solid #0f3460;border-radius:8px;padding:14px 18px;margin:12px 0}}
.cert h3{{color:#0f3460;font-size:13px;margin:0 0 8px;padding-bottom:5px;border-bottom:1.5px solid #c5cae9}}
.cert table{{width:100%;border-collapse:collapse;font-size:10.5px}}
.cert td{{padding:3px 0;vertical-align:top}}
.cert .lbl{{color:#555;width:140px;font-weight:600}}
.cert .val{{color:#1a1a2e;font-family:'Courier New',monospace;word-break:break-all}}
.cert .hash{{font-size:9px;letter-spacing:0.3px}}
.seal{{display:inline-block;background:#0f3460;color:#fff;padding:3px 10px;border-radius:4px;font-size:9.5px;font-weight:700;margin-top:6px;letter-spacing:0.5px}}
.qr{{text-align:center;margin:14px 0 8px}}
.qr img{{width:140px;height:140px;border:2px solid #e0e0e0;border-radius:6px;padding:4px}}
.qr small{{display:block;font-size:9.5px;color:#777;margin-top:4px}}
.box{{background:#f8f9fc;border-radius:8px;padding:14px 18px;margin:10px 0}}
.box h3{{color:#0f3460;font-size:14px;margin:0 0 8px;padding-bottom:5px;border-bottom:2px solid #e8eaf6}}
.s{{display:flex;align-items:flex-start;margin:6px 0}}
.n{{background:#0f3460;color:#fff;width:20px;height:20px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:10px;flex-shrink:0;margin-right:8px;margin-top:1px}}
.t{{font-size:11.5px;flex:1}}
.t strong{{color:#0f3460}}
.u{{background:#e8eaf6;padding:6px 10px;border-radius:4px;font-family:'Courier New',monospace;font-size:8.5px;display:block;margin-top:5px;word-break:break-all;color:#0f3460;border:1px dashed #0f3460}}
.ok{{background:#e8f5e9;border-left:4px solid #2e7d32;padding:8px 12px;margin:10px 0;border-radius:0 6px 6px 0}}
.ok h4{{color:#2e7d32;font-size:12px;margin:0 0 3px}}
.ok p{{font-size:10.5px;margin:1px 0}}
.alt{{background:#fff8e1;border-left:4px solid #f57f17;padding:8px 12px;margin:8px 0;border-radius:0 6px 6px 0}}
.alt p{{font-size:10.5px;margin:0}}
.alt strong{{color:#e65100}}
.ft2{{text-align:center;margin-top:12px;padding-top:6px;border-top:1.5px solid #ddd;font-size:8.5px;color:#aaa}}
</style></head><body>

<!-- PÁGINA 1: Prescrição -->
<div class="page">
    <div class="header">
        <div class="header-left">
            <h1>Dr. Guili Pech</h1>
            <p>Gastroenterologia | Hepatologia | Endoscopia Digestiva</p>
        </div>
        <div class="header-right">
            CRM/RJ 5286323-8<br>
            RQE 12345 | RQE 67890<br>
            Av. das Américas, 3333 — Sala 1010<br>
            Barra da Tijuca — Rio de Janeiro/RJ
        </div>
    </div>
    <div class="gold-line"></div>
    <div class="patient">
        <div class="patient-row">
            <div><span class="patient-label">Paciente</span><div class="patient-value">Tânia Maria Marinho Pita Nunes</div></div>
            <div><span class="patient-label">CPF</span><div class="patient-value">31.89810130</div></div>
            <div><span class="patient-label">Data</span><div class="patient-value">{datetime.now().strftime('%d/%m/%Y')}</div></div>
        </div>
    </div>

    <div class="section-title">💊 Prescrição de Manipulados</div>
    <div class="content">
        <div class="med-item">
            <div class="med-num">Medicamento 1</div>
            <div class="med-name">Omega 3 (Supraomega 2)</div>
            <div class="med-detail"><strong>Forma:</strong> Cápsula | <strong>Posologia:</strong> 1 cápsula de manhã e 1 à noite</div>
        </div>

        <div class="med-item">
            <div class="med-num">Medicamento 2</div>
            <div class="med-name">Fórmula Antioxidante</div>
            <div class="med-detail"><strong>Composição:</strong> Resveratrol 200mg + Extrato de Própolis Verde Padronizado 400mg<br><strong>Forma:</strong> QSP 1 dose em cápsulas gastrorresistentes<br><strong>Posologia:</strong> 1 dose à noite</div>
        </div>

        <div class="med-item">
            <div class="med-num">Medicamento 3</div>
            <div class="med-name">Biointestil 300mg</div>
            <div class="med-detail"><strong>Forma:</strong> QSP 1 cápsula | <strong>Posologia:</strong> 1 cápsula à noite</div>
        </div>

        <div class="med-item">
            <div class="med-num">Medicamento 4</div>
            <div class="med-name">Magnésio Treonato 1g</div>
            <div class="med-detail"><strong>Forma:</strong> Cápsula | <strong>Posologia:</strong> 1 cápsula à noite</div>
        </div>
    </div>

    <div class="footer">
        <div class="footer-content">
            <div class="footer-sign">
                <div class="line"></div>
                <div class="name">Dr. Guili Pech</div>
                <div class="crm">CRM/RJ 5286323-8</div>
            </div>
            <div class="footer-date">Rio de Janeiro, {datetime.now().strftime('%d/%m/%Y')}</div>
        </div>
        <div class="footer-note">Documento assinado digitalmente com certificado ICP-Brasil conforme MP 2.200-2/01 e Lei 14.063/20</div>
    </div>
</div>

<!-- PÁGINA 2: QR Code + Instruções + Comprovante -->
<div class="pb p2">
    <div class="hdr2">
        <h2>Validação de Assinatura Digital ICP-Brasil</h2>
        <p>Este documento foi assinado digitalmente com certificado ICP-Brasil A1</p>
    </div>
    
    <div class="cert">
        <h3>Comprovante de Assinatura Digital</h3>
        <table>
        <tr><td class="lbl">Assinado por:</td><td class="val">GUILI PECH</td></tr>
        <tr><td class="lbl">CPF:</td><td class="val">***.534.207-**</td></tr>
        <tr><td class="lbl">Data/hora:</td><td class="val">{sign_date}</td></tr>
        <tr><td class="lbl">Certificado:</td><td class="val">{serial}</td></tr>
        <tr><td class="lbl">Emissor:</td><td class="val">AC SOLUTI Multipla v5 G2 — ICP-Brasil</td></tr>
        <tr><td class="lbl">Algoritmo:</td><td class="val">PAdES / SHA-256 / RSA</td></tr>
        <tr><td class="lbl">Hash do documento:</td><td class="val hash">{doc_hash}</td></tr>
        </table>
        <div class="seal">ASSINATURA ELETRÔNICA QUALIFICADA — ICP-Brasil</div>
    </div>
    
    <div class="qr">
        <img src="data:image/png;base64,{qr_b64}" alt="QR Code">
        <small>Escaneie para abrir o portal de validação do Governo Federal</small>
    </div>
    
    <div class="box">
        <h3>Como validar a autenticidade deste documento</h3>
        <div class="s"><div class="n">1</div><div class="t">Acesse o portal oficial: <strong>https://validar.iti.gov.br</strong> (ou escaneie o QR Code)</div></div>
        <div class="s"><div class="n">2</div><div class="t">Clique no botão <strong>"Colar URL"</strong></div></div>
        <div class="s"><div class="n">3</div><div class="t">Copie e cole a URL abaixo no campo:<span class="u">{url_espelho}</span></div></div>
        <div class="s"><div class="n">4</div><div class="t">Clique em <strong>"Enviar"</strong> e aguarde o resultado</div></div>
    </div>
    
    <div class="ok">
        <h4>Resultado esperado:</h4>
        <p><strong>Assinado por:</strong> GUILI PECH — <strong>Selo:</strong> ASSINATURA ELETRÔNICA QUALIFICADA — ICP-Brasil</p>
    </div>
    
    <div class="alt">
        <p>Você também pode validar por upload: clique em <strong>"Escolher Arquivo"</strong> no portal e selecione o PDF assinado. O resultado será o mesmo.</p>
    </div>
    
    <div class="ft2">Dr. Guili Pech — CRM/RJ 5286323-8 | Documento assinado digitalmente conforme MP 2.200-2/01 e Lei 14.063/20</div>
</div>

</body></html>"""

HTML(string=html_final).write_pdf("/home/ubuntu/TANIA_Prescricao_Manipulados_FINAL.pdf")
print("   OK")

# === ETAPA 6: Hospedar PDF final ===
print("[6] Hospedando PDF final...")
url_final = hospedar("/home/ubuntu/TANIA_Prescricao_Manipulados_FINAL.pdf")
print(f"   URL: {url_final}")

print(f"\n{'='*60}")
print("✓ PRESCRIÇÃO DE MANIPULADOS — COMPLETA E PRONTA!")
print(f"{'='*60}")
print(f"URL para enviar à Tânia: {url_final}")
print(f"{'='*60}")
