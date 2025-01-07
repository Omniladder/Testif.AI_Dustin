# Testif.AI

![Testif.AI](./static/logo.png)

> [!IMPORTANT]
> We're pleased to announce that Testif.AI won best Educational and 2nd best Overall Hack at [HackUMBC](https://www.hackumbc.tech) 2024!

## About the Project

Making a test can take a long time. You have to review the material you want to test, select the most important topics, write out questions and create an answer key. This can take hours especially for complex subjects.

Making a test can take a long time. You have to review the material you want to test, select the most important topics, write out questions and create an answer key. This can take hours especially for complex subjects.

In order to address this issue, we created Testif.AI, an AI powered test creation assistant. The teacher can start by setting information about the test - the test name, the course name and the professors name. Then, they will select the number and style of questions the test should include. After that, the teacher will be able to select the difficulty and grade level so the test is an appropriate difficulty. The teacher will then have the chance to give information about their testing philosophy to make sure the generated test reflects the teachers desires and teaching style. Lastly, the teacher can upload any .pdf, .pptx, .txt, .doc, .docx, .png, .jpeg, or .jpg file and generate a test. Once the test generation is complete, the teacher can edit the answer key and test before exporting them as pdfs.

Though this solution is primarily for teachers, it is also a great tool for students! Creating practice tests and taking them is a great study strategy. By lowering the barrier of entry for test creation, students can quickly make practice tests to hone their skills.

Learning is important to our team and to the world. We've made a meaningful contribution to the world of education by simplifying the process of test creation for teachers and students alike.

## Technical Details

Testif.AI has a frontend built with HTML, CSS and Javascript. When the user fills out the test generation form a request is sent to our FastAPI backend which calls Langchain (a generative AI framework) and uses a variety of techniques including mixture of experts, retrieval augmented generation, and prompt chaining to generate a great test that meets the users specifications

## About the Team

Our team consists of Spencer Presley, Dustin O'Brien, Isaac Dugan, and JJ McCauley. We are all students from Salisbury University. Go Gulls!

## How to run

1. Clone the repository

    ```bash
    git clone https://github.com/spencerpresley/TestifAI.git && cd TestifAI
    ```

2. Install the dependencies

    ```bash
    pip install -r requirements.txt
    ```

3. Run the server

    ```bash
    uvicorn server:app
    ```

4. Open the frontend in your browser

    ```bash
    http://127.0.0.1:8000
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
