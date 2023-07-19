from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def create_pdf_from_variable(value):
    buffer = BytesIO()  # Create an in-memory buffer to store the PDF content
    c = canvas.Canvas(buffer, pagesize=letter)

    # Add the text from the variable to the PDF
    c.drawString(100, 700, value)

    c.save()  # Save the canvas content to the buffer
    buffer.seek(0)  # Move the buffer's pointer to the beginning

    return buffer

if __name__ == "__main__":
    a = "hey its me"  # Replace this with your desired value

    pdf_buffer = create_pdf_from_variable(a)

    # Save the PDF content to a file and download it
    with open("output.pdf", "wb") as f:
        f.write(pdf_buffer.read())

    print("PDF created and downloaded successfully.")
