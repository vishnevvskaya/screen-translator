from paddleocr import PaddleOCR
import os

os.makedirs('paddle_models', exist_ok=True)

model = PaddleOCR(
    lang='en', # select the recognition language
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    device='gpu', 
)

print("Models successfully downloaded!")