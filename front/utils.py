import random
import string
import qrcode
import base64
from io import BytesIO
from xhtml2pdf import pisa   
from django.http import HttpResponse
from django.template.loader import get_template
from django.core.files.uploadedfile import SimpleUploadedFile
import base64

"""
Génération des clés de sécurité
"""
def generate_secure_key(length: int):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

"""
Fonction pour générer le QrCode
"""
def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    qr_code_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return qr_code_b64

"""
Fonction pour générer le PDF
"""
def render_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

"""
Fonction pour générer une image de test
"""
def get_test_image():
    return SimpleUploadedFile(
        name='test.jpg',
        content=base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="),
        content_type='image/jpeg'
    )
