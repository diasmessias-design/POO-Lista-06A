import json


class Cliente:
    def __init__(self, id, nome, email, fone):
        self.set_id(id)
        self.set_nome(nome)
        self.set_email(email)
        self.set_fone(fone)

    def set_id(self, id):
        self.__id = id

    def set_nome(self, nome):
        if nome.strip() == "":
            raise ValueError("Nome inválido")
        self.__nome = nome

    def set_email(self, email):
        self.__email = email

    def set_fone(self, fone):
        self.__fone = fone

    def get_id(self):
        return self.__id

    def get_nome(self):
        return self.__nome

    def get_email(self):
        return self.__email

    def get_fone(self):
        return self.__fone

    def __str__(self):
        return f"{self.__id} - {self.__nome} - {self.__email} - {self.__fone}"


class ClienteDAO:
    objetos = []

    @staticmethod
    def Inserir(obj):
        if ClienteDAO.Listar_Id(obj.get_id()) is not None:
            return False

        ClienteDAO.objetos.append(obj)
        return True

    @staticmethod
    def Listar():
        return ClienteDAO.objetos

    @staticmethod
    def Listar_Id(id):
        for obj in ClienteDAO.objetos:
            if obj.get_id() == id:
                return obj
        return None

    @staticmethod
    def Atualizar(obj):
        for i, cliente in enumerate(ClienteDAO.objetos):
            if cliente.get_id() == obj.get_id():
                ClienteDAO.objetos[i] = obj
                return True
        return False

    @staticmethod
    def Excluir(id):
        for obj in ClienteDAO.objetos:
            if obj.get_id() == id:
                ClienteDAO.objetos.remove(obj)
                return True
        return False

    @staticmethod
    def Salvar():
        dados = []

        for obj in ClienteDAO.objetos:
            dados.append({
                "id": obj.get_id(),
                "nome": obj.get_nome(),
                "email": obj.get_email(),
                "fone": obj.get_fone()
            })

        with open("clientes.json", "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

    @staticmethod
    def Abrir():
        try:
            with open("clientes.json", "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            ClienteDAO.objetos = []

            for dado in dados:
                cliente = Cliente(
                    dado["id"],
                    dado["nome"],
                    dado["email"],
                    dado["fone"]
                )
                ClienteDAO.objetos.append(cliente)

        except FileNotFoundError:
            ClienteDAO.objetos = []


class UI:
    @staticmethod
    def menu():
        print("1 - Inserir Cliente")
        print("2 - Listar clientes")
        print("3 - Buscar cliente por ID")
        print("4 - Atualizar cliente")
        print("5 - Excluir cliente")
        print("6 - Sair")

        return int(input("Escolha uma opção: "))

    @staticmethod
    def inserir():
        id = int(input("ID: "))
        nome = input("Nome: ")
        email = input("Email: ")
        fone = input("Telefone: ")

        try:
            cliente = Cliente(id, nome, email, fone)

            if ClienteDAO.Inserir(cliente):
                ClienteDAO.Salvar()
                print("Cliente cadastrado com sucesso!")
            else:
                print("Já existe um cliente com esse ID!")

        except ValueError as erro:
            print(erro)

    @staticmethod
    def listar():
        clientes = ClienteDAO.Listar()

        if len(clientes) == 0:
            print("Nenhum cliente cadastrado!")
            return

        for cliente in clientes:
            print(cliente)

    @staticmethod
    def buscar():
        id = int(input("ID do cliente: "))
        cliente = ClienteDAO.Listar_Id(id)

        if cliente is not None:
            print(cliente)
        else:
            print("Cliente não encontrado!")

    @staticmethod
    def atualizar():
        id = int(input("ID do cliente: "))
        cliente = ClienteDAO.Listar_Id(id)

        if cliente is None:
            print("Cliente não encontrado!")
            return

        nome = input("Novo nome: ")
        email = input("Novo email: ")
        fone = input("Novo telefone: ")

        try:
            novo = Cliente(id, nome, email, fone)

            if ClienteDAO.Atualizar(novo):
                ClienteDAO.Salvar()
                print("Cliente atualizado")

        except ValueError as erro:
            print(erro)

    @staticmethod
    def excluir():
        id = int(input("ID do cliente: "))

        if ClienteDAO.Excluir(id):
            ClienteDAO.Salvar()
            print("Cliente excluído")
        else:
            print("Cliente não encontrado")

    @staticmethod
    def main():
        ClienteDAO.Abrir()

        while True:
            op = UI.menu()

            if op == 1:
                UI.inserir()

            elif op == 2:
                UI.listar()

            elif op == 3:
                UI.buscar()

            elif op == 4:
                UI.atualizar()

            elif op == 5:
                UI.excluir()

            elif op == 6:
                print("Encerrando o programa...")
                break

            else:
                print("Opção inválida")


UI.main()
