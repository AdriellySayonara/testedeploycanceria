import os
import base64
import traceback
import pdfkit


def generate_exam_pdf(report_data):
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        pdf_ufpe_logo_path = os.path.join(path, 'pdfTemplate', 'ufpe.jpg')
        pdf_style_path = os.path.join(path, 'pdfTemplate', 'styles.css')
        pdf_html_path = os.path.join(path, 'pdfTemplate', 'index.html')

        exam_image_base64 = ''
        with open(os.path.join('privateFiles', report_data['exam_image']), "rb") as img_file:
            exam_image_base64 = base64.b64encode(img_file.read()).decode("utf-8")

        text = ''
        with open(pdf_html_path, "r", encoding='utf-8') as f:
            text = f.read()

        filepath = os.path.join('examPDFFiles', report_data['exam_image'])
        pdfkit.from_string(text.format(pdf_style_path=pdf_style_path,
                                       pdf_ufpe_logo_path=pdf_ufpe_logo_path,
                                       exam_image_base64=exam_image_base64,
                                       patient_name=report_data['patient_name'],
                                       patient_numSUS=report_data['patient_numSUS'],
                                       patient_dataNasc=report_data['patient_dataNasc'],
                                       patient_obs=report_data['patient_obs'],
                                       classifier_name=report_data['classifier_name'],
                                       exam_title=report_data['exam_title'],
                                       exam_label=report_data['exam_label'],
                                       exam_result=report_data['exam_result'],
                                       ), filepath, options={
            "enable-local-file-access": None
        })

        return filepath
    except Exception:
        print(traceback.format_exc())

    return None
