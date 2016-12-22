# import required modules
import os;
import getpass as passExtractor;
import sqlite3 as sqlite;
import time;
import re as regex;
from datetime import datetime;
import locale;

# declare ATM Class
class ATM:
  # ATM Class control fields
  account = None; 
  # db connection
  dbcon = None;
  # current action choosen
  act_option = 1;

  def initialize(self):
    locale.setlocale(locale.LC_ALL, '');
    self.connectDB();
    if self.account is None:
      self.requestAuth();
    else:
      while(self.act_option < 8):
        self.drawMenu();
        self.act_option = input("Escolha uma opção [ENTER]: ");
        if(self.act_option == ''):
          self.act_option = 0;
          continue;
        else:
          self.act_option = int(self.act_option);
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
          self.logout();
          time.sleep(1);

  def drawWelcome(self):
    self.clearScreen();
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
    self.clearScreen();
    print("---------------------------------------------------------------------------------------------");
    print("               PyLanguage ATM - Saldo de conta corrente (Ag: "+self.account["agency"]+" C/C:"+self.account["number"]+")");
    print("---------------------------------------------------------------------------------------------");
    print(" * Saldo atual: "+str(self.account["balance"]));
    print("---------------------------------------------------------------------------------------------");
    input("Pressione [ENTER] para continuar ...");


  def displayHistory(self):
    self.clearScreen();
    print("----------------------------------------------------------------------------------------------");
    print("               PyLanguage ATM - Extrato de conta corrente (Ag: "+self.account["agency"]+" C/C:"+self.account["number"]+")");
    print("----------------------------------------------------------------------------------------------");
    print("        Data        \t           Tipo            \t          Valor");
    print("==============================================================================================");
    cursor = self.dbcon.cursor();
    cursor.execute("""
      SELECT moviment_date, moviment_type, moviment_value FROM atm_moviment 
      WHERE account_ag = '"""+self.account["agency"]+"""'
      AND account_number = '"""+self.account["number"]+"""'
      ORDER BY moviment_date DESC
    """);
    hists = cursor.fetchall();
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

      dt_reg = regex.match(r"([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}:[0-9]{2}:[0-9]{2})", str(mov[0]));
      dt_mov = dt_reg.group(3)+"/"+dt_reg.group(2)+"/"+dt_reg.group(1)+" "+dt_reg.group(4);
      mov_val =locale.currency(mov[2], grouping=True);
      print(" "+dt_mov+"      \t"+movtip.ljust(19)+"      \t"+mov_val);
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
    print("\n => Validando informações, aguade ...");
    time.sleep(2);
    # check if authentication succeds
    if self.authenticate(auth_ag, auth_account, auth_pwd):
     self.initialize();
    else:
      print(" Desculpe, não foi possivel realizar a autenticação de seus dados. Reiniciando processo, aguarde ...");
      time.sleep(3);
      self.initialize();
      
  def logout(self):
     self.clearScreen();
     print("----------------------------------------------------------------------------------------------");
     print("                      PyLanguage ATM - sair (Ag: "+self.account["agency"]+" C/C:"+self.account["number"]+")");
     print("----------------------------------------------------------------------------------------------");
     conf_logout = 'x';
     while(conf_logout != 'S' and conf_logout != 'N'):
      print("\n"+self.account["user_fullname"]+" deseja realmente sair ?");
      conf_logout = input("\nPressione [S/N]: ");
      if(conf_logout == 'N'):
        self.act_option = 0;
      elif(conf_logout == 'S'):
        self.closeDB();
        print("Obrigado pela visita, volte sempre !");
        time.sleep(1);
    
      
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
      self.dbcon = sqlite.connect("atmdb.db", detect_types=sqlite.PARSE_COLNAMES);
  
  def closeDB(self):
    self.dbcon.close();
  
  def clearScreen(self):
    if os.name == 'nt':
      os.system('cls');
    else:
      os.system('clear');





    
  