CROP DISEASE EXPERT SYSTEM - VS CODE

1. Open this folder in Visual Studio Code.

2. Open Terminal in VS Code.

3. Create virtual environment:
   python -m venv venv

4. Activate it in Windows PowerShell:
   venv\Scripts\Activate.ps1

   If PowerShell blocks activation, use Command Prompt:
   venv\Scripts\activate.bat

5. Install libraries:
   pip install -r requirements.txt

6. Run:
   python main.py

7. Click:
   Select Leaf Image
   -> choose JPG/PNG leaf image
   -> Analyze Image

The application extracts HSV/lesion/GLCM features, converts them
into symbolic facts, applies forward-chaining rules and displays
the disease, certainty factor and fired-rule explanation.

IMPORTANT:
This is an educational rule-based implementation. The image
thresholds are approximate and should not be treated as a medical
or agricultural diagnosis.
