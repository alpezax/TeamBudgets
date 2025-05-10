import json
import weasyprint
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

def generar_pdf(data: dict, output_path: str):
    # Configurar el entorno de Jinja2
    env = Environment(loader=FileSystemLoader('reports/templates'))
    template = env.get_template('invoice_template.html')

    # Renderizar el HTML con los datos
    html_content = template.render(
        mes=data['mes'],
        equipo_id=data['equipo-id'],
        equipo_nombre=data['equipo-nombre'],
        trabajadores=data['estructura-costes']['trabajadores'],
        total_coste=data['estructura-costes']['totales']['coste'],
        imputaciones=data['imputaciones']
    )

    # Convertir el HTML a PDF
    html = HTML(string=html_content)
    pdf = html.write_pdf(stylesheets=[weasyprint.CSS('reports/static/css/style.css')])

    # Guardar el PDF en la ruta indicada
    with open(output_path, 'wb') as f:
        f.write(pdf)

    print(f'Informe PDF generado: {output_path}')
