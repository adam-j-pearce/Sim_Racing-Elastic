# Getting Started

This project uses a Python3 virtual environment to ensure smoother development and easier creation of a working development
environment. To get started follow the below steps:

1. Create a development environment. If you call it `venv` it will be automatically ignored when commiting. If you change
the name please remember to update `.gitignore`:
    ```bash
    py -m venv venv
    ```
2. Activate the environment:
    ```bash 
    call venv\\Scripts\\activate
    ```
3. Install the project dependencies:
    ```
    pip install -r requirements.txt
    ```

If you have updated the enivornment with extra packages at any point in the development cycle. Please remember to run `pip freeze` to capture these changes in the requirements.txt file. 