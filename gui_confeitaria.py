import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from modelo_confeitaria import SistemaConfeitaria


class SistemaConfeitariaGUI:
    def __init__(self, root):
        # Inicializar o modelo
        self.sistema = SistemaConfeitaria()

        # Configurar a janela principal
        self.root = root
        self.root.title("Donna Luiza - Sistema de Confeitaria")
        self.root.geometry("850x650")
        self.root.minsize(700, 500)

        # Cor de fundo
        self.root.configure(bg="#FFDAB9")

        # Configuração de estilos
        self.configurar_estilos()

        # Criar menu principal
        self.criar_menu_principal()

        # Criar footer
        self.criar_footer()

    def configurar_estilos(self):
        # Configurar estilo para os widgets
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#FFDAB9")
        self.style.configure("TButton", font=("Arial", 11), padding=6)
        self.style.configure("TLabel", background="#FFDAB9", font=("Arial", 11))
        self.style.configure("Header.TLabel", font=("Arial", 16, "bold"))
        self.style.configure("Title.TLabel", font=("Arial", 22, "bold"))

        # Cores personalizadas
        self.cor_principal = "#ff9999"  # Rosa claro
        self.cor_secundaria = "#ffcccc"  # Rosa mais claro
        self.cor_texto = "#333333"  # Cinza escuro

    def limpar_frame(self):
        """Limpa todos os widgets do frame principal."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def criar_menu_principal(self):
        """Cria o menu principal da aplicação."""
        self.limpar_frame()

        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Adicionar a logo
        try:
            # Carregar a imagem da logo
            self.logo_img = tk.PhotoImage(file="logo_confeitaria.png")

            # Redimensionar a imagem (opcional)
            largura_desejada = 150
            altura_desejada = int(self.logo_img.height() * (largura_desejada / self.logo_img.width()))
            if largura_desejada > 0 and altura_desejada > 0:
                subsample_width = max(1, self.logo_img.width() // largura_desejada)
                subsample_height = max(1, self.logo_img.height() // altura_desejada)
                self.logo_img = self.logo_img.subsample(subsample_width, subsample_height)

            # Criar Label para exibir a logo
            logo_label = tk.Label(main_frame, image=self.logo_img, background="#FFDAB9")
            logo_label.image = self.logo_img  # Manter referência para evitar garbage collection
            logo_label.pack(pady=(0, 20))  # Espaçamento abaixo da logo

        except tk.TclError:
            # Se a imagem não for encontrada, exibir uma mensagem de erro
            erro_label = ttk.Label(main_frame, text="Erro: Logo não encontrada!", style="Header.TLabel")
            erro_label.pack(pady=(0, 20))

        # Título modificado
        titulo_label = ttk.Label(main_frame, text="Donna Luiza", style="Title.TLabel")
        titulo_label.pack()

        subtitulo_label = ttk.Label(main_frame, text="Registro de Receitas", style="Header.TLabel")
        subtitulo_label.pack(pady=(0, 30))

        # Botões do menu principal
        frame_botoes = ttk.Frame(main_frame)
        frame_botoes.pack(pady=20)

        # Botão para ver receitas
        btn_ver_receitas = ttk.Button(
            frame_botoes,
            text="Ver Receitas Registradas",
            command=self.mostrar_lista_receitas,
            width=30
        )
        btn_ver_receitas.pack(pady=10)

        # Botão para registrar receita
        btn_registrar_receita = ttk.Button(
            frame_botoes,
            text="Registrar Nova Receita",
            command=self.mostrar_form_registro,
            width=30
        )
        btn_registrar_receita.pack(pady=10)

        # Botão para sair
        btn_sair = ttk.Button(
            frame_botoes,
            text="Sair do Sistema",
            command=self.root.quit,
            width=30
        )
        btn_sair.pack(pady=10)

        # Adicionar imagem ou decoração (opcional)
        lbl_info = ttk.Label(main_frame, text="Sistema para gerenciamento de receitas de confeitaria")
        lbl_info.pack(side=tk.BOTTOM, pady=20)

    def mostrar_lista_receitas(self):
        """Mostra a lista de receitas registradas."""
        self.limpar_frame()

        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        ttk.Label(main_frame, text="Receitas Registradas", style="Title.TLabel").pack(pady=(0, 20))

        # Frame para lista e detalhes
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Frame da lista de receitas
        list_frame = ttk.Frame(content_frame)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Barra de rolagem para a lista
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Lista de receitas
        self.lista_receitas = tk.Listbox(
            list_frame,
            font=("Arial", 11),
            height=15,
            selectbackground=self.cor_principal,
            selectforeground="white"
        )
        self.lista_receitas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configurar barra de rolagem
        self.lista_receitas.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.lista_receitas.yview)

        # Preencher lista com receitas
        receitas = self.sistema.obter_todas_receitas()
        if not receitas:
            self.lista_receitas.insert(tk.END, "Não há receitas registradas")
        else:
            for receita in receitas:
                self.lista_receitas.insert(tk.END, f"{receita['id']}. {receita['nome']} ({receita['tipo']})")

        # Frame para detalhes da receita
        self.detalhe_frame = ttk.Frame(content_frame)
        self.detalhe_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # Área de texto para mostrar detalhes
        ttk.Label(self.detalhe_frame, text="Detalhes da Receita", style="Header.TLabel").pack(pady=(0, 10))

        self.texto_detalhes = scrolledtext.ScrolledText(
            self.detalhe_frame,
            wrap=tk.WORD,
            width=40,
            height=15,
            font=("Arial", 11)
        )
        self.texto_detalhes.pack(fill=tk.BOTH, expand=True)
        self.texto_detalhes.config(state=tk.DISABLED)

        # Vincular seleção da lista à exibição de detalhes
        self.lista_receitas.bind('<<ListboxSelect>>', self.mostrar_detalhes_receita)

        # Botões
        botoes_frame = ttk.Frame(main_frame)
        botoes_frame.pack(fill=tk.X, pady=20)

        btn_voltar = ttk.Button(
            botoes_frame,
            text="Voltar ao Menu Principal",
            command=self.criar_menu_principal
        )
        btn_voltar.pack(side=tk.RIGHT)

    def mostrar_detalhes_receita(self, event):
        """Mostra os detalhes da receita selecionada."""
        receitas = self.sistema.obter_todas_receitas()
        if not receitas:
            return

        try:
            # Obter índice selecionado
            index = self.lista_receitas.curselection()[0]
            linha_selecionada = self.lista_receitas.get(index)

            # Extrair ID da receita
            id_receita = int(linha_selecionada.split('.')[0])

            # Buscar receita pelo ID
            receita = self.sistema.obter_receita_por_id(id_receita)

            if receita:
                # Habilitar edição para atualizar o texto
                self.texto_detalhes.config(state=tk.NORMAL)
                self.texto_detalhes.delete(1.0, tk.END)

                # Adicionar detalhes da receita
                detalhes = f"ID: {receita['id']}\n"
                detalhes += f"Nome: {receita['nome']}\n"
                detalhes += f"Tipo: {receita['tipo']}\n\n"
                detalhes += f"Materiais Base:\n{', '.join(receita['materiais_base'])}\n\n"
                detalhes += f"Materiais Decoração:\n{', '.join(receita['materiais_decoracao'])}\n\n"
                detalhes += f"Embalagem: {receita['embalagem']}\n"
                detalhes += f"Precisa de Caixa para Transporte: {'Sim' if receita['precisa_caixa_transporte'] else 'Não'}\n\n"

                if receita.get('observacoes'):
                    detalhes += f"Observações:\n{receita['observacoes']}\n\n"

                detalhes += f"Data de Registro: {receita['data_registro']}"

                self.texto_detalhes.insert(tk.END, detalhes)
                self.texto_detalhes.config(state=tk.DISABLED)  # Desabilitar edição
        except (IndexError, ValueError):
            pass

    def mostrar_form_registro(self):
        """Mostra o formulário para registro de uma nova receita."""
        self.limpar_frame()

        # Frame principal com barra de rolagem
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas e scrollbar para permitir rolagem
        canvas = tk.Canvas(main_frame, bg="#FFDAB9", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="TFrame")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")

        # Título
        ttk.Label(scrollable_frame, text="Registrar Nova Receita", style="Title.TLabel").pack(pady=(0, 20))

        # Campos do formulário
        form_frame = ttk.Frame(scrollable_frame)
        form_frame.pack(fill=tk.X, pady=10)

        # Nome da receita
        ttk.Label(form_frame, text="Nome da Receita:").pack(anchor=tk.W, pady=(10, 5))
        self.nome_entry = ttk.Entry(form_frame, width=50)
        self.nome_entry.pack(fill=tk.X, pady=(0, 10))

        # Tipo de receita
        ttk.Label(form_frame, text="Tipo de Receita:").pack(anchor=tk.W, pady=(10, 5))

        tipo_frame = ttk.Frame(form_frame)
        tipo_frame.pack(fill=tk.X, pady=(0, 10))

        self.tipo_var = tk.StringVar()
        self.tipos = ["Bolo", "Torta", "Cupcake", "Doce", "Outro"]
        self.tipo_combobox = ttk.Combobox(tipo_frame, textvariable=self.tipo_var, values=self.tipos, state="readonly")
        self.tipo_combobox.current(0)  # Seleciona "Bolo" por padrão
        self.tipo_combobox.pack(side=tk.LEFT)

        # Campo para especificar outro tipo
        ttk.Label(tipo_frame, text=" Se Outro, especifique:").pack(side=tk.LEFT, padx=(10, 5))
        self.outro_tipo_entry = ttk.Entry(tipo_frame, width=20)
        self.outro_tipo_entry.pack(side=tk.LEFT)

        # Vincular evento de mudança no combobox
        self.tipo_combobox.bind("<<ComboboxSelected>>", self.verificar_tipo_outro)

        # Materiais base
        ttk.Label(form_frame, text="Materiais Base (separados por vírgula):").pack(anchor=tk.W, pady=(10, 5))
        self.materiais_base_text = scrolledtext.ScrolledText(form_frame, wrap=tk.WORD, height=4)
        self.materiais_base_text.pack(fill=tk.X, pady=(0, 10))

        # Materiais decoração
        ttk.Label(form_frame, text="Materiais Decoração (separados por vírgula):").pack(anchor=tk.W, pady=(10, 5))
        self.materiais_decoracao_text = scrolledtext.ScrolledText(form_frame, wrap=tk.WORD, height=4)
        self.materiais_decoracao_text.pack(fill=tk.X, pady=(0, 10))

        # Embalagem
        ttk.Label(form_frame, text="Embalagem:").pack(anchor=tk.W, pady=(10, 5))
        self.embalagem_entry = ttk.Entry(form_frame, width=50)
        self.embalagem_entry.pack(fill=tk.X, pady=(0, 10))

        # Caixa de transporte
        self.caixa_var = tk.BooleanVar(value=False)
        caixa_check = ttk.Checkbutton(form_frame, text="Precisa de caixa para transporte", variable=self.caixa_var)
        caixa_check.pack(anchor=tk.W, pady=10)

        # Observações
        ttk.Label(form_frame, text="Observações (opcional):").pack(anchor=tk.W, pady=(10, 5))
        self.observacoes_text = scrolledtext.ScrolledText(form_frame, wrap=tk.WORD, height=4)
        self.observacoes_text.pack(fill=tk.X, pady=(0, 10))

        # Botões
        botoes_frame = ttk.Frame(scrollable_frame)
        botoes_frame.pack(fill=tk.X, pady=20)

        btn_cancelar = ttk.Button(
            botoes_frame,
            text="Cancelar",
            command=self.criar_menu_principal
        )
        btn_cancelar.pack(side=tk.RIGHT, padx=5)

        btn_salvar = ttk.Button(
            botoes_frame,
            text="Salvar Receita",
            command=self.salvar_nova_receita
        )
        btn_salvar.pack(side=tk.RIGHT, padx=5)

    def verificar_tipo_outro(self, event):
        """Verifica se o tipo selecionado é 'Outro' e ajusta o campo 'outro_tipo_entry'."""
        if self.tipo_var.get() == "Outro":
            self.outro_tipo_entry.config(state="normal")
        else:
            self.outro_tipo_entry.delete(0, tk.END)
            self.outro_tipo_entry.config(state="disabled")

    def salvar_nova_receita(self):
        """Salva uma nova receita com base nos dados do formulário."""
        # Obter dados do formulário
        nome = self.nome_entry.get().strip()

        # Determinar o tipo
        tipo = self.tipo_var.get()
        if tipo == "Outro":
            outro_tipo = self.outro_tipo_entry.get().strip()
            if outro_tipo:
                tipo = outro_tipo

        # Processar materiais
        materiais_base = self.materiais_base_text.get("1.0", tk.END).strip()
        materiais_base_lista = [m.strip() for m in materiais_base.split(',') if m.strip()]

        materiais_decoracao = self.materiais_decoracao_text.get("1.0", tk.END).strip()
        materiais_decoracao_lista = [m.strip() for m in materiais_decoracao.split(',') if m.strip()]

        embalagem = self.embalagem_entry.get().strip()
        precisa_caixa = self.caixa_var.get()
        observacoes = self.observacoes_text.get("1.0", tk.END).strip()

        # Registrar receita usando o modelo
        sucesso, mensagem = self.sistema.registrar_receita(
            nome,
            tipo,
            materiais_base_lista,
            materiais_decoracao_lista,
            embalagem,
            precisa_caixa,
            observacoes
        )

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.criar_menu_principal()
        else:
            messagebox.showerror("Erro", mensagem)

    def criar_footer(self):
        """Cria um footer na parte inferior da janela."""
        footer_frame = tk.Frame(self.root, bg="black", height=30)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        footer_label = tk.Label(
            footer_frame,
            text="Feito por Iuri Costa - iuri.j.t@outlook.com",
            bg="black",
            fg="white",
            font=("Arial", 10)
        )
        footer_label.pack(pady=5)


# Arquivo para executar a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaConfeitariaGUI(root)
    root.mainloop()