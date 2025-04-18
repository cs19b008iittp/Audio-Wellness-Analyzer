
Follow these steps to set up the project locally:

### 1. Download the Project

First, download the project as a **ZIP** file from the GitHub repository:

1. Go to the GitHub repository: [Repository URL](https://github.com/cs19b008iittp/Audio-Wellness-Analyzer.git)
2. Click the "Code" button, and select "Download ZIP".
3. Extract the ZIP file to a location of your choice on your computer.

### 2. Set Up a Virtual Environment

Navigate to the project folder where you extracted the ZIP file. Then, follow these steps to set up a Python virtual environment:

#### For Windows:

```bash
# Navigate to the project folder
cd path/to/your/project

# Create a virtual environment
python -m venv myenv

# Activate the virtual environment
myenv\Scripts\activate

```

### 3. Install the Required Dependencies

To install the dependencies for this project, run the following command:

```bash

pip install -r requirements.txt

```

### 4. Run the Application Locally

Use the following command to start the server:

```bash

uvicorn main:app --reload

```

This command will run the FastAPI application on http://127.0.0.1:8000. You can access the app by opening your browser and navigating to this URL.

The --reload flag makes the server restart upon code changes, which is useful during development.

### 5. Test the Application

Once the server is running, open your web browser and navigate to: http://127.0.0.1:8000

### 6.Deactivating the Virtual Environment

When you are done working with the project, you can deactivate the virtual environment by running:

```bash

deactivate

```







