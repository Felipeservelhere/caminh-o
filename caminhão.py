import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime, timedelta

class TruckManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Lançamento de Documentos de Caminhões")

        # Criar um notebook para as abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        # Criar as abas
        self.tab_register = ttk.Frame(self.notebook)
        self.tab_record = ttk.Frame(self.notebook)
        self.tab_view = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_register, text="Registrar Caminhões e Motoristas")
        self.notebook.add(self.tab_record, text="Registrar Carga e Descarga")
        self.notebook.add(self.tab_view, text="Visualizar Lançamentos")

        # Inicializar dados
        self.trucks = []
        self.drivers = []
        self.loads = []  # Lista para armazenar os lançamentos
        self.load_data()

        # Criar widgets para a aba de registro
        self.create_register_widgets()

        # Criar widgets para a aba de registro de carga
        self.create_record_widgets()

        # Criar widgets para a aba de visualização
        self.create_view_widgets()

        # Criar estilo para as caixas
        self.style = ttk.Style()
        self.style.configure("White.TFrame", background="white")
        self.style.configure("White.TLabel", background="white", foreground="black")  # Fundo branco e texto preto

    def create_register_widgets(self):
        # Registro de Caminhões
        ttk.Label(self.tab_register, text="Registrar Caminhão").grid(row=0, column=0, padx=10, pady=10)
        self.truck_entry = ttk.Entry(self.tab_register)
        self.truck_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Button(self.tab_register, text="Adicionar Caminhão", command=self.add_truck).grid(row=0, column=2, padx=10, pady=10)

        # Registro de Motoristas
        ttk.Label(self.tab_register, text="Registrar Motorista").grid(row=1, column=0, padx=10, pady=10)
        self.driver_entry = ttk.Entry(self.tab_register)
        self.driver_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(self.tab_register, text="Adicionar Motorista", command=self.add_driver).grid(row=1, column=2, padx=10, pady=10)

    def create_record_widgets(self):
        # Seleção de Caminhão
        ttk.Label(self.tab_record, text="Selecionar Caminhão").grid(row=0, column=0, padx=10, pady=10)
        self.truck_combobox = ttk.Combobox(self.tab_record, values=self.trucks)
        self.truck_combobox.grid(row=0, column=1, padx=10, pady=10)

        # Seleção de Motorista
        ttk.Label(self.tab_record, text="Selecionar Motorista").grid(row=1, column=0, padx=10, pady=10)
        self.driver_combobox = ttk.Combobox(self.tab_record, values=self.drivers)
        self.driver_combobox.grid(row=1, column=1, padx=10, pady=10)

        # Data da Carga
        ttk.Label(self.tab_record, text="Data da Carga (DD/MM/AAAA)").grid(row=2, column=0, padx=10, pady=10)
        self.load_date_entry = ttk.Entry(self.tab_record)
        self.load_date_entry.grid(row=2, column=1, padx=10, pady=10)
        self.load_date_entry.bind("<KeyRelease>", self.format_date)

        # Data da Descarga
        ttk.Label(self.tab_record, text="Data da Descarga (DD/MM/AAAA)").grid(row=3, column=0, padx=10, pady=10)
        self.unload_date_entry = ttk.Entry(self.tab_record)
        self.unload_date_entry.grid(row=3, column=1, padx=10, pady=10)
        self.unload_date_entry.bind("<KeyRelease>", self.format_date)

        # Local da Carga
        ttk.Label(self.tab_record, text="Local da Carga").grid(row=4, column=0, padx=10, pady=10)
        self.load_location_entry = ttk.Entry(self.tab_record)
        self.load_location_entry.grid(row=4, column=1, padx=10, pady=10)

        # Local da Descarga
        ttk.Label(self.tab_record, text="Local da Descarga").grid(row=5, column=0, padx=10, pady=10)
        self.unload_location_entry = ttk.Entry(self.tab_record)
        self.unload_location_entry.grid(row=5, column=1, padx=10, pady=10)

        # KM da Carga
        ttk.Label(self.tab_record, text="KM da Carga").grid(row=6, column=0, padx=10, pady=10)
        self.load_km_entry = ttk.Entry(self.tab_record)
        self.load_km_entry.grid(row=6, column=1, padx=10, pady=10)

        # KM da Descarga
        ttk.Label(self.tab_record, text="KM da Descarga").grid(row=7, column=0, padx=10, pady=10)
        self.unload_km_entry = ttk.Entry(self.tab_record)
        self.unload_km_entry.grid(row=7, column=1, padx=10, pady=10)

        # Despesa
        ttk.Label(self.tab_record, text="Despesa").grid(row=8, column=0, padx=10, pady=10)
        self.expense_entry = ttk.Entry(self.tab_record)
        self.expense_entry.grid(row=8, column=1, padx=10, pady=10)

        # Botão para lançar valores
        ttk.Button(self.tab_record, text="Lançar Valores", command=self.launch_expense_values).grid(row=8, column=2, padx=10, pady=10)

        # Receita
        ttk.Label(self.tab_record, text="Receita").grid(row=9, column=0, padx=10, pady=10)
        self.revenue_entry = ttk.Entry(self.tab_record)
        self.revenue_entry.grid(row=9, column=1, padx=10, pady=10)
        self.revenue_entry.bind("<KeyRelease>", self.update_profit)

        # Botão para registrar carga
        ttk.Button(self.tab_record, text="Registrar Carga", command=self.record_load).grid(row=10, column=0, columnspan=2, padx=10, pady=10)

        # Label para mostrar o lucro
        self.profit_label = ttk.Label(self.tab_record, text="Lucro: R$ 0.00")
        self.profit_label.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

    def create_view_widgets(self):
        # Frame para os lançamentos
        self.launches_frame = ttk.Frame(self.tab_view)
        self.launches_frame.pack(fill='both', expand=True)

        # Combobox para filtrar lançamentos
        self.filter_combobox = ttk.Combobox(self.tab_view, values=["Hoje", "Ontem", "Essa Semana", "Esse Mês", "Esse Semestre", "Esse Ano", "Todos os Registros", "Personalizado"])
        self.filter_combobox.current(0)  # Set default to "Hoje"
        self.filter_combobox.pack(pady=10, padx=10, anchor='nw')
        self.filter_combobox.bind("<<ComboboxSelected>>", self.toggle_custom_date_inputs)

        # Entradas para datas personalizadas
        self.start_date_entry = ttk.Entry(self.tab_view, state='disabled')
        self.start_date_entry.pack(pady=5, padx=10, anchor='nw')
        self.start_date_entry.insert(0, "Data Inicial (DD/MM/AAAA)")

        self.end_date_entry = ttk.Entry(self.tab_view, state='disabled')
        self.end_date_entry.pack(pady=5, padx=10, anchor='nw')
        self.end_date_entry.insert(0, "Data Final (DD/MM/AAAA)")

        # Botão de pesquisa (lupa)
        search_button = ttk.Button(self.tab_view, text="🔍", command=self.update_launch_summary)
        search_button.pack(pady=10, padx=10, anchor='nw')

        # Frame para resumo de lançamentos por caminhão (lado esquerdo)
        self.summary_frame = ttk.Frame(self.launches_frame)
        self.summary_frame.pack(side=tk.LEFT, fill='y', padx=10, pady=10)

        # Frame para detalhes dos lançamentos (lado direito)
        self.details_frame = ttk.Frame(self.launches_frame)
        self.details_frame.pack(side=tk.RIGHT, fill='both', expand=True, padx=10, pady=10)

        # Atualiza o resumo de lançamentos
        self.update_launch_summary()

    def toggle_custom_date_inputs(self, event):
        """Habilita ou desabilita as entradas de data personalizada com base na seleção do filtro."""
        if self.filter_combobox.get() == "Personalizado":
            self.start_date_entry.config(state='normal')
            self.end_date_entry.config(state='normal')
        else:
            self.start_date_entry.config(state='disabled')
            self.end_date_entry.config(state='disabled')

    def launch_expense_values(self):
        """Abre uma nova janela para lançar múltiplos valores de despesa."""
        self.expense_window = tk.Toplevel(self.root)
        self.expense_window.title("Lançar Valores de Despesa")

        self.expense_entries = []
        for i in range(20):
            entry = ttk.Entry(self.expense_window)
            entry.grid(row=i, column=0, padx=10, pady=5)
            self.expense_entries.append(entry)

        ttk.Button(self.expense_window, text="Confirmar", command=self.confirm_expenses).grid(row=21, column=0, padx=10, pady=10)

    def confirm_expenses(self):
        """Confirma os valores de despesa e calcula a soma."""
        total_expense = 0
        for entry in self.expense_entries:
            try:
                value = float(entry.get().strip())
                total_expense += value
            except ValueError:
                continue  # Ignora entradas não numéricas

        self.expense_entry.delete(0, tk.END)
        self.expense_entry.insert(0, f"{total_expense:.2f}")
        self.expense_window.destroy()

    def add_truck(self):
        truck_name = self.truck_entry.get().strip()
        if truck_name:
            self.trucks.append(truck_name)
            self.truck_combobox['values'] = self.trucks  # Atualiza a combobox
            self.truck_entry.delete(0, tk.END)  # Limpa o campo de entrada
            self.save_data()
            messagebox.showinfo("Sucesso", "Caminhão adicionado com sucesso!")
        else:
            messagebox.showwarning("Erro", "Por favor, insira um nome de caminhão.")

    def add_driver(self):
        driver_name = self.driver_entry.get().strip()
        if driver_name:
            self.drivers.append(driver_name)
            self.driver_combobox['values'] = self.drivers  # Atualiza a combobox
            self.driver_entry.delete(0, tk.END)  # Limpa o campo de entrada
            self.save_data()
            messagebox.showinfo("Sucesso", "Motorista adicionado com sucesso!")
        else:
            messagebox.showwarning("Erro", "Por favor, insira um nome de motorista.")

    def record_load(self):
        truck = self.truck_combobox.get()
        driver = self.driver_combobox.get()
        load_date = self.load_date_entry.get().strip()
        unload_date = self.unload_date_entry.get().strip()
        load_location = self.load_location_entry.get().strip()
        unload_location = self.unload_location_entry.get().strip()
        load_km = self.load_km_entry.get().strip()
        unload_km = self.unload_km_entry.get().strip()
        expense = self.expense_entry.get().strip()
        revenue = self.revenue_entry.get().strip()

        if not all([truck, driver, load_date, unload_date, load_location, unload_location, load_km, unload_km, expense, revenue]):
            messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")
            return

        try:
            expense = float(expense)
            revenue = float(revenue)
            profit = revenue - expense
            self.profit_label.config(text=f"Lucro: R$ {profit:.2f}")

            # Adiciona o lançamento à lista
            self.loads.append({
                'truck': truck,
                'driver': driver,
                'load_date': load_date,
                'unload_date': unload_date,
                'load_location': load_location,
                'unload_location': unload_location,
                'load_km': load_km,
                'unload_km': unload_km,
                'expense': expense,
                'revenue': revenue,
                'profit': profit
            })

            # Ordena os lançamentos com base na data de descarga (do mais recente para o mais antigo)
            self.loads.sort(key=lambda x: datetime.strptime(x['unload_date'], "%d/%m/%Y"), reverse=True)

            # Atualiza o resumo de lançamentos
            self.update_launch_summary()

            # Salva os dados
            self.save_data()

        except ValueError:
            messagebox.showwarning("Erro", "Despesa e Receita devem ser números válidos.")
            return

        messagebox.showinfo("Sucesso", "Carga registrada com sucesso!")

    def update_profit(self, event):
        """Atualiza o lucro em tempo real ao digitar despesa e receita."""
        try:
            expense = float(self.expense_entry.get().strip() or 0)
            revenue = float(self.revenue_entry.get().strip() or 0)
            profit = revenue - expense
            self.profit_label.config(text=f"Lucro: R$ {profit:.2f}")
        except ValueError:
            self.profit_label.config(text="Lucro: R$ 0.00")

    def update_launch_summary(self, event=None):
        """Atualiza o resumo dos lançamentos por caminhão no layout especificado."""
        for widget in self.summary_frame.winfo_children():
            widget.destroy()  # Limpa o frame existente

        # Obter o filtro selecionado
        filter_value = self.filter_combobox.get()
        filtered_loads = self.filter_loads(filter_value)

        # Contar lançamentos por caminhão
        launch_count = {truck: 0 for truck in self.trucks}

        for load in filtered_loads:
            if load['truck'] in launch_count:
                launch_count[load['truck']] += 1

        # Adicionar boxes para cada caminhão
        for truck, count in launch_count.items():
            box = ttk.Frame(self.summary_frame, padding=10, style="White.TFrame")
            box.pack(side=tk.TOP, fill='x', padx=10, pady=5, anchor='w')

            title = ttk.Label(box, text=truck, font=("Arial", 12, "bold"), style="White.TLabel")
            title.pack(anchor='w')

            count_label = ttk.Label(box, text=f"Quantidade de lançamentos: {count}", font=("Arial", 10), style="White.TLabel")
            count_label.pack(anchor='w')

            # Configurando a borda da caixa
            box.config(relief="solid", borderwidth=1)

            # Vincular o evento de clique à caixa
            box.bind("<Button-1>", lambda event, t=truck: self.show_launch_details(t, box, filtered_loads))

    def filter_loads(self, filter_value):
        """Filtra os lançamentos com base no valor do filtro selecionado."""
        today = datetime.now()
        filtered_loads = []

        for load in self.loads:
            unload_date = datetime.strptime(load['unload_date'], "%d/%m/%Y")

            if filter_value == "Hoje" and unload_date.date() == today.date():
                filtered_loads.append(load)
            elif filter_value == "Ontem" and unload_date.date() == (today - timedelta(days=1)).date():
                filtered_loads.append(load)
            elif filter_value == "Essa Semana" and unload_date >= today - timedelta(days=today.weekday()):
                filtered_loads.append(load)
            elif filter_value == "Esse Mês" and unload_date.month == today.month and unload_date.year == today.year:
                filtered_loads.append(load)
            elif filter_value == "Esse Semestre" and (unload_date.month <= 6 and today.month <= 6 or unload_date.month > 6 and today.month > 6) and unload_date.year == today.year:
                filtered_loads.append(load)
            elif filter_value == "Esse Ano" and unload_date.year == today.year:
                filtered_loads.append(load)
            elif filter_value == "Todos os Registros":
                filtered_loads.append(load)
            elif filter_value == "Personalizado":
                # Obter as datas de início e fim
                start_date_str = self.start_date_entry.get().strip()
                end_date_str = self.end_date_entry.get().strip()
                try:
                    start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
                    end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
                    if start_date <= unload_date <= end_date:
                        filtered_loads.append(load)
                except ValueError:
                    messagebox.showwarning("Erro", "Formato de data inválido. Use DD/MM/AAAA.")
                    return []

        return filtered_loads

    def show_launch_details(self, truck, box, filtered_loads):
        """Mostra os detalhes dos lançamentos ao clicar em um veículo, organizando em colunas."""
        # Filtra os lançamentos para o caminhão selecionado
        truck_loads = [load for load in filtered_loads if load['truck'] == truck]

        if not truck_loads:
            messagebox.showinfo("Sem Lançamentos", f"Nenhum lançamento encontrado para o caminhão: {truck}.")
            return

        box.config(relief="sunken")
        self.root.after(200, lambda: box.config(relief="solid"))

        for widget in self.details_frame.winfo_children():
            widget.destroy()

        self.details_frame.config(style="White.TFrame")

        truck_label = ttk.Label(self.details_frame, text=truck, font=("Arial", 14, "bold"), style="White.TLabel")
        truck_label.pack(anchor='ne', padx=10, pady=10)

        # Criando Canvas + Scrollbar
        canvas = tk.Canvas(self.details_frame)
        scrollbar = ttk.Scrollbar(self.details_frame, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas, padding=10, style="White.TFrame")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        entry_widgets = {}  # Dicionário para armazenar widgets

        columns = 5  # Número de colunas desejado
        row_frames = []
        for i in range(0, len(truck_loads), columns):
            row_frame = ttk.Frame(scroll_frame)
            row_frame.pack(fill='x', padx=10, pady=5)
            row_frames.append(row_frame)

        for index, load in enumerate(truck_loads):
            col = index % columns
            row = index // columns

            detail_frame = ttk.Frame(row_frames[row], padding=10, style="White.TFrame")
            detail_frame.grid(row=0, column=col, padx=10, pady=5, sticky="nsew")
            detail_frame.config(relief="solid", borderwidth=1)

            # Criando entradas editáveis
            driver_entry = ttk.Entry(detail_frame, font=("Arial", 12))
            driver_entry.insert(0, load['driver'])

            load_date_entry = ttk.Entry(detail_frame, font=("Arial", 12))
            load_date_entry.insert(0, load['load_date'])

            unload_date_entry = ttk.Entry(detail_frame, font=("Arial", 12))
            unload_date_entry.insert(0, load['unload_date'])

            load_location_entry = ttk.Entry(detail_frame, font=("Arial", 12))
            load_location_entry.insert(0, load.get('load_location', ''))  # Use get to avoid KeyError

            unload_location_entry = ttk.Entry(detail_frame, font=("Arial", 12))
            unload_location_entry.insert(0, load.get('unload_location', ''))  # Use get to avoid KeyError

            load_km_entry = ttk.Entry(detail_frame, font=("Arial", 12))
            load_km_entry.insert(0, load.get('load_km', ''))  # Use get to avoid KeyError

            unload_km_entry = ttk.Entry(detail_frame, font=("Arial", 12))
            unload_km_entry.insert(0, load.get('unload_km', ''))  # Use get to avoid KeyError

            expense_entry = ttk.Entry(detail_frame, font=("Arial", 12))
            expense_entry.insert(0, f"{load['expense']:.2f}")

            revenue_entry = ttk.Entry(detail_frame, font=("Arial", 12))
            revenue_entry.insert(0, f"{load['revenue']:.2f}")

            profit_entry = ttk.Entry(detail_frame, font=("Arial", 12), state="readonly")
            profit_entry.insert(0, f"{load['profit']:.2f}")

            # Armazenar referências no dicionário
            entry_widgets[load['truck']] = (driver_entry, load_date_entry, unload_date_entry, load_location_entry, unload_location_entry, load_km_entry, unload_km_entry, expense_entry, revenue_entry, profit_entry)

            # Empacotando os campos
            ttk.Label(detail_frame, text="Motorista:", font=("Arial", 10, "bold"), style="White.TLabel").pack(anchor='w')
            driver_entry.pack(fill='x')

            ttk.Label(detail_frame, text="Data da Carga:", font=("Arial", 10, "bold"), style="White.TLabel").pack(anchor='w')
            load_date_entry.pack(fill='x')

            ttk.Label(detail_frame, text="Data da Descarga:", font=("Arial", 10, "bold"), style="White.TLabel").pack(anchor='w')
            unload_date_entry.pack(fill='x')

            ttk.Label(detail_frame, text="Local da Carga:", font=("Arial", 10, "bold"), style="White.TLabel").pack(anchor='w')
            load_location_entry.pack(fill='x')

            ttk.Label(detail_frame, text="Local da Descarga:", font=("Arial", 10, "bold"), style="White.TLabel").pack(anchor='w')
            unload_location_entry.pack(fill='x')

            ttk.Label(detail_frame, text="KM da Carga:", font=("Arial", 10, "bold"), style="White.TLabel").pack(anchor='w')
            load_km_entry.pack(fill='x')

            ttk.Label(detail_frame, text="KM da Descarga:", font=("Arial", 10, "bold"), style="White.TLabel").pack(anchor='w')
            unload_km_entry.pack(fill='x')

            ttk.Label(detail_frame, text="Despesa (R$):", font=("Arial", 10, "bold"), style="White.TLabel").pack(anchor='w')
            expense_entry.pack(fill='x')

            ttk.Label(detail_frame, text="Receita (R$):", font=("Arial", 10, "bold"), style="White.TLabel").pack(anchor='w')
            revenue_entry.pack(fill='x')

            ttk.Label(detail_frame, text="Lucro (R$):", font=("Arial", 10, "bold"), style="White.TLabel").pack(anchor='w')
            profit_entry.pack(fill='x')

            # Criando frame para botões
            button_frame = ttk.Frame(detail_frame)
            button_frame.pack(anchor='e', pady=5)

            save_button = ttk.Button(button_frame, text="Salvar", command=lambda l=load, e=entry_widgets[load['truck']]: self.save_changes(l, e))
            save_button.pack(side="left", padx=5)

            delete_button = ttk.Button(button_frame, text="Excluir", command=lambda l=load: self.delete_load(l))
            delete_button.pack(side="left", padx=5)

        total_profit = sum(load['profit'] for load in truck_loads)

        total_profit_label = ttk.Label(scroll_frame, text=f"Total de Lucro: R$ {total_profit:.2f}", font=("Arial", 12, "bold"), style="White.TLabel")
        total_profit_label.pack(side=tk.BOTTOM, pady=10)

    def save_changes(self, load, entries):
        """Salva as alterações feitas nos lançamentos."""
        driver_entry, load_date_entry, unload_date_entry, load_location_entry, unload_location_entry, load_km_entry, unload_km_entry, expense_entry, revenue_entry, profit_entry = entries

        load['driver'] = driver_entry.get()
        load['load_date'] = load_date_entry.get()
        load['unload_date'] = unload_date_entry.get()
        load['load_location'] = load_location_entry.get()
        load['unload_location'] = unload_location_entry.get()
        load['load_km'] = load_km_entry.get()
        load['unload_km'] = unload_km_entry.get()
        load['expense'] = float(expense_entry.get().replace(",", "."))
        load['revenue'] = float(revenue_entry.get().replace(",", "."))
        load['profit'] = load['revenue'] - load['expense']

        profit_entry.config(state="normal")
        profit_entry.delete(0, tk.END)
        profit_entry.insert(0, f"{load['profit']:.2f}")
        profit_entry.config(state="readonly")

        self.save_data()
        messagebox.showinfo("Sucesso", "Lançamento atualizado com sucesso!")

    def delete_load(self, load):
        """Exclui um lançamento da lista."""
        self.loads.remove(load)
        self.save_data()
        self.update_launch_summary()
        messagebox.showinfo("Sucesso", "Lançamento excluído com sucesso!")

    def format_date(self, event):
        """Formata a data automaticamente ao digitar."""
        date_entry = event.widget
        date_str = date_entry.get().replace("/", "")
        if len(date_str) >= 2:
            date_str = date_str[:2] + "/" + date_str[2:]
        if len(date_str) >= 5:
            date_str = date_str[:5] + "/" + date_str[5:]
        date_entry.delete(0, tk.END)
        date_entry.insert(0, date_str)

    def load_data(self):
        """Carrega dados de caminhões e motoristas de um arquivo JSON."""
        if os.path.exists('data.json'):
            with open('data.json', 'r') as file:
                data = json.load(file)
                self.trucks = data.get('trucks', [])
                self.drivers = data.get('drivers', [])
                self.loads = data.get('loads', [])  # Carrega os lançamentos

                # Ordena os lançamentos com base na data de descarga (do mais recente para o mais antigo)
                self.loads.sort(key=lambda x: datetime.strptime(x['unload_date'], "%d/%m/%Y"), reverse=True)

    def save_data(self):
        """Salva dados de caminhões, motoristas e lançamentos em um arquivo JSON."""
        data = {
            'trucks': self.trucks,
            'drivers': self.drivers,
            'loads': self.loads  # Salva os lançamentos
        }
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = TruckManagementApp(root)
    root.mainloop()