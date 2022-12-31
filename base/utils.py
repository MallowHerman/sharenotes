# from pdf2image import convert_from_path, convert_from_bytes

# images = convert_from_path("/home/herman/Desktop/Projetos/Python/Django/sharemynotes/sharemynotes/media/Plano_de_sessão.pdf")

# for i in range(len(images)):
# 	images[1].save('page'+str(i)+'.png', 'PN')



import tempfile
from pathlib import Path
import os

from pdf2image import convert_from_path

def convert_pdf_to_image(pdf_file, thumbnail_name):
	BASE_DIR = Path.cwd()

	pdf_file = f"{BASE_DIR}{pdf_file}"
	output_folder = f"{BASE_DIR}/media/thumbnail/"
	images = convert_from_path(pdf_file, fmt="png", output_folder=output_folder, output_file=thumbnail_name, last_page=1)

	return images