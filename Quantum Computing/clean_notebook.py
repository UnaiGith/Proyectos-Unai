import nbformat
import os

# Usamos una ruta relativa que incluya la carpeta
filename = 'Quantum Computing/Mermin_Peres_Quantum_Telepathy_UnaiGarrido.ipynb'

# Verificación de seguridad para avisarte si la ruta es correcta
if not os.path.exists(filename):
    print(f"Error: No se encuentra el archivo en {os.path.abspath(filename)}")
else:
    with open(filename, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    if 'widgets' in nb.metadata:
        print("Sección 'widgets' encontrada. Eliminando...")
        del nb.metadata['widgets']
    else:
        print("No se encontró la sección 'widgets' en los metadatos.")

    with open(filename, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("¡Archivo limpiado con éxito!")