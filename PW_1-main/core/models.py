from django.db import models

class PDF(models.Model):
    nombre = models.CharField(max_length=100)
    materia = models.CharField(max_length=100)
    carrera = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20)
    objetivos = models.TextField()#Para textos largos como fundamentos, bibliografia, etc
    condicion = models.CharField(max_length=50)
    curso = models.CharField(max_length=50)
    semestre = models.CharField(max_length=50)
    requisitos = models.TextField()
    carga_horaria_semanal = models.CharField(max_length=100)
    carga_horaria_semestral = models.CharField(max_length=100)
    fundamentacion = models.TextField()
    metodologia = models.TextField()
    evaluacion = models.TextField()
    bibliografia = models.TextField()
    

    def _str_(self):
        return self.archivo