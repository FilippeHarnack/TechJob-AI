from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from app.services.file_parser import extract_text_from_pdf, extract_text_from_docx
from app.services.openai_integration import generate_job_suggestions

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <h2>Upload de Currículo</h2>
    <form action="/upload" enctype="multipart/form-data" method="post">
        <input name="file" type="file">
        <input type="submit" value="Enviar">
    </form>
    """

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    file_path = f"temp_{file.filename}"
    
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Extrair texto do arquivo
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file.filename.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        return {"error": "Formato de arquivo não suportado"}
    
    # Gerar sugestões de vagas com OpenAI
    job_suggestions = generate_job_suggestions(text)
    
    return {"filename": file.filename, "suggestions": job_suggestions}
