import PyInstaller.__main__
import os

gtk_path = r'C:\Program Files\GTK3-Runtime Win64\bin'
datas = [
    ('app/templates', 'app/templates'),
    ('app/static', 'app/static'),
]

# If GTK exists, bundle it into a 'bin/gtk3' folder inside the EXE
if os.path.exists(gtk_path):
    datas.append((gtk_path, 'bin/gtk3'))

PyInstaller.__main__.run([
    'app/main.py',
    '--name=InvoiceEngine',
    '--onefile',
    '--add-data=app/templates;app/templates',
    '--add-data=app/static;app/static',
    *([f'--add-data={gtk_path};bin/gtk3'] if os.path.exists(gtk_path) else []),
    '--hidden-import=weasyprint',
    '--hidden-import=jinja2',
    '--hidden-import=uvicorn.logging',
    '--hidden-import=uvicorn.loops',
    '--hidden-import=uvicorn.loops.auto',
    '--hidden-import=uvicorn.protocols',
    '--hidden-import=uvicorn.protocols.http',
    '--hidden-import=uvicorn.protocols.http.auto',
    '--hidden-import=uvicorn.protocols.websockets',
    '--hidden-import=uvicorn.protocols.websockets.auto',
    '--hidden-import=uvicorn.lifespan',
    '--hidden-import=uvicorn.lifespan.on',
    '--hidden-import=fastapi',
])
