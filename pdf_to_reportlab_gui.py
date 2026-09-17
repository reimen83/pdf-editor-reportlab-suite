import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pdf_to_reportlab as ptr

class PDFSuiteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Editor & ReportLab Suite")
        self.root.geometry("680x520")
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.aba_extracao = ttk.Frame(self.notebook)
        self.aba_compilacao = ttk.Frame(self.notebook)
        self.aba_clonar = ttk.Frame(self.notebook)
        
        self.notebook.add(self.aba_extracao, text="1. PDF -> Python")
        self.notebook.add(self.aba_compilacao, text="2. Python -> PDF")
        self.notebook.add(self.aba_clonar, text="3. Clonar Layout (Fusão)")
        
        self.setup_aba_extracao()
        self.setup_aba_compilacao()
        self.setup_aba_clonar()
        
    def setup_aba_extracao(self):
        lbl = ttk.Label(self.aba_extracao, text="Extrair PDF para Código Python Editável", font=('Helvetica', 12, 'bold'))
        lbl.pack(pady=10)
        
        btn_sel = ttk.Button(self.aba_extracao, text="Selecionar PDF e Gerar Script .py", command=self.extrair_pdf)
        btn_sel.pack(pady=20)

    def setup_aba_compilacao(self):
        lbl = ttk.Label(self.aba_compilacao, text="Recompilar Código Python em PDF Final", font=('Helvetica', 12, 'bold'))
        lbl.pack(pady=10)
        
        btn_sel = ttk.Button(self.aba_compilacao, text="Selecionar Script .py e Gerar PDF", command=self.compilar_py)
        btn_sel.pack(pady=20)

    def setup_aba_clonar(self):
        lbl = ttk.Label(self.aba_clonar, text="Transferência de Estilo Visual entre PDFs", font=('Helvetica', 12, 'bold'))
        lbl.pack(pady=10)
        
        frame_a = ttk.Frame(self.aba_clonar)
        frame_a.pack(fill='x', padx=20, pady=5)
        ttk.Label(frame_a, text="1. PDF de Referência (Design/Layout):").pack(anchor='w')
        self.ent_pdf_a = ttk.Entry(frame_a, width=50)
        self.ent_pdf_a.pack(side='left', fill='x', expand=True, padx=(0, 5))
        ttk.Button(frame_a, text="Buscar...", command=self.selecionar_pdf_a).pack(side='right')

        frame_b = ttk.Frame(self.aba_clonar)
        frame_b.pack(fill='x', padx=20, pady=5)
        ttk.Label(frame_b, text="2. PDF de Destino (Seu Conteúdo):").pack(anchor='w')
        self.ent_pdf_b = ttk.Entry(frame_b, width=50)
        self.ent_pdf_b.pack(side='left', fill='x', expand=True, padx=(0, 5))
        ttk.Button(frame_b, text="Buscar...", command=self.selecionar_pdf_b).pack(side='right')

        btn_exec = ttk.Button(self.aba_clonar, text="🚀 Aplicar Estilo e Gerar Novo PDF", command=self.executar_fusao)
        btn_exec.pack(pady=25)

    def selecionar_pdf_a(self):
        path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if path:
            self.ent_pdf_a.delete(0, tk.END)
            self.ent_pdf_a.insert(0, path)

    def selecionar_pdf_b(self):
        path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if path:
            self.ent_pdf_b.delete(0, tk.END)
            self.ent_pdf_b.insert(0, path)

    def extrair_pdf(self):
        pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if pdf_path:
            output_py = os.path.splitext(pdf_path)[0] + "_editavel.py"
            messagebox.showinfo("Sucesso", f"Script gerado em:\n{output_py}")

    def compilar_py(self):
        py_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if py_path:
            os.system(f"python3 {py_path}")
            messagebox.showinfo("Sucesso", "PDF Recompilado com sucesso!")

    def executar_fusao(self):
        pdf_a = self.ent_pdf_a.get()
        pdf_b = self.ent_pdf_b.get()
        
        if not pdf_a or not pdf_b:
            messagebox.showwarning("Atenção", "Por favor, selecione ambos os arquivos PDF.")
            return
            
        pdf_saida = os.path.splitext(pdf_b)[0] + "_estilizado.pdf"
        
        try:
            ptr.clonar_layout_e_aplicar(pdf_a, pdf_b, pdf_saida)
            messagebox.showinfo("Sucesso!", f"Novo PDF gerado com sucesso em:\n{pdf_saida}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao realizar fusão:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFSuiteApp(root)
    root.mainloop()
