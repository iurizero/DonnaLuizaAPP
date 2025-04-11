import os
import json
from datetime import datetime

class SistemaConfeitaria:
    def __init__(self):
        self.receitas = []
        self.arquivo_receitas = "receitas.json"
        self.carregar_receitas()

    def carregar_receitas(self):
        """Carrega as receitas do arquivo JSON se existir."""
        if os.path.exists(self.arquivo_receitas):
            try:
                with open(self.arquivo_receitas, 'r', encoding='utf-8') as arquivo:
                    self.receitas = json.load(arquivo)
                return True
            except Exception as e:
                print(f"Erro ao carregar receitas: {e}")
                self.receitas = []
                return False
        return True

    def salvar_receitas(self):
        """Salva as receitas em um arquivo JSON."""
        try:
            with open(self.arquivo_receitas, 'w', encoding='utf-8') as arquivo:
                json.dump(self.receitas, arquivo, ensure_ascii=False, indent=4)
            return True, "Receitas salvas com sucesso!"
        except Exception as e:
            return False, f"Erro ao salvar receitas: {e}"

    def obter_todas_receitas(self):
        """Retorna todas as receitas."""
        return self.receitas

    def obter_receita_por_id(self, id_receita):
        """Busca uma receita específica pelo ID."""
        for receita in self.receitas:
            if receita['id'] == id_receita:
                return receita
        return None

    def registrar_receita(self, nome, tipo, materiais_base, materiais_decoracao, embalagem, precisa_caixa, observacoes=""):
        """Registra uma nova receita."""
        # Validações básicas
        if not nome:
            return False, "O nome da receita é obrigatório."
        
        if not materiais_base:
            return False, "Informe pelo menos um material base."
        
        # Gerar ID para a nova receita
        novo_id = 1
        if self.receitas:
            # Encontrar o maior ID existente e adicionar 1
            novo_id = max(receita["id"] for receita in self.receitas) + 1
        
        # Criar dicionário da nova receita
        nova_receita = {
            "id": novo_id,
            "nome": nome,
            "tipo": tipo,
            "materiais_base": materiais_base,
            "materiais_decoracao": materiais_decoracao,
            "embalagem": embalagem,
            "precisa_caixa_transporte": precisa_caixa,
            "observacoes": observacoes,
            "data_registro": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        
        # Adicionar à lista
        self.receitas.append(nova_receita)
        
        # Salvar no arquivo
        sucesso, mensagem = self.salvar_receitas()
        if sucesso:
            return True, f"Receita '{nome}' registrada com sucesso!"
        else:
            # Remover a receita da lista em caso de erro ao salvar
            self.receitas.pop()
            return False, mensagem