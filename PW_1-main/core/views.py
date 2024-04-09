from django.shortcuts import render, redirect
from .models import PDF
import PyPDF2
import re

def import_success(request):
    return render(request, 'import_success.html')


def importar_pdf(request):
    if request.method == 'POST' and request.FILES.getlist('pdf_files'):
        pdf_files = request.FILES.getlist('pdf_files')

        for pdf_file in pdf_files:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            # page = pdf_reader.pages[0]
            text = ""
            # Iterar sobre todas las páginas del PDF
            for no_page in range(len(pdf_reader.pages)):
                info_page = pdf_reader._get_page(no_page)
                text += info_page.extract_text()


            nombre_archivo = pdf_file.name
            materia = None
            codigo = None
            carrera = None
            objetivos_text = None
            condicion = None
            curso = None
            semestre = None
            requisitos = None
            carga_horaria_semanal = None
            carga_horaria_semestral = None
            fundamentacion = None
            metodologia = None
            evaluacion = None
            bibliografia = None

            # Extraer datos del PDF
            materia_match = re.search(r'Nombre\s*de\s*la\s*Materia\s*:\s*(.*)', text)
            materia = materia_match.group(1).strip() if materia_match else None
            materia = re.sub(r'\.\s*$', '', materia) if materia else None

            codigo_match = re.search(r'Código\s*:\s*(.*)', text)
            codigo = codigo_match.group(1).strip().replace(" ", "") if codigo_match else None
            codigo = re.sub(r'\.\s*$', '', codigo) if codigo else None

            carrera_match = re.search(r'Carrera\s*:\s*(.*)', text)
            carrera = carrera_match.group(1).strip() if carrera_match else None
            carrera = re.sub(r'\.\s*$', '', carrera) if carrera else None

            objetivos_match = re.search(r'OBJETIVOS\s*(?:\. )?(.*?)(?=IV.|$)', text, re.DOTALL)
            objetivos_text = objetivos_match.group(1).strip() if objetivos_match else None

            condicion_match = re.search(r'Condición\s*:\s*(.*)', text)
            condicion = condicion_match.group(1).strip() if condicion_match else None

            curso_match = re.search(r'Curso\s*:\s*(.*)', text)
            curso = curso_match.group(1).strip() if curso_match else None

            semestre_match = re.search(r'Semestre\s*:\s*(.*)', text)
            semestre = semestre_match.group(1).strip() if semestre_match else None

            requisitos_match = re.search(r'Requisitos\s*:\s*(.*)', text)
            requisitos = requisitos_match.group(1).strip() if requisitos_match else None

            carga_horaria_semanal_match = re.search(r'Carga\s*horaria\s*semanal\s*:\s*(.*)', text, re.IGNORECASE)
            carga_horaria_semanal = carga_horaria_semanal_match.group(1).strip() if carga_horaria_semanal_match else None

            carga_horaria_semestral_match = re.search(r'Carga\s*horaria\s*semestral\s*:\s*(.*)', text, re.IGNORECASE)
            carga_horaria_semestral = carga_horaria_semestral_match.group(1).strip() if carga_horaria_semestral_match else None

            fundamentacion_match = re.search(r'FUNDAMENTACIÓN\s*(?:\. )?(.*?)(?=III.|$)', text, re.DOTALL)
            fundamentacion = fundamentacion_match.group(1).strip() if fundamentacion_match else None

            metodologia_match = re.search(r'METODOLOGÍA\s*(?:\. )?(.*?)(?=VI.|$)', text, re.DOTALL)
            metodologia = metodologia_match.group(1).strip() if metodologia_match else None

            evaluacion_match = re.search(r'EVALUACIÓN\s*(?:\. )?(.*?)(?=VII.|$)', text, re.DOTALL)
            evaluacion = evaluacion_match.group(1).strip() if evaluacion_match else None

            bibliografia_match = re.search(r'BIBLIOGRAFÍA\s*(?:\. )?(.*?)(?=$)', text, re.DOTALL)
            bibliografia = bibliografia_match.group(1).strip() if bibliografia_match else None

            # Guardar en la base de datos
            pdf = PDF(nombre=nombre_archivo, materia=materia, carrera=carrera, codigo=codigo, objetivos=objetivos_text, 
                      condicion=condicion, curso=curso, semestre=semestre, requisitos=requisitos,
                      carga_horaria_semanal=carga_horaria_semanal, carga_horaria_semestral=carga_horaria_semestral,
                      fundamentacion=fundamentacion, metodologia=metodologia, evaluacion=evaluacion,
                      bibliografia=bibliografia)
            pdf.save()

        return redirect('import_success')
    return render(request, 'import_pdf.html')