# Testif.AI

![Testif.AI](./static/logo.png)

> [!IMPORTANT]
> We're pleased to announce that Testif.AI won best Educational and 2nd best Overall Hack at [HackUMBC](https://www.hackumbc.tech) 2024!
>
> If you find this project useful, please consider giving us a star!

## About the Project

Making a test can take a long time. You have to review the material you want to test, select the most important topics, write out questions and create an answer key. This can take hours especially for complex subjects.

Making a test can take a long time. You have to review the material you want to test, select the most important topics, write out questions and create an answer key. This can take hours especially for complex subjects.

In order to address this issue, we created Testif.AI, an AI powered test creation assistant. The teacher can start by setting information about the test - the test name, the course name and the professors name. Then, they will select the number and style of questions the test should include. After that, the teacher will be able to select the difficulty and grade level so the test is an appropriate difficulty. The teacher will then have the chance to give information about their testing philosophy to make sure the generated test reflects the teachers desires and teaching style. Lastly, the teacher can upload any .pdf, .pptx, .txt, .doc, .docx, .png, .jpeg, or .jpg file and generate a test. Once the test generation is complete, the teacher can edit the answer key and test before exporting them as pdfs.

Though this solution is primarily for teachers, it is also a great tool for students! Creating practice tests and taking them is a great study strategy. By lowering the barrier of entry for test creation, students can quickly make practice tests to hone their skills.

Learning is important to our team and to the world. We've made a meaningful contribution to the world of education by simplifying the process of test creation for teachers and students alike.

## Technical Details

Testif.AI has a frontend built with HTML, CSS and Javascript. When the user fills out the test generation form a request is sent to our FastAPI backend which calls Langchain (a generative AI framework) and uses a variety of techniques including mixture of experts, retrieval augmented generation, and prompt chaining to generate a great test that meets the users specifications

## About the Team

Our team consists of:

- [Spencer Presley](https://github.com/spencerpresley)
- [Dustin O'Brien](https://github.com/Omniladder)
- [Isaac Dugan](https://github.com/idugan100)
- [JJ McCauley](https://github.com/Jairik)

We are all students from Salisbury University. Go Gulls!

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

## How to run using uv

[uv](https://github.com/astral-sh/uv) is a python package manager written in rust, and is much faster than using something like pip.

1. Install uv:

    ```bash
    # On macOS
    brew install uv

    # On Unix/Linux/macOS (alternative method)
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # On Windows
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

2. Create and activate a new virtual environment:

    ```bash
    uv venv
    source .venv/bin/activate  # On Unix/macOS
    # or
    .venv\Scripts\activate  # On Windows
    ```

3. Install dependencies using uv:

    ```bash
    uv pip install -r requirements.txt
    ```

4. Run the server:

    ```bash
    uvicorn server:app
    ```

5. Open the frontend in your browser:

    ```bash
    http://127.0.0.1:8000
    ```

> [!NOTE]
> Using uv can significantly speed up dependency installation,
> especially in projects with many requirements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
