# Git y GitHub para Ciencia de Datos — material de las 3 sesiones

Tres sesiones de 2 horas para estudiantes de Ingeniería en Ciencia de Datos que
ya programan en Python pero nunca han versionado. Hilo conductor: al terminar,
cada estudiante tiene un perfil de GitHub con el proyecto del corte publicado
como pieza de portafolio y sabe trabajar en equipo sin pisarse el código.

## Archivos

| Archivo | Para quién | Qué es |
|---|---|---|
| `Sesion1_Mi_primer_repositorio.pptx` | docente | 13 diapositivas, con notas del orador |
| `Sesion2_Trabajar_en_equipo.pptx` | docente | 13 diapositivas, con notas del orador |
| `Sesion3_De_repositorio_a_portafolio.pptx` | docente | 12 diapositivas, con notas del orador |
| `Guia_del_estudiante_Git_y_GitHub.docx` | estudiante | tutorial paso a paso de las 3 sesiones, con «Si algo falla», retos y checklists (12 páginas) |
| `Hoja_de_comandos_Git.docx` | estudiante | los comandos en una página, para imprimir |
| `Guia_rapida_Dos_flujos_Git.docx` | estudiante | los dos flujos (local→GitHub y GitHub→local), el ciclo diario, tabla de errores reales y manejo de dos cuentas (4 páginas) |
| `Taller_Casa_Tu_Repositorio_del_Curso.docx` | estudiante | **taller autónomo de 4 h para hacer EN CASA** (11 págs.): instalar Git desde cero, clonar su repo de la U, crear el repositorio del curso con todo el material organizado, conectar, subir, y clonar repositorios ajenos. Rúbrica de 10 pts |
| `Taller_Git_Software_Carpentry.docx` | estudiante | taller evaluable (8 págs.) que sigue la lección abierta de Software Carpentry aplicándola a un repositorio de análisis de datos; incluye rúbrica de 10 pts |
| `crear_conflicto.sh` | ambos | script que crea un repo con un conflicto listo para resolver (sesión 2) |
| `proyecto_ejemplo/` | estudiante | plantilla de estructura de un proyecto de datos: README, .gitignore, requirements, LICENSE, carpetas (sesión 3) |

## Agenda resumida

| Sesión | Pregunta | Se llevan |
|---|---|---|
| 1 · Mi primer repositorio | ¿Cómo dejo de tener `dashboard_final_v3_AHORA_SI.py`? | Un repo publicado en GitHub y el hábito status → add → commit → push |
| 2 · Trabajar en equipo | ¿Cómo trabajamos cuatro personas sobre el mismo dashboard? | El repo del grupo con ramas, un conflicto resuelto y un Pull Request aprobado |
| 3 · De repositorio a portafolio | ¿Qué ve un reclutador cuando abre mi GitHub? | Perfil con el proyecto fijado y un README que lo vende |

## Antes de la sesión 2

Correr `bash crear_conflicto.sh` en una carpeta corta (por ejemplo `C:\Users\<usuario>\git_practica`)
para verificar que funciona en el equipo del salón. Crea la carpeta `demo_conflicto/`.

## Qué se dejó fuera a propósito

`rebase`, `stash`, `cherry-pick`, submódulos, GitHub Actions, DVC y SSH aparecen en una sola
diapositiva de «siguiente nivel» en la sesión 3. En 6 horas confunden más de lo que aportan.
