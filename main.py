import os
import google.generativeai as genai
from fpdf import FPDF

# ==========================================
# Step 1: Configure the AI
# ==========================================
def generate_ai_content(prompt):
    """Fetches text content from the Gemini API based on a prompt."""
    print(f"Asking AI: '{prompt}'...")
    
    # Ensure the API key is available in the environment
    api_key = os.environ.get("AIzaSyAy_ZAznF2z4Y_2wBOqjG2qII6rHj_R7rM")
    if not api_key:
        raise ValueError("Please set the GEMINI_API_KEY environment variable.")
        
    genai.configure(api_key=api_key)
    
    # We use Gemini 1.5 Flash as it is fast and excellent for text generation
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating content: {e}")
        return None

# ==========================================
# Step 2: Create the PDF Generator
# ==========================================
class PDFGenerator(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Title
        self.cell(0, 10, 'AI Generated Document', 0, 1, 'C')
        # Line break
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf(text_content, filename="output.pdf"):
    """Takes text and converts it into a formatted PDF."""
    print(f"Generating {filename}...")
    
    pdf = PDFGenerator()
    pdf.add_page()
    
    # Set font for the main body
    # Standard fpdf only supports a few built-in fonts without extra configuration
    pdf.set_font("Arial", size=11)
    
    # Encode text to latin-1 to avoid character errors with basic FPDF
    # Note: For full unicode support (emojis, complex symbols), consider using PyFPDF2 or ReportLab
    clean_text = text_content.encode('latin-1', 'replace').decode('latin-1')
    
    # Use multi_cell for text wrapping
    pdf.multi_cell(0, 7, clean_text)
    
    # Save the file
    pdf.output(filename)
    print("Done!")

# ==========================================
# Step 3: Run the Pipeline
# ==========================================
if __name__ == "__main__":
    # Define what you want the AI to write about
    user_topic = "Write a comprehensive essay explaining how quantum computing works to a high school student."
    
    # 1. Get the text from the AI
    ai_text = generate_ai_content(user_topic)
    
    # 2. If successful, write it to a PDF
    if ai_text:
        create_pdf(ai_text, "Quantum_Computing_Essay.pdf")