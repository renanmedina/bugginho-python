import os;
import getpass as passExtractor;
import sqlite3 as sqlite;
import time;

class ATM:
  
  account = None; 
  dbcon = None;
  act_option = 1;

  def initialize(self):
    self.connectDB();
    if self.account is None:
      self.requestAuth();
    else:
      while(self.act_option < 8):
        self.drawMenu();
        self.act_option = int(input("Escolha uma opção [ENTER]: "));
        if(self.act_option > 8 or self.act_option < 0):
          print(" Opção não disponível, favor selecione uma opção entre as listadas.")
          time.sleep(1);
          self.act_option = 1;
        elif(self.act_option == 1):
          self.displayBalance();
        elif(self.act_option == 2):
          self.displayHistory();
        elif(self.act_option == 3):
          # deposit money on current account
          self.depositMoney();
        elif(self.act_option == 4):
          # deposit money on another account (that's what means 'True')
          self.depositMoney(True);
        elif(self.act_option == 5):
          self.withdrawMoney();
        elif(self.act_option == 6):
          self.transferMoney();
        elif(self.act_option == 7):
          self.editPersonalInfo();
        else:
          print(" Obrigado pela visita, "+self.account["user_fullname"]+". Volte sempre !!");
          time.sleep(2);

  def drawWelcome(self):
    os.system("clear");
    print("=====================================================================================");
    print("                                   PyLanguage ATM                                    ");
    print("=====================================================================================");
    print(" *** Bem vindo ao PyLanguage ATM ***");
    print("-------------------------------------------------------------------------------------");

  def drawMenu(self):
    self.drawWelcome();
    print(" Bem vindo, "+self.account['user_fullname']+".");
    print(" Ag: "+self.account['agency']);
    print(" C/C: "+self.account['number']);
    print("-------------------------------------------------------------------------------------");
    print(" Opções disponíveis:");
    print("""
    1 - Consultar saldo
    2 - Emitir extrato
    3 - Depositar
    4 - Depositar em outra c/c
    5 - Sacar
    6 - Transferência
    7 - Alterar dados cadastrais
    8 - Sair
    """);

  def displayBalance(self):
    os.system("clear");
    print("---------------------------------------------------------------------------------------------");
    print("               PyLanguage ATM - Saldo de conta corrente (Ag: "+self.account["agency"]+" C/C:"+self.account["number"]+")");
    print("---------------------------------------------------------------------------------------------");
    print(" * Saldo atual: "+str(self.account["balance"]));
    print("---------------------------------------------------------------------------------------------");
    input("Pressione [ENTER] para continuar ...");
  
  def displayHistory(self):
    os.system("clear");
    print("----------------------------------------------------------------------------------------------");
    print("               PyLanguage ATM - Extrato de conta corrente (Ag: "+self.account["agency"]+" C/C:"+self.account["number"]+")");
    print("----------------------------------------------------------------------------------------------");
    cursor = self.dbcon.cursor();
    cursor.execute("""
      SELECT moviment_date, moviment_type, moviment_value FROM atm_moviment 
      WHERE account_ag = '"""+self.account["agency"]+"""'
      AND account_number = '"""+self.account["number"]+"""'
      ORDER BY moviment_date DESC
    """);
    hists = cursor.fetchall();
    print(" Data      \t      Tipo      \t      Valor");
    for mov in hists:
      movtip = str(mov[1]);
      if(movtip == 'D'):
        movtip = 'Depósito';
      elif(movtip == 'T'):
        movtip = 'Transferência';
      elif (movtip == 'TO'):
        movtip = 'Transferência outra c/c';
      elif(movtip == 'S'):
        movtip = 'Saque';
      print(" "+str(mov[0])+"      \t      "+movtip+"      \t      "+str(mov[2]));
    print("-----------------------------------------------------------------------------------------------");
    print(" Total de "+str(len(hists))+" registros\n");
    input(" Pressione [ENTER] para continuar ...");
  
  def depositMoney(self,another_account=False):
    return '';
  
  def withdrawMoney(self):
    return '';
  
  def transferMoney(self):
    return '';
  
  def editPersonalInfo(self):
    return '';

  def requestAuth(self):
    self.drawWelcome();
    auth_ag = str(input(" Informe sua agência: "));
    auth_account = str(input(" Informe sua c/c: "));
    auth_pwd = str(passExtractor.getpass());
    print("\n Validando informações, aguade ...");
    time.sleep(2);
    # check if authentication succeds
    if self.authenticate(auth_ag, auth_account, auth_pwd):
     self.initialize();
    else:
      print(" Desculpe, não foi possivel realizar a autenticação de seus dados. Reiniciando processo, aguarde ...");
      time.sleep(3);
      self.initialize();
      

  def authenticate(self, ag, acc, pwd):
    cur = self.dbcon.cursor();
    cur.execute("""
        SELECT b.account_ag, b.account_number, a.user_id, a.user_fullname, b.current_balance FROM atm_user a 
        INNER JOIN atm_account b ON a.user_id = b.user_id
        WHERE b.account_ag = '"""+ag+"""' 
        AND b.account_number = '"""+acc+"""'
        AND b.account_pwd = '"""+pwd+"""'
    """);

    auth_rows = cur.fetchone();

    if(auth_rows is None):
     return False;
    else:
      self.account = {'agency': str(auth_rows[0]),
                      'number': str(auth_rows[1]),
                      'user_id': auth_rows[2],
                      'user_fullname': auth_rows[3],
                      'balance': auth_rows[4]};
      return True;

  def connectDB(self):
    if(self.dbcon is None):
      self.dbcon = sqlite.connect("atmdb.db");
  
  def closeDB(self):
    self.dbcon.close();
    

    
  