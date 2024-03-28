# Invoice Parser App

## Summary

The Invoice Parser App is a web-based tool built using generative AI multimodel with Streamlit for parsing invoice images to extract relevant information such as invoice number, date, total amount, and item details. It provides a user-friendly interface for uploading one or more invoice images, parsing them, and generating a summary Excel file containing the parsed data.


## Installation

To use the Invoice Parser App locally, follow these steps:

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/invoice-parser-app.git
cd Invoice_Parser_Apps_With_Real_Time_Database
```

2. **Create a virtual environment based on the provided requirements.txt file:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
pip install -r requirements.txt
```

## How to use

1. **Activate the virtual environment:**

```bash
source venv_invoice/bin/activate  # On Windows, use venv\Scripts\activate
```

2. **Provide the GOOGLE_API_KEY**
   * Create .env file
   * Copy and paste your GOOGLE_API_KEY in the file
     GOOGLE_API_KEY = ""

4. **Run the Streamlit app:**

```bash
streamlit run app.py
```

## Additional Information
* This project uses Streamlit, a Python library for building web applications, and the PIL (Python Imaging Library) for image processing.
* Make sure to have Python installed on your system before setting up the project.
* For any issues or feature requests, please feel free to open an issue on the GitHub repository.
