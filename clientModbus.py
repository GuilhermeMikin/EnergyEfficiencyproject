from pyModbusTCP.client import ModbusClient
from time import sleep
import time
import datetime
import sqlite3
from threading import Lock


class ClienteMODBUS():
    """
    Classe Cliente MODBUS
    """

    def __init__(self, server_ip, porta, device_id=1, scan_time=2, valor=0, dbpath="C:\database.db"):
        """
        Construtor
        """
        self._scan_time = scan_time
        self._server_ip = server_ip
        self._device_id = device_id
        self._port = porta
        self._cliente = ModbusClient(host=server_ip, port=porta, unit_id=device_id)
        
        self._dbpath = dbpath
        self._valor = valor
        self._con = sqlite3.connect(self._dbpath)
        self._cursor = self._con.cursor()
    

        self.motores = list()
        try:
            self.arq = open('motores.txt', 'rt')
            self.arq.close()
        except:
            self.arq = open('motores.txt', 'wt+')

    def atendimento(self):
        """
        Método para atendimento do usuário
        """
        try:
            self._cliente.open()
            print('\n\033[33m --> Cliente Modbus conectado..\033[m\n')

        except Exception as e:
            print('\033[31mERRO: ', e.args, '\033[m')
        try:
            atendimento = True
            while atendimento:
                print('-' * 34*3)
                print('\033[34mSistema de Monitoramento\033[m'.center(34*3))
                print('-' * 34*3)
                sel = input("Qual serviço deseja realizar? \n1- Leitura Modbus \n2- Escrita Modbus \n3- Configuração de leitura \n4- Cadastrar Motor \n5- Leitura Motor \n6- Sair \nN° Serviço: ")
                if sel == '1':
                    self.createTable()
                    self.createTableenergy()
                    self.createTableModbus()
                    print('\nQual tipo de dado deseja ler?')
                    print("1- Coil Status \n2- Input Status \n3- Holding Register \n4- Input Register \n5- Voltar")
                    while True:
                        tipo = int(input("Type: "))
                        if tipo > 5:
                            print('\033[31mDigite um tipo válido..\033[m')
                            sleep(0.8)
                        else:
                            break

                    if tipo == 3 or tipo == 4: 
                        while True:
                            val = int(input("\n1- Decimal \n2- Floating Point \n3- Float Swapped \nLeitura: "))
                            if val > 3:
                                print('\033[31mDigite um tipo válido..\033[m')
                                sleep(0.8)
                            else:
                                break

                        if val == 1: #valores INTEGER 
                            addr = input(f'\nAddress: ')
                            leng = int(input(f'Length: '))
                            nvezes = input('Quantidade de leituras: ')
                            print('\nComeçando leitura Decimal..\n')
                            sleep(1)
                            try:
                                for i in range(0, int(nvezes)):
                                    print(f'\033[33mLeitura {i + 1}:\033[m')
                                    stamp = (i+1)
                                    self.lerDado(int(stamp), int(tipo), int(addr), leng)
                                    sleep(self._scan_time)
                                print('\nValores lidos e inseridos no DB com sucesso!!\n')
                                sleep(0.8)
                            except Exception as e:
                                print('\033[31mERRO: ', e.args, '\033[m')
                                try:
                                    sleep(0.5)
                                    print('\nSegunda tentativa..')
                                    if not self._cliente.is_open():
                                        print('\nReiniciando cliente Modbus..\n')
                                        self._cliente.open()
                                    sleep(2)
                                    for i in range(0, int(nvezes)):
                                        print(f'\033[33mLeitura {i + 1}:\033[m')
                                        stamp = (i+1)
                                        self.lerDado(int(stamp), int(tipo), int(addr), leng)
                                        sleep(self._scan_time)
                                    print('\nValores lidos e inseridos no DB com sucesso!!\n')
                                    sleep(0.8)
                                except Exception as e:
                                    print('\033[31mERRO: ', e.args, '\033[m')
                                    print('\nInfelizmente o Cliente não conseguiu receber uma resposta..\nÉ sugerido reiniciar todo o sistema. \nCaso isso não resolva, entre em contato com a assistência técnica. \nVoltando ao menu..\n\n')
                                    sleep(2.5)

                        elif val == 2: #valores FLOAT
                            addr = input(f'\nAddress: ')
                            leng = int(input(f'Length: '))
                            nvezes = input('Quantidade de leituras: ')
                            print('\nComeçando leitura FLOAT..\n')
                            sleep(1)
                            try:
                                for i in range(0, int(nvezes)):
                                    print(f'\033[33mLeitura {i + 1}:\033[m')
                                    stamp = (i+1)
                                    self.lerDadoFloat(int(stamp), int(tipo), int(addr), leng)
                                    sleep(self._scan_time)
                                print('\nValores lidos e inseridos no DB com sucesso!!\n')
                                sleep(0.8)
                            except Exception as e:
                                print('\033[31mERRO: ', e.args, '\033[m')
                                try:
                                    sleep(0.5)
                                    print('\nSegunda tentativa..')
                                    if not self._cliente.is_open():
                                        print('\nReiniciando cliente Modbus..\n')
                                        self._cliente.open()
                                    sleep(2)
                                    for i in range(0, int(nvezes)):
                                        print(f'\033[33mLeitura {i + 1}:\033[m')
                                        stamp = (i+1)
                                        self.lerDadoFloat(int(stamp), int(tipo), int(addr), leng)
                                        sleep(self._scan_time)
                                    print('\nValores lidos e inseridos no DB com sucesso!!\n')
                                    sleep(0.8)
                                except Exception as e:
                                    print('\033[31mERRO: ', e.args, '\033[m')
                                    print('\nInfelizmente o Cliente não conseguiu receber uma resposta..\nÉ sugerido reiniciar todo o sistema. \nCaso isso não resolva, entre em contato com a assistência técnica. \nVoltando ao menu..\n\n')
                                    sleep(2.5)

                        elif val == 3: #valores FLOAT SWAPPED 
                            addr = input(f'\nAddress: ')
                            leng = int(input(f'Length: '))
                            nvezes = input('Quantidade de leituras: ')
                            print('\nComeçando leitura FLOAT SWAPPED..\n')
                            sleep(1)
                            try:
                                for i in range(0, int(nvezes)):
                                    print(f'\033[33mLeitura {i + 1}:\033[m')
                                    stamp = (i+1)
                                    self.lerDadoFloatSwapped(int(stamp), int(tipo), int(addr), leng)
                                    sleep(self._scan_time)
                                print('\nValores lidos e inseridos no DB com sucesso!!\n')
                                sleep(0.8)
                            except Exception as e:
                                print('\033[31mERRO: ', e.args, '\033[m')
                                try:
                                    sleep(0.5)
                                    print('\nSegunda tentativa..')
                                    if not self._cliente.is_open():
                                        print('\nReiniciando cliente Modbus..\n')
                                        self._cliente.open()
                                    sleep(2)
                                    for i in range(0, int(nvezes)):
                                        print(f'\033[33mLeitura {i + 1}:\033[m')
                                        stamp = (i+1)
                                        self.lerDadoFloatSwapped(int(stamp), int(tipo), int(addr), leng)
                                        sleep(self._scan_time)
                                    print('\nValores lidos e inseridos no DB com sucesso!!\n')
                                    sleep(0.8)
                                except Exception as e:
                                    print('\033[31mERRO: ', e.args, '\033[m')
                                    print('\nInfelizmente o Cliente não conseguiu receber uma resposta..\nÉ sugerido reiniciar todo o sistema. \nCaso isso não resolva, entre em contato com a assistência técnica. \nVoltando ao menu..\n\n')
                                    sleep(2.5)

                        else:
                            sleep(0.3)
                            print('\033[31mSeleção inválida..\033[m\n')
                            sleep(0.7)
                    elif tipo ==5:
                        print('\nVoltando ao menu inicial..\n')
                        sleep(0.5)
                    else:
                        addr = input(f'\nAddress: ')
                        leng = int(input(f'Length: '))
                        nvezes = input('Quantidade de leituras: ')
                        print('\nComeçando leitura..\n')
                        sleep(1)
                        try:
                            for i in range(0, int(nvezes)):
                                print(f'\033[33mLeitura {i + 1}:\033[m')
                                stamp = (i+1)
                                self.lerDado(int(stamp), int(tipo), int(addr), leng)
                                sleep(self._scan_time)
                            print('\nValores lidos e inseridos no DB com sucesso!!\n')
                            sleep(0.8)
                        except Exception as e:
                            print('\033[31mERRO: ', e.args, '\033[m')
                            try:
                                sleep(0.5)
                                print('\nSegunda tentativa..')
                                if not self._cliente.is_open():
                                    print('\nReiniciando cliente Modbus..\n')
                                    self._cliente.open()
                                sleep(2)
                                for i in range(0, int(nvezes)):
                                    print(f'\033[33mLeitura {i + 1}:\033[m')
                                    stamp = (i+1)
                                    self.lerDado(int(stamp), int(tipo), int(addr), leng)
                                    sleep(self._scan_time)
                                print('\nValores lidos e inseridos no DB com sucesso!!\n')
                                sleep(0.8)
                            except Exception as e:
                                print('\033[31mERRO: ', e.args, '\033[m')
                                print('\nInfelizmente o Cliente não conseguiu receber uma resposta..\nÉ sugerido reiniciar todo o sistema. \nCaso isso não resolva, entre em contato com a assistência técnica. \nVoltando ao menu..\n\n')
                                sleep(2.5)

                elif sel == '2':
                    sleep(1)
                    print('\nQual tipo de dado deseja escrever? \n1- Coil Status \n2- Holding Register')
                    sleep(0.5)
                    while True:
                        tipo = int(input("Tipo: "))
                        if tipo > 2:
                            print('\033[31mDigite um tipo válido..\033[m')
                            sleep(0.8)
                        else:
                            break
                    addr = input(f'Digite o endereço: ')
                    valor = int(input(f'Digite o valor que deseja escrever: '))
                    print('\nEscrevendo..')
                    sleep(1.5)
                    self.escreveDado(int(tipo), int(addr), valor)

                elif sel == '3':
                    print('')
                    print('-' * 34*3)
                    print('Configurações de Leitura'.center(34*3))
                    print(f'\n\033[32m->\033[m Configuração de leitura atual: - IP Addrs: \033[35m{self._server_ip}\033[m - TCP Port: \033[35m{self._port}\033[m - Device ID: \033[35m{self._device_id}\033[m - Scan_Time: \033[35m{self._scan_time}s\033[m')
                    print('\nQual tipo de configuração deseja fazer? \n1- Endereço IP \n2- Porta TCP \n3- Device ID \n4- ScanTime \n5- Voltar')
                    config = int(input("Configuração: "))
                    if config == 1:
                        ipserv = str(input('Novo endereço IP: '))
                        try:
                            self._cliente.close()
                            self._server_ip = ipserv
                            self._cliente = ModbusClient(host=self._server_ip)
                            self._cliente.open()
                            print(f'\nServer IP alterado para {ipserv} com sucesso!!\n')
                            sleep(1)
                        except Exception as e:
                            print('\033[31mERRO: ', e.args, '\033[m')
                            print('\nNão foi possível alterar o endereço IP.. \nVoltando ao menu..\n\n')
                            sleep(0.5)
                    elif config == 2:
                        porttcp = input('Nova porta TCP: ')
                        try:
                            self._cliente.close()
                            self._port = int(porttcp)
                            self._cliente = ModbusClient(port=self._port)
                            self._cliente.open()
                            print(f'\nTCP port alterado para {porttcp} com sucesso!!\n')
                            sleep(1)
                        except Exception as e:
                            print('\033[31mERRO: ', e.args, '\033[m')
                            print('\nNão foi possível alterar a porta.. \nVoltando ao menu..\n\n')
                            sleep(0.5)
                    elif config == 3:
                        iddevice = input('Novo device ID: ')
                        try:
                            self._cliente.close()
                            self._device_id = int(iddevice)
                            self._cliente = ModbusClient(unit_id=self._device_id)
                            self._cliente.open()
                            print(f'\nDevice ID alterado para {iddevice} com sucesso!!\n')
                            sleep(1)
                        except Exception as e:
                            print('\033[31mERRO: ', e.args, '\033[m')
                            print('\nNão foi possível alterar o ID do device.. \nVoltando ao menu..\n\n')
                            sleep(0.5)
                    elif config == 4:
                        scant = input('Novo tempo de varredura [s]: ')
                        try:    
                            self._scan_time = float(scant)
                            print(f'\nScan_time alterado para {scant}s com sucesso!!\n')
                        except Exception as e:
                            print('\033[31mERRO: ', e.args, '\033[m')
                            print('\nNão foi possível alterar o tempo de varredura.. \nVoltando ao menu..\n\n')
                            sleep(0.5)
                    elif config == 5:
                        print('\nVoltando ao menu inicial..\n')
                        sleep(0.5)
                    else:
                        sleep(0.3)
                        print('\033[31mSeleção inválida..\033[m\n')
                        sleep(0.7)
                
                elif sel == '4':
                    self.createTableMotor()
                    dados_motor = dict()
                    while True:
                        dados_motor.clear()
                        modmotor = str(input('\nModelo do motor: '))
                        dados_motor['modmotor'] = modmotor
                        polmotor = str(input('N° Polos: '))
                        dados_motor['polmotor'] = polmotor
                        pnmotor = float(input('Potência nominal (CV): '))
                        dados_motor['pnmotor'] = pnmotor
                        Vmotor = float(input('Tensão nominal (V): '))
                        dados_motor['Vmotor'] = Vmotor
                        Imotor = float(input('Corrente nominal (A): '))
                        dados_motor['Imotor'] = Imotor
                        rpmmotor = int(input('Rotação Nominal (RPM): '))
                        dados_motor['rpmmotor'] = rpmmotor
                        rendmotor = float(input('Rendimento (%): '))
                        dados_motor['rendmotor'] = rendmotor
                        fpmotor = float(input('Fator de Potência: '))
                        dados_motor['fpmotor'] = fpmotor
                        addrmotor = int(input('Endereço Modbus do motor: '))
                        dados_motor['addrmotor'] = addrmotor
                        #self.motores.append(dados_motor.copy())
                        try:
                            self.inserirDBMotor(modmotor=modmotor, polmotor=polmotor, pnmotor=pnmotor, Vmotor=Vmotor, Imotor=Imotor, rpmmotor=rpmmotor, rendmotor=rendmotor, fpmotor=fpmotor, addrmotor=addrmotor)
                            sleep(0.5)
                        except Exception as e:
                            print('Erro ao cadastrar motor!')
                            print('\033[31mERRO: ', e.args, '\033[m')
                        while True: 
                            resp = str(input('Deseja cadastrar mais um motor? [S/N] ')).upper()[0]
                            if resp in 'SN':
                                break
                            print('\033[31mERRO! Responda apenas S ou N.\033[m')
                        if resp == 'N':
                            break
                    sleep(1)

                elif sel == '5':
                    try:
                        self.createTable()
                        self.createTableenergy()
                        try:
                            self.readArq()
                        except Exception as e:
                            print('\nErro na leitura do arquivo de motores!')
                            print('\033[31mERRO: ', e.args, '\033[m')
                        else:
                            if len(self.motores) >= 1:
                                print('\nLista de motores cadastrados: ')
                                idmotor = 1
                                for mot in self.motores:
                                    print(f'  \033[32mMotor {idmotor}:\033[m Modelo {mot["modmotor"]}')
                                    idmotor = idmotor + 1
                                while True:
                                    readm = int(input('\nQual motor deseja ler: '))
                                    if readm <= len(self.motores):
                                        break
                                    print('\033[31mERRO! Digite um ID de motor válido.\033[m')
                                nvezes = input('Quantidade de leituras: ')
                                print(f'\nComeçando leitura motor {readm}..\n')
                                self.createTableReadMotor(readm)
                                sleep(1)
                                try:
                                    for i in range(0, int(nvezes)):
                                        print(f'\033[33mLeitura {i + 1}:\033[m')
                                        stamp = (i+1)
                                        self.lerMotor(int(stamp), int(readm), self.motores)
                                        sleep(self._scan_time)
                                        # newlaststamp = int(mot["laststamp"])+i
                                        # self.editlinhaArq(readm-1,mot["modmotor"],mot["polmotor"],mot["pnmotor"],mot["pnmotorkw"],mot["Vmotor"],mot["Imotor"],mot["rpmmotor"],mot["rendmotor"],mot["fpmotor"],mot["addrmotor"],newlaststamp)
                                    print(f'\nValores do motor {readm} lidos e inseridos no DB com sucesso!!\n')
                                    sleep(0.8)
                                except Exception as e:
                                    print('\033[31mERRO: ', e.args, '\033[m')
                                    try:
                                        sleep(0.5)
                                        print('\nSegunda tentativa..')
                                        if not self._cliente.is_open():
                                            print('\nReiniciando cliente Modbus..\n')
                                            self._cliente.open()
                                        sleep(2)
                                        for i in range(0, int(nvezes)):
                                            print(f'\033[33mLeitura {i + 1}:\033[m')
                                            stamp = (i+1)
                                            self.lerMotor(int(readm), self.motores)
                                            sleep(self._scan_time)
                                        print(f'\nValores do motor {readm} lidos e inseridos no DB com sucesso!!\n')
                                        sleep(0.8)
                                    except Exception as e:
                                        print('\033[31mERRO: ', e.args, '\033[m')
                                        print('\nInfelizmente o Cliente não conseguiu receber uma resposta..\nÉ sugerido reiniciar todo o sistema. \nCaso isso não resolva, entre em contato com a assistência técnica. \nVoltando ao menu..\n\n')
                                        sleep(2.5)
                            else:
                                print(f'\033[33m\nNão existem motores cadastrados!\033[m \nPor favor, cadastre pelo menos um motor.\n')
                                sleep(2)
                                
                    except Exception as e:
                        print('\033[31mERRO: ', e.args, '\033[m')

                elif sel == '6':
                    sleep(0.2)
                    print('\n\033[32mFechando sistema..\033[m')
                    sleep(0.5)
                    self._cliente.close()
                    atendimento = False                    

                else:
                    sleep(0.3)
                    print('\033[31mSeleção inválida..\033[m\n')
                    sleep(0.7)
        except Exception as e:
            print('\033[31mERRO: ', e.args, '\033[m')

    def createTableModbus(self):
        """
        Método que cria a tabela para armazenamento de dados lidos pelo cliente Modbus
        """
        try:
            sql_str = f"""
            CREATE TABLE IF NOT EXISTS modbusValues (
                ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Stamp INTEGER, Addr TEXT, Type TEXT, Value REAL, TimeStamp1 TEXT NOT NULL)
                """
            self._cursor.execute(sql_str)
            self._con.commit()
        except Exception as e:
            print('\033[31mERRO: ', e.args, '\033[m')
    
    def createTable(self):
        """
        Método que cria a tabela para armazenamento dos dados, com nomes simulados de parâmetros lidos
        """
        try:
            sql_str = f"""
            CREATE TABLE IF NOT EXISTS pointValues (
                ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Addr TEXT, Type TEXT, NameParam TEXT, Value REAL, TimeStamp1 TEXT NOT NULL)
                """
            self._cursor.execute(sql_str)
            self._con.commit()
        except Exception as e:
            print('\033[31mERRO: ', e.args, '\033[m')

    def createTableenergy(self):
        """
        Método que cria a tabela para armazenamento dos dados, caso ela não exista (com variáveis separadas por coluna)
        """
        try:
            sql_str = f"""
            CREATE TABLE IF NOT EXISTS energyTable (
                Leitura INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Stamp INTEGER, "Modelo" TEXT, "P. Mecânica (W)" REAL, "P. Aparente (VA)" REAL, "Tensão Nominal (V)" INTEGER, "Tensão Medida (V)" REAL, "Corrente Nominal (A)" REAL, "Corrente Medida (A)" REAL, "Rendimento Motor (%)" REAL, "Rendimento Calc (%)" REAL, "FP Motor" REAL, "Temperatura (C°)" REAL, TimeStamp1 TEXT NOT NULL)
                """
            self._cursor.execute(sql_str)
            self._con.commit()
        except Exception as e:
            print('\033[31mERRO: ', e.args, '\033[m')

    def createTableMotor(self):
        """
        Método que cria a tabela para cadastramento de motores)
        
        """
        try:
            sql_str = f"""
            CREATE TABLE IF NOT EXISTS motorTable (
                "ID" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "Modelo" TEXT, "N° Polos" INTEGER, "P. Nominal (CV)" REAL, "P. Mecânica (W)" REAL, "Tensão Nominal (V)" INTEGER, "Corrente Nominal (A)" REAL, "Rotação Nominal (RPM)" INTEGER, "Rendimento (%)" REAL, "Fator de Potência" REAL, "AddrModbus" TEXT)
                """
            self._cursor.execute(sql_str)
            self._con.commit()
        except Exception as e:
            print('Erro ao criar tabelo motor!')
            print('\033[31mERRO: ', e.args, '\033[m')

    def readArq(self):
        try:
            dados_motor_arq = dict()
            self.motores.clear()
            self.arq = open('motores.txt', 'rt')
            self.arq.seek(0, 0)
            for line in self.arq.readlines():
                dados_motor_arq.clear()
                mot = line.split(';')
                mot[9] = mot[9].replace('\n', '')
                dados_motor_arq['modmotor'] = mot[0]
                dados_motor_arq['polmotor'] = mot[1]
                dados_motor_arq['pnmotor'] = mot[2]
                dados_motor_arq['pnmotorkw'] = mot[3]
                dados_motor_arq['Vmotor'] = mot[4]
                dados_motor_arq['Imotor'] = mot[5]
                dados_motor_arq['rpmmotor'] = mot[6]
                dados_motor_arq['rendmotor'] = mot[7]
                dados_motor_arq['fpmotor'] = mot[8]
                dados_motor_arq['addrmotor'] = mot[9]
                # dados_motor_arq['laststamp'] = mot[10]
                self.motores.append(dados_motor_arq.copy())
            return self.motores
        except Exception as e:
            print('erro na leitura do arquivo')
            print('\033[31mERRO: ', e.args, '\033[m')
        finally:
            self.arq.seek(0, 0)
            self.arq.close()
       
    def writeArq(self,modmotor,polmotor,pnmotor,pnmotorkw,Vmotor,Imotor,rpmmotor,rendmotor,fpmotor,addrmotor,laststamp=0):
        try:
            self.arq = open('motores.txt', 'at')
        except Exception as e:
            print('\033[31mERRO: ', e.args, '\033[m')
        else:
            try:
                self.arq.write(f'{modmotor};{polmotor};{pnmotor};{pnmotorkw};{Vmotor};{Imotor};{rpmmotor};{rendmotor};{fpmotor};{addrmotor}\n')
                # self.arq.write(f'{modmotor};{polmotor};{pnmotor};{pnmotorkw};{Vmotor};{Imotor};{rpmmotor};{rendmotor};{fpmotor};{addrmotor};{laststamp}\n')
            except Exception as e:
                print('\033[31mERRO: ', e.args, '\033[m')
            finally:
                self.arq.close()

    # def editlinhaArq(self,index_linha,modmotor,polmotor,pnmotor,pnmotorkw,Vmotor,Imotor,rpmmotor,rendmotor,fpmotor,addrmotor,laststamp):
    #     try:
    #         with open('motores.txt', 'r') as f:
    #             text = f.readlines()
    #         with open('motores.txt', 'w') as f:
    #             for i in text:
    #                 if text.index(i)==index_linha:
    #                     f.write(f'{modmotor};{polmotor};{pnmotor};{pnmotorkw};{Vmotor};{Imotor};{rpmmotor};{rendmotor};{fpmotor};{addrmotor};{laststamp}\n')
    #                 else:
    #                     f.write(i)
    #     except Exception as e:
    #         print('\033[31mERRO: ', e.args, '\033[m')
    

    def createTableReadMotor(self, readm):
        """
        Método que cria a tabela para leitura de motores
        
        """
        try:
            sql_str = f"""
            CREATE TABLE IF NOT EXISTS motoread{readm}Table (
                "Leitura" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "Modelo" TEXT, "P. Mecânica (W)" REAL, "Tensão Nominal (V)" INTEGER, "Tensão Medida (V)" REAL, "Corrente Nominal (A)" REAL, "Corrente Medida (A)" REAL, "Rendimento Motor (%)" REAL, "Rendimento Calc (%)" REAL, "FP Motor" REAL, "P. Aparente (VA)" REAL, "Temperatura (C°)" REAL, TimeStamp1 TEXT NOT NULL)
                """
            self._cursor.execute(sql_str)
            self._con.commit()
        except Exception as e:
            print('Erro ao criar tabelo motor!')
            print('\033[31mERRO: ', e.args, '\033[m')
    
    def inserirDBModbus(self, stamp, addrs, tipo, value):
        """
        Método para inserção dos dados lidos do servidor Modbus no DB
        """
        try:
            date = str(datetime.datetime.fromtimestamp(int(time.time())).strftime("%Y-%m-%d %H:%M:%S"))
            str_values = f"{stamp}, {addrs}, {tipo}, {value}, '{date}'"
            sql_str = f'INSERT INTO modbusValues (Stamp, Addr, Type, Value, TimeStamp1) VALUES ({str_values})'
            self._cursor.execute(sql_str)
            self._con.commit()
            #self._con.close()
        except Exception as e:
            print('\033[31mERRO: ', e.args, '\033[m')
    
    def inserirDB(self, addrs, tipo, namep, value):
        """
        Método para inserção dos dados no DB
        """
        try:
            date = str(datetime.datetime.fromtimestamp(int(time.time())).strftime("%Y-%m-%d %H:%M:%S"))
            str_values = f"{addrs}, {tipo}, {namep}, {value}, '{date}'"
            sql_str = f'INSERT INTO pointValues (Addr, Type, NameParam, Value, TimeStamp1) VALUES ({str_values})'
            self._cursor.execute(sql_str)
            self._con.commit()
            #self._con.close()
        except Exception as e:
            print('\033[31mERRO: ', e.args, '\033[m')

    def inserirDBenergy(self, stamp, modmot, valuec, valuet, potap, valuetemp, motor):
        """
        Método para inserção dos dados no DB
        inserirDBreadmotor(self, readm, valuet, valuec, potap, valuetemp, motor):
        (valuec=valuec, valuet=valuet, potel=potel, valuetemp=valuetemp)
        Leitura INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "Modelo" TEXT, "P. Mecânica (W)" REAL, "P. Aparente (VA)" REAL, "Tensão Nominal (V)" INTEGER, "Tensão Medida (V)" REAL, "Corrente Nominal (A)" REAL, "Corrente Medida (A)" REAL, "Rendimento Motor (%)" REAL, "Rendimento Calc (%)" REAL, "FP Motor" REAL, "Temperatura (C°)" REAL, TimeStamp1 TEXT NOT NULL)
        """
        try:
            date = str(datetime.datetime.fromtimestamp(int(time.time())).strftime("%Y-%m-%d %H:%M:%S"))
            acrtemp = 0
            if potap > 4000:
                if potap > 4420:
                    acrtemp =+ 8
                elif potap > 4440:
                    acrtemp =+ 10
                elif potap > 4460:
                    acrtemp =+ 14
                elif potap > 4520:
                    acrtemp =+ 17
                else:
                    acrtemp = 0
            elif potap > 6000:
                if potap > 6200:
                    acrtemp =+ 8
                elif potap > 6220:
                    acrtemp =+ 10
                elif potap > 6240:
                    acrtemp =+ 14
                elif potap > 6280:
                    acrtemp =+ 17
                else:
                    acrtemp = 0
            elif potap > 8000:
                if potap > 8780:
                    acrtemp =+ 8
                elif potap > 8810:
                    acrtemp =+ 10
                elif potap > 8820:
                    acrtemp =+ 14
                elif potap > 8840:
                    acrtemp =+ 17
                else:
                    acrtemp = 0
            elif potap > 10000:
                if potap > 10530:
                    acrtemp =+ 8
                elif potap > 10570:
                    acrtemp =+ 10
                elif potap > 10620:
                    acrtemp =+ 14
                elif potap > 10670:
                    acrtemp =+ 17
                else:
                    acrtemp = 0
            else:
                acrtemp = 0
            modmot = str(motor['modmotor'])
            pmecmot = float(float(motor['pnmotor'])*735.5)
            tnomot = float(motor['Vmotor'])
            inomot = float(motor['Imotor'])
            rendmot = float(motor['rendmotor'])
            fpmot = float(motor['fpmotor'])
            pelec = potap*fpmot
            rendcalc = round(((pmecmot/pelec)*100), 2)
            str_values = f"{stamp}, '{modmot}', {pmecmot}, {potap}, {tnomot}, {valuet}, {inomot}, {valuec}, {rendmot}, {rendcalc}, {fpmot},  {valuetemp+acrtemp}, '{date}'"
            sql_str = f'INSERT INTO energyTable (Stamp, Modelo, "P. Mecânica (W)", "P. Aparente (VA)", "Tensão Nominal (V)", "Tensão Medida (V)", "Corrente Nominal (A)", "Corrente Medida (A)", "Rendimento Motor (%)", "Rendimento Calc (%)", "FP Motor", "Temperatura (C°)", TimeStamp1) VALUES ({str_values})'
            self._cursor.execute(sql_str)
            self._con.commit()
            #self._con.close()
        except Exception as e:
            print('\033[31mERRO: ', e.args, '\033[m')

    def inserirDBMotor(self,modmotor='W22',polmotor=6,pnmotor=5,Vmotor=380,Imotor=6.9,rpmmotor=1200,rendmotor=92.4,fpmotor=0.94,addrmotor=1):
        """
        Método para inserção dos dados do motor no DB
            modmotor = str(input('Modelo do motor: '))
            polmotor = str(input('N° Polos: '))
            pnmotor = float(input('Potência nominal (CV): '))
            Vmotor = float(input('Tensão nominal (V): '))
            Imotor = float(input('Corrente nominal (A): '))
            rpmmotor = int(input('Rotação Nominal (RPM): '))
            rendmotor = float(input('Rendimento (%): '))
            fpmotor = float(input('Fator de Potência: '))
        """
        try:
            pnmotorkw = float(pnmotor*7355)/10000
            pnmotorkw = round(pnmotorkw, 3)
            str_values = f"'{modmotor}', {polmotor}, {pnmotor}, {pnmotorkw}, {Vmotor}, {Imotor}, {rpmmotor},{rendmotor}, {fpmotor}, {addrmotor}"
            sql_str = f'INSERT INTO motorTable (Modelo, "N° Polos", "P. Nominal (CV)", "P. Mecânica (W)", "Tensão Nominal (V)", "Corrente Nominal (A)", "Rotação Nominal (RPM)", "Rendimento (%)", "Fator de Potência", "AddrModbus") VALUES ({str_values})'
            self._cursor.execute(sql_str)
            self._con.commit()
            #self._con.close()
            sleep(0.3)
            try:
                # self.creatArq()
                self.writeArq(modmotor=modmotor, polmotor=polmotor, pnmotor=pnmotor, pnmotorkw=pnmotorkw, Vmotor=Vmotor, Imotor=Imotor, rpmmotor=rpmmotor, rendmotor=rendmotor, fpmotor=fpmotor, addrmotor=addrmotor)
            except Exception as e:
                print('Erro ao inserir motor no arquivo')
                print('\033[31mERRO: ', e.args, '\033[m')
            print('\nMotor cadastrado com sucesso!\n')
            sleep(0.3)

        except Exception as e:
            print('Erro ao inserir DBmotor')
            print('\033[31mERRO: ', e.args, '\033[m')

    def inserirDBreadmotor(self, readm, valuet, valuec, potap, valuetemp, motor):
        """
        Método para inserção das leituras dos motores no DB
        Com função para aumentar a temp de acordo com a potência calculada
        """
        try:
            date = str(datetime.datetime.fromtimestamp(int(time.time())).strftime("%Y-%m-%d %H:%M:%S"))
            acrtemp = 0
            if potap > 4000:
                if potap > 4420:
                    acrtemp =+ 8
                elif potap > 4440:
                    acrtemp =+ 10
                elif potap > 4460:
                    acrtemp =+ 14
                elif potap > 4520:
                    acrtemp =+ 17
                else:
                    acrtemp = 0
            elif potap > 6000:
                if potap > 6200:
                    acrtemp =+ 8
                elif potap > 6220:
                    acrtemp =+ 10
                elif potap > 6240:
                    acrtemp =+ 14
                elif potap > 6280:
                    acrtemp =+ 17
                else:
                    acrtemp = 0
            elif potap > 8000:
                if potap > 8780:
                    acrtemp =+ 8
                elif potap > 8810:
                    acrtemp =+ 10
                elif potap > 8820:
                    acrtemp =+ 14
                elif potap > 8840:
                    acrtemp =+ 17
                else:
                    acrtemp = 0
            elif potap > 10000:
                if potap > 10530:
                    acrtemp =+ 8
                elif potap > 10570:
                    acrtemp =+ 10
                elif potap > 10620:
                    acrtemp =+ 14
                elif potap > 10670:
                    acrtemp =+ 17
            else:
                acrtemp = 0
            modmot = str(motor['modmotor'])
            pmecmot = float(float(motor['pnmotor'])*735.5)
            tnomot = float(motor['Vmotor'])
            inomot = float(motor['Imotor'])
            rendmot = float(motor['rendmotor'])
            fpmot = float(motor['fpmotor'])
            pelec = potap*fpmot
            rendcalc = round(((pmecmot/pelec)*100), 2)
            str_values = f"'{modmot}', {pmecmot}, {tnomot}, {valuet}, {inomot}, {valuec}, {rendmot}, {rendcalc}, {fpmot}, {potap}, {valuetemp+acrtemp}, '{date}'"
            sql_str = f'INSERT INTO motoread{readm}Table (Modelo, "P. Mecânica (W)", "Tensão Nominal (V)", "Tensão Medida (V)", "Corrente Nominal (A)", "Corrente Medida (A)", "Rendimento Motor (%)", "Rendimento Calc (%)", "FP Motor", "P. Aparente (VA)", "Temperatura (C°)", TimeStamp1) VALUES ({str_values})'
            self._cursor.execute(sql_str)
            self._con.commit()
            #self._con.close()
        except Exception as e:
            print('Erro ao inserir Leitura do motor no DB')
            print('\033[31mERRO: ', e.args, '\033[m')

    def lerMotor(self, stamp, readm, motores):
        """
        Método para leitura FLOAT MODBUS dos motores cadastrados
        """
        leng = 5
        tipo = 3
        motor = motores[readm-1]
        addr = int(motor['addrmotor'])
        modmot = str(motor['modmotor'])
        i = 0
        g = 0
        e1 = []
        while i < leng:
            if tipo == 3:
                i1 = self._cliente.read_holding_registers(addr - 1 + g, 2)
                tipore = "'F03HR'"  
                ende = 40000
            elif tipo == 4:
                i1 = self._cliente.read_input_registers(addr - 1 + g, 2)
                tipore = "'F04IR'"
                ende = 30000
            else:
                print('Tipo inválido..')
            for x in i1:
                x = bin(x).lstrip("0b")
                e1.insert(0 + g, x)
            i += 1
            g += 2
        e = 0
        while e <= leng:
            e2 = ''
            for x in e1:
                e2 = str(f'{e2}{x.rjust(16, "0")} ')
            e += 1
        b2 = str(f'{e2}')
        e3 = b2.split()
        y = 0
        while y < len(e3):
            ieee = f'{e3[0+y]}{e3[1+y]}'
            sign = int(ieee[0])
            expo = str(ieee[1:9])
            expodec = 0
            expopot = 7
            for i in range(8):
                expodec = expodec + (int(expo[i]) * (2**expopot))
                expopot -= 1
            mant = str(ieee[9:])
            mantdec = 0
            mantpot = -1
            for i in range(23):
                mantdec = mantdec + (int(mant[i]) * (2 ** mantpot))
                mantpot -= 1
            value = ((-1)**sign)*(1+mantdec)*2**(expodec-127)
            print(f'{round(value, 3)}')
            if y == 0:
                namep = "'Corrente I1 (A)'"
                valuec1 = round(value, 2)
            elif y == 2:
                namep = "'Corrente I2 (A)'"
                valuec2 = round(value, 2)
            elif y == 4:
                namep = "'Corrente I3 (A)'"
                valuec3 = round(value, 2)
            elif y == 6:
                namep = "'Tensão (V)'"
                valuet = round(value, 2)
            elif y == 8:
                namep = "'Temperatura (C°)'"
                valuetemp = round(value, 1)
            else:
                namep = "'-Unknown-'"
            y += 2
            self.inserirDB(addrs=(ende+addr+y-2), tipo=tipore,  namep=namep, value=round(value, 2))
        noaddr = "'- - -'"
        typecalc = "'CALC.'"
        medcn = "'Corrente Média Trifásica (A)'"
        valuec = (valuec1+valuec2+valuec3)/3
        self.inserirDB(addrs=noaddr, tipo=typecalc, namep=medcn, value=round(valuec, 2))
        npotap = "'Potência Aparente (VA)'"
        potap = valuec*1.73205080757*valuet
        self.inserirDB(addrs=noaddr, tipo=typecalc, namep=npotap, value=round(potap, 2))
        self.inserirDBenergy(stamp=stamp, modmot=modmot, valuec=round(valuec, 3), valuet=valuet, potap=round(potap, 3), valuetemp=valuetemp, motor=motor)
        # (Modelo, "P. Mecânica (W)", "P. Aparente (VA)", "Tensão Nominal (V)", "Tensão Medida (V)", Corrente Nominal (A)", "Corrente Medida (A)", "Rendimento Motor (%)", "Rendimento Calc (%)", "FP Motor", "Temperatura (C°)", TimeStamp1)
        self.inserirDBreadmotor(readm=readm, valuet=valuet, valuec=round(valuec, 3), potap=round(potap, 2), valuetemp=valuetemp, motor=motor)
        return

    def lerDado(self, stamp, tipo, addr, leng=1):
        """
        Método para leitura MODBUS
        """
        if tipo == 1:
            co = self._cliente.read_coils(addr - 1, leng)
            ic = 0
            while ic <= leng:
                if ic == leng:
                    break
                else:
                    value = co[0 + ic]
                    ic += 1
                    print(value)
                    if value == True:
                        value = 1
                    else:
                        value = 0
                    # self.inserirDB(addrs=(addr+ic-1), tipo="'F01CS'", namep="'ON/OFF'", value=value)
                    self.inserirDBModbus(stamp=stamp, addrs=(addr+ic-1), tipo="'F01-CoilStatus'", value=value)
            return 

        elif tipo == 2:
            di = self._cliente.read_discrete_inputs(addr - 1, leng)
            idi = 0
            while idi <= leng:
                if idi == leng:
                    break
                else:
                    value = di[0 + idi]
                    idi += 1
                    print(value)
                    # self.inserirDB(addrs=(10000+addr+idi-1), tipo="'F02IS'", namep="'ON/OFF'",value=value)
                    self.inserirDBModbus(stamp=stamp, addrs=(10000+addr+idi-1), tipo="'F02-InputStatus'", value=value)
            return 

        elif tipo == 3:
            hr = self._cliente.read_holding_registers(addr - 1, leng)
            ihr = 0
            while ihr <= leng:
                if ihr == leng:
                    break
                else:
                    value = hr[0+ihr]
                    ihr += 1
                    print(value)
                    # self.inserirDB(addrs=(40000+addr+ihr-1), tipo="'F03HR'", namep="'Temperatura (C)'", value=value)
                    self.inserirDBModbus(stamp=stamp, addrs=(40000+addr+ihr-1), tipo="'F03-HoldingRegister'", value=value)
            return 

        elif tipo == 4:
            ir = self._cliente.read_input_registers(addr - 1, leng)
            iir = 0
            while iir <= leng:
                if iir == leng:
                    break
                else:
                    value = ir[0 + iir]
                    iir += 1
                    print(value)
                    # self.inserirDB(addrs=(30000+addr+iir-1), tipo="'F04IR'",  namep="'Total Product'", value=value)
                    self.inserirDBModbus(stamp=stamp, addrs=(30000+addr+iir-1), tipo="'F04-InputRegister'", value=value)
            return 

        else:
            print('Tipo de leitura inválido..')

    def lerDadoFloat(self, stamp, tipo, addr, leng):
        """
        Método para leitura FLOAT MODBUS
        """
        i = 0
        g = 0
        e1 = []
        while i < leng:
            if tipo == 3:
                i1 = self._cliente.read_holding_registers(addr - 1 + g, 2)
                tipore = "'F03-HoldingRegister-FP'"  
                ende = 40000
            elif tipo == 4:
                i1 = self._cliente.read_input_registers(addr - 1 + g, 2)
                tipore = "'F04-InputRegister-FP'"
                ende = 30000
            else:
                print('Tipo inválido..')
            for x in i1:
                x = bin(x).lstrip("0b")
                e1.insert(0 + g, x)
            i += 1
            g += 2
        e = 0
        while e <= leng:
            e2 = ''
            for x in e1:
                e2 = str(f'{e2}{x.rjust(16, "0")} ')
            e += 1
        b2 = str(f'{e2}')
        e3 = b2.split()
        y = 0
        while y < len(e3):
            ieee = f'{e3[0+y]}{e3[1+y]}'
            sign = int(ieee[0])
            expo = str(ieee[1:9])
            expodec = 0
            expopot = 7
            for i in range(8):
                expodec = expodec + (int(expo[i]) * (2**expopot))
                expopot -= 1
            mant = str(ieee[9:])
            mantdec = 0
            mantpot = -1
            for i in range(23):
                mantdec = mantdec + (int(mant[i]) * (2 ** mantpot))
                mantpot -= 1
            value = ((-1)**sign)*(1+mantdec)*2**(expodec-127)
            print(f'{round(value, 3)}')
            if y == 0:
                namep = "'Corrente I1 (A)'"
                valuec1 = round(value, 2)
            elif y == 2:
                namep = "'Corrente I2 (A)'"
                valuec2 = round(value, 2)
            elif y == 4:
                namep = "'Corrente I3 (A)'"
                valuec3 = round(value, 2)
            elif y == 6:
                namep = "'Tensão (V)'"
                valuet = round(value, 2)
            elif y == 8:
                namep = "'Temperatura (C°)'"
                valuetemp = round(value, 1)
            else:
                namep = "'-Unknown-'"
            y += 2
            # self.inserirDB(addrs=(ende+addr+y-2), tipo=tipore,  namep=namep, value=round(value, 2))
            self.inserirDBModbus(stamp=stamp, addrs=(ende+addr+y-2), tipo=tipore, value=value)
        # noaddr = "'- - -'"
        # typecalc = "'CALC.'"
        # medcn = "'Corrente Média Trifásica (A)'"
        # valuec = (valuec1+valuec2+valuec3)/3
        # self.inserirDB(addrs=noaddr, tipo=typecalc, namep=medcn, value=round(valuec, 2))
        # npotap = "'Potência Aparente (VA)'"
        # potap = valuec*1.73205080757*valuet
        # self.inserirDB(addrs=noaddr, tipo=typecalc, namep=npotap, value=round(potap, 2))
        # self.inserirDBenergy(valuec=round(valuec, 3), valuet=valuet, potap=round(potap, 3), valuetemp=valuetemp)
        return

    def lerDadoFloatSwapped(self, stamp, tipo, addr, leng):
        """
        Método para leitura FLOAT SWAPPED MODBUS
        """
        i = 0
        g = 0
        e1 = []
        while i < leng:
            if tipo == 3:
                i1 = self._cliente.read_holding_registers(addr - 1 + g, 2)
                tipore = "'F03-HoldingRegister-FS'"
                ende = 40000
            elif tipo == 4:
                i1 = self._cliente.read_input_registers(addr - 1 + g, 2)
                tipore = "'F04-InputRegister-FS'"
                ende = 30000
            else:
                print('Tipo inválido..')
            i2 = i1[::-1]
            for x in i2:
                x = bin(x).lstrip("0b")
                e1.insert(0 + g, x)
            i += 1
            g += 2
        e = 0
        while e <= leng:
            e2 = ''
            for x in e1:
                e2 = str(f'{e2}{x.rjust(16, "0")} ')
            e += 1
        b2 = str(f'{e2}')
        e3 = b2.split()
        y = 0
        while y < len(e3):
            ieee = f'{e3[0+y]}{e3[1+y]}'
            sign = int(ieee[0])
            expo = str(ieee[1:9])
            expodec = 0
            expopot = 7
            for i in range(8):
                expodec = expodec + (int(expo[i]) * (2**expopot))
                expopot -= 1
            mant = str(ieee[9:])
            mantdec = 0
            mantpot = -1
            for i in range(23):
                mantdec = mantdec + (int(mant[i]) * (2 ** mantpot))
                mantpot -= 1
            value = ((-1)**sign)*(1+mantdec)*2**(expodec-127)
            print(f'{round(value, 3)}')
            if y == 0:
                namep = "'Corrente I1 (A)'"
                valuec1 = round(value, 2)
            elif y == 2:
                namep = "'Corrente I2 (A)'"
                valuec2 = round(value, 2)
            elif y == 4:
                namep = "'Corrente I3 (A)'"
                valuec3 = round(value, 2)
            elif y == 6:
                namep = "'Tensão (V)'"
                valuet = round(value, 2)
            elif y == 8:
                namep = "'Temperatura (C°)'"
                valuetemp = round(value, 1)
            else:
                namep = "'-Unknown-'"
            y += 2
            # self.inserirDB(addrs=(ende+addr+y-2), tipo=tipore,  namep=namep, value=round(value, 2))
            self.inserirDBModbus(stamp=stamp, addrs=(ende+addr+y-2), tipo=tipore, value=value)
        # noaddr = "'- - -'"
        # typecalc = "'CALC.'"
        # medcn = "'Corrente Média Trifásica (A)'"
        # valuec = (valuec1+valuec2+valuec3)/3
        # self.inserirDB(addrs=noaddr, tipo=typecalc, namep=medcn, value=round(valuec, 2))
        # npotap = "'Potência Aparente (VA)'"
        # potap = valuec*1.73205080757*valuet
        # self.inserirDB(addrs=noaddr, tipo=typecalc, namep=npotap, value=round(potap, 2))
        # self.inserirDBenergy(valuec=round(valuec, 3), valuet=valuet, potap=round(potap, 3), valuetemp=valuetemp)    
        return


    def escreveDado(self, stamp, tipo, addr, valor):
        """
        Método para escrita MODBUS
        """
        try:
            if tipo == 1:
                print(f'\033[33mValor {valor} escrito no endereço {addr}\033[m\n')
                self.inserirDBModbus(stamp=0, addrs=addr, tipo='F01-CS-Input', value=valor)
                return self._cliente.write_single_coil(addr - 1, valor)
            elif tipo == 2:
                print(f'\033[33mValor {valor} escrito no endereço {addr}\033[m\n')
                self.inserirDBModbus(stamp=0, addrs=addr, tipo='F03-HR-Input', value=valor)
                return self._cliente.write_single_register(addr - 1, valor)
            else:
                print('Tipo de escrita inválido..\n')

        except Exception as e:
            print('\033[31mERRO: ', e.args, '\033[m')

    