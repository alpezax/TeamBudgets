import json
import weasyprint
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

def generar_pdf_balance(data: dict, output_path: str):
    env = Environment(loader=FileSystemLoader('reports/templates'))
    template = env.get_template('balance_template.html')

    html_content = template.render(
        nombre_balance=data['nombre_balance'],
        mes=data['mes'],
        año=data['año'],
        equipo_ref=data['equipo']['ref'],
        imputaciones=data['imputaciones'],
        imputacionespersona=data['imputaciones-persona'],
        total_balance=data['total_balance']
    )

    html = HTML(string=html_content)
    pdf = html.write_pdf(stylesheets=[weasyprint.CSS('reports/static/css/style.css')])

    with open(output_path, 'wb') as f:
        f.write(pdf)

    print(f'PDF generado: {output_path}')
