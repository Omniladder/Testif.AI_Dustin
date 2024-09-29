import json
import os
from dotenv import load_dotenv
import logging
from typing import List

from PIL import Image
import pytesseract
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='chains.log',
    filemode='w'
)

from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader, UnstructuredPowerPointLoader

from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from pydantic import BaseModel
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser, PydanticOutputParser

class QAPair(BaseModel):
    question:str
    answer: str
    q_type: str
    choices: List[str] = ['T', 'F'] #Holds Choices in a multiple Choice question
    
class GeneratedTest(BaseModel):
    questions:List[QAPair]

# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     temperature=0.6,
#     api_key=os.getenv("OPENAI_API_KEY"),
# ) 

async def question_generate_chain(*, 
                            clean_response: str, 
                            llm, 
                            title, 
                            course, 
                            professor,
                            number_of_mcq_questions, 
                            number_of_TF_questions, 
                            number_of_written_questions,
                            school_type, 
                            difficulty, 
                            testing_philosophy,
                            ):
    question_generation_json_format, json_structure = get_json_format()
    question_generation_system_prompt, question_generation_human_prompt = get_templates()
    system_prompt = SystemMessagePromptTemplate.from_template(question_generation_system_prompt.template)
    human_prompt = HumanMessagePromptTemplate.from_template(question_generation_human_prompt.template)
    prompt = ChatPromptTemplate.from_messages(
        [
            system_prompt,
            human_prompt,
        ]
    )
    
    total_number_of_questions = number_of_mcq_questions + number_of_TF_questions + number_of_written_questions
    chain = await get_question_generate_chain(
        clean_response=clean_response,
        llm=llm,
        title=title,
        course=course,
        professor=professor,
        number_of_mcq_questions=number_of_mcq_questions,
        number_of_TF_questions=number_of_TF_questions,
        number_of_written_questions=number_of_written_questions,
        school_type=school_type,
        difficulty=difficulty,
        testing_philosophy=testing_philosophy,
        prompt=prompt,
        total_number_of_questions=total_number_of_questions,
        question_generation_json_format=question_generation_json_format,
        json_structure=json_structure,
        question_generation_system_prompt=question_generation_system_prompt,
        question_generation_human_prompt=question_generation_human_prompt
    )
    pydantic_return_object = await chain.ainvoke(
        {
            "QAPair_json_format": question_generation_json_format,
            "document": clean_response,
            "number_of_mcq_questions": number_of_mcq_questions,
            "number_of_TF_questions": number_of_TF_questions,
            "number_of_written_questions": number_of_written_questions,
            "school_type": school_type,
            "difficulty": difficulty,
            "testing_philosophy": testing_philosophy,
            "course": course,
            "title": title,
            "total_number_of_questions": total_number_of_questions,
            "json_structure": json_structure
        }
    )
    # print(pydantic_return_object)
    # input("Press Enter to continue...")
    return pydantic_return_object    
    
async def get_question_generate_chain(*, clean_response: str, llm, title, course, professor,
                            number_of_mcq_questions, number_of_TF_questions, number_of_written_questions,
                            school_type, difficulty, testing_philosophy, prompt,
                            question_generation_json_format, question_generation_system_prompt, question_generation_human_prompt,
                            total_number_of_questions, json_structure
                            ):
    parser = PydanticOutputParser(pydantic_object=GeneratedTest)
    chain = (
        RunnablePassthrough.assign(
            question_generation_system_prompt = lambda x: question_generation_system_prompt.format(
                QAPair_json_format=x["QAPair_json_format"],
                number_of_mcq_questions=x["number_of_mcq_questions"],
                number_of_TF_questions=x["number_of_TF_questions"],
                number_of_written_questions=x["number_of_written_questions"],
                difficulty=x["difficulty"],
                school_type=x["school_type"],
                testing_philosophy=x["testing_philosophy"],
                course=x["course"],
                title=x["title"],
                total_number_of_questions=x["total_number_of_questions"],
                json_structure=x["json_structure"]
            ),
            question_generation_human_prompt = lambda x: question_generation_human_prompt.format(
                document=x["document"],
                total_number_of_questions=x["total_number_of_questions"]
            )
        )
        | prompt
        | llm
        | parser
    )
    logging.info(f"Chain type: {type(chain)}")
    return chain

def get_templates():
    question_generation_system_prompt = PromptTemplate(
    template="""
    You are a teacher/professor's assistant tasked with generating them test questions and answers based on the provided document.
    
    You are assisting the teacher/professor in their {course} course. Analyze this course and determine the key concepts and topics that are important to the course.
    
    This course is for the following level of education: {school_type}
    The teacher wishes the test to be at the following difficulty: {difficulty}
    This is the teacher's testing philosophy: {testing_philosophy}
    
    For this test, you are to generate this many questions:
    {total_number_of_questions}
    
    Out of the {total_number_of_questions}, they are to be split up as follows:
    {number_of_mcq_questions} out of the {total_number_of_questions} question are to be multiple choice questions.
    {number_of_TF_questions} out of the {total_number_of_questions} question are to be true/false questions.
    {number_of_written_questions} out of the {total_number_of_questions} question are to be written questions.
    Ensure you follow this EXACT breakdown. Do not deviate from it. Do not generate more than the number of questions asked. Do not generate less than the number of questions asked.
    
    For multiple choice questions, you are to provide four choices, one of which is correct.
    For true/false questions, you are to provide two choices, one of which is correct.
    For written questions, you are to provide no choices.
    
    You should carefully read the document step by step and use it and only it to generate the questions, do not use any other information you already have or from any other sources. ONLY USE THE PROVIDED DOCUMENT.
    
    You are to provide your answer in the following JSON format:
    {json_structure}
    
    Here are examples for what the JSON format should look like:
    {QAPair_json_format}
    
    Only provide the JSON, no other information. Adhere to this JSON format EXACTLY. Always adhere to this JSON format.
    
    You are to use the following names for types:
    If multiple choice: "multiple_choice"
    if true/false: "TF"
    if written: "written"
        
    IMPORTANT: Always attempt to provide your answer in the JSON format. If you do not provide your answer in the JSON format, you have failed.
    IMPORTANT: Always generate the EXACT number of questions asked. Do not generate more, do not generate less.
    IMPORTANT: Always generate the exact amount of multiple choice questions asked. Do not generate more, do not generate less.
    IMPORTANT: Always generate the exact amount of true/false questions asked. Do not generate more, do not generate less.
    IMPORTANT: Always generate the exact amount of written questions asked. Do not generate more, do not generate less.
    IMPORTANT: Carefully read the document and use it to generate the questions. Do not use any other information you already have or from any other sources. ONLY USE THE PROVIDED DOCUMENT.
    """
    )

    question_generation_human_prompt = PromptTemplate(
        template = """
        Document:
        {document}
    """
    )
    
    return question_generation_system_prompt, question_generation_human_prompt

def get_json_format():
    QAPair_json_format = """
    {
        "questions": [
            {
                "question": "What is the capital of France?",
                "q_type": "multiple_choice",
                "answer": "Paris",
                "choices": [
                    "London",
                    "Berlin",
                    "Paris",
                    "Madrid"
                ]
            },
            {
                "question": "The Earth is flat.",
                "q_type": "TF",
                "answer": "False",
                "choices": [
                    "True",
                    "False"
                ]
            },
            {
                "question": "Explain the process of photosynthesis in plants.",
                "q_type": "written",
                "answer": "Photosynthesis is the process by which plants use sunlight, water, and carbon dioxide to produce oxygen and energy in the form of sugar.",
                "choices": []
            }
        ]
    }
    """
    
    json_structure = """
    {
        "questions": [
            {
                "question": "The full text of the question",
                "q_type": "The type of question: multiple_choice, TF, or written",
                "answer": "The correct answer to the question",
                "choices": [
                    "For multiple_choice: First choice",
                    "For multiple_choice: Second choice",
                    "For multiple_choice: Third choice",
                    "For multiple_choice: Fourth choice"
                ]
            },
            {
                "question": "The full text of a true/false question",
                "q_type": "TF",
                "answer": "The correct answer: True or False",
                "choices": [
                    "Always True",
                    "Always False"
                ]
            },
            {
                "question": "The full text of a written question",
                "q_type": "written",
                "answer": "The expected answer or key points for the written question",
                "choices": []
            }
        ]
    }
    """
    
    return QAPair_json_format, json_structure


    