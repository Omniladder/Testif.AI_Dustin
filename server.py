from typing import Annotated
from typing import List
import logging
import sys
from typing import List, Optional

sys.path.append('.')
# from .pythonBackend import run
# for spencer
from pythonBackend import run
from starlette.responses import FileResponse
from fastapi import FastAPI, UploadFile, Form, Request, File
from pydantic import BaseModel, ValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory="templates")

class FormSettings(BaseModel):
    title: str
    course: str
    professor: str
    number_of_written_questions: int
    number_of_mcq_questions: int
    number_of_TF_questions: int
    level: str
    school_type: str
    difficulty: str
    testing_philosophy: str
    url_1: Optional[str] = None
    url_2: Optional[str] = None
    subject_material:List[UploadFile]


class QAPair(BaseModel):
    question:str
    answer: str
    q_type: str
    choices: List[str] = ['T', 'F'] #Holds Choices in a multiple Choice question
    
class GeneratedTest(BaseModel):
    questions:List[QAPair]

app = FastAPI()

app.mount("/TestifAi/static", StaticFiles(directory="static"), name="static")
#app.mount("/static/images", StaticFiles(directory="static/images"), name="images")
logger.info("Static files mounted")


#Used for converting Multiple Choice Numbers to Letters
def toLetter(num):
    return chr(num + 64)

templates.env.filters['toLetter'] = toLetter
logger.info("toLetter filter added to Jinja2 environment")

@app.get("/")
def read_index(request: Request):
    logger.info("GET request received for index page")
    return templates.TemplateResponse(
        request=request, name="form.html")


'''
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    # Log the validation error
    logger.error(f"Validation error occurred: {exc.errors()}")
    
    # Optionally, you can log specific details from the validation error
    for error in exc.errors():
        field = error.get('loc')  # Field that caused the error
        msg = error.get('msg')  # Message about the error
        logger.error(f"Field {field} failed validation: {msg}")
    
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )
'''

@app.post("/generate")
async def final(
    request: Request,
    title: str = Form(...),
    course: str = Form(...),
    professor: str = Form(...),
    number_of_written_questions: int = Form(...),
    number_of_mcq_questions: int = Form(...),
    number_of_TF_questions: int = Form(...),
    level: str = Form(...),
    school_type: str = Form(...),
    difficulty: str = Form(...),
    testing_philosophy: str = Form(...),
    subject_material: List[UploadFile] = File()
    
):

    data = FormSettings(
        title=title,
        course=course,
        professor=professor,
        number_of_written_questions=number_of_written_questions,
        number_of_mcq_questions=number_of_mcq_questions,
        number_of_TF_questions=number_of_TF_questions,
        level=level,
        school_type=school_type,
        difficulty=difficulty,
        testing_philosophy=testing_philosophy,
        subject_material=subject_material
    )

    logger.info("POST request received for /generate")
    logger.info(f"Form data: {data}")
    try:
        test = await run(data)
        print("Generated Test")
        logger.info("Test generated successfully")
    except Exception as e:
        logger.error(f"Error generating test: {e}")
        return templates.TemplateResponse(
            request=request, name="error.html", context={"error": str(e)}
        )

    # fake_response=GeneratedTest(questions=[QAPair(question="What is 2+2?", answer="4", type="written"),QAPair(question="What is 1+2?",answer="3" , type="written"),QAPair(question="What is 1+3?",answer="4" , type="multiple", choices=["1", "2", "3", "4"]), QAPair(question="Does 2+2=4?", answer="T", type="TF")] )

    return templates.TemplateResponse(
        request=request, name="finshed_test.html", 
        context={"Settings": data,"Test":test}
    )
