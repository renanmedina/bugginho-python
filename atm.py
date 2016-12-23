# import required modules
import os;
import getpass as passExtractor;
import time;
import re as regex;
from datetime import datetime;
import locale;
from account import ATMAccount;

# declare ATM Class
class ATM:
  # ATM Class control fields
  authacc = None; 
  # current action choosen
  act_option = 1;

  def initialize(self):
    locale.setlocale(locale.LC_ALL, '');
    if self.authacc is None:
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
    print(" Bem vindo, "+self.authacc.getUserFullname()+".");
    print(" Ag: "+self.authacc.getAgency());
    print(" C/C: "+self.authacc.getAccountNumber());
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
    print("               PyLanguage ATM - Saldo de conta corrente (Ag: "+self.authacc.getAgency()+" C/C:"+self.authacc.getAccountNumber()+")");
    print("---------------------------------------------------------------------------------------------");
    print(" * Saldo atual: "+locale.currency(self.authacc.getBalance(), grouping=True));
    print("---------------------------------------------------------------------------------------------");
    input("Pressione [ENTER] para continuar ...");

  def displayHistory(self):
    self.clearScreen();
    print("----------------------------------------------------------------------------------------------");
    print("               PyLanguage ATM - Extrato de conta corrente (Ag: "+self.authacc.getAgency()+" C/C:"+self.authacc.getAccountNumber()+")");
    print("----------------------------------------------------------------------------------------------");
    print("        Data        \t           Tipo            \t          Valor");
    print("==============================================================================================");
    hists = self.authacc.getMovimentHistory();
    for mov in hists:
      movtip = str(mov[1]);
      if(movtip == 'D'):
        movtip = 'Depósito';
      elif(movtip == 'DO'):
        movtip = 'Depósito outra c/c';
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
    self.clearScreen();
    print("----------------------------------------------------------------------------------------------");
    print("                     "+("PyLanguage ATM - depositar em outra conta corrente" if another_account else "PyLanguage ATM - depositar em conta corrente"));                       
    print("----------------------------------------------------------------------------------------------");
    print("AG: "+self.authacc.getAgency());
    print("C/C: "+self.authacc.getAccountNumber());
    print("-----------------------------------------------------------------------------------------------");
    deposit_amount = float(input(" Informe o valor à ser depositado: "));  
    if(another_account):
      ag_deposit = str(input(" Informe a agencia que deseja depositar: "));
      acc_deposit = str(input(" Informe a conta que deseja depositar: "));
      deposit_ok = self.authacc.deposit(deposit_amount, ag_deposit, acc_deposit);
    else:
      deposit_ok = self.authacc.deposit(deposit_amount);
    
    if(deposit_ok):
      print("\n\n Depósito realizado com sucesso, aguarde recarregamento ...");
      time.sleep(2);


  def withdrawMoney(self):
    return '';
  
  def transferMoney(self):
    print("----------------------------------------------------------------------------------------------");
    print("                     PyLanguage ATM - transferência                                           ");                       
    print("----------------------------------------------------------------------------------------------");
    print("AG: "+self.authacc.getAgency());
    print("C/C: "+self.authacc.getAccountNumber());
    print("-----------------------------------------------------------------------------------------------");
    ag_transf = str(input("Informe a agencia para a transferência: "));
    acc_transf = str(input("Informe a conta para a transferência: "));
    transf_amount = float(input("Informe a quantia à ser transferida: "));
    
    self.authacc.transfer(ag_transf, acc_transf, transf_amount);
    print(" \n\n Trasnferência realizada com sucesso, aguarde recarregamento ...");
    time.sleep(2);

  def editPersonalInfo(self):
    return '';

  def requestAuth(self):
    self.drawWelcome();
    auth_ag = str(input(" Informe sua agência: "));
    auth_account = str(input(" Informe sua c/c: "));
    auth_pwd = str(passExtractor.getpass());
    print("\n => Validando informações, aguade ...");
    time.sleep(2);
    self.authacc = ATMAccount();
    # check if authentication succeds
    if self.authacc.authenticate(auth_ag, auth_account, auth_pwd):
     self.initialize();
    else:
      print(" Desculpe, não foi possivel realizar a autenticação de seus dados. Reiniciando processo, aguarde ...");
      time.sleep(3);
      self.initialize();
      
  def logout(self):
     self.clearScreen();
     print("----------------------------------------------------------------------------------------------");
     print("                      PyLanguage ATM - sair (Ag: "+self.authacc.getAgency()+" C/C:"+self.authacc.getAccountNumber()+")");
     print("----------------------------------------------------------------------------------------------");
     conf_logout = 'x';
     while(conf_logout != 'S' and conf_logout != 'N'):
      print("\n"+self.authacc.getUserFullname()+" deseja realmente sair ?");
      conf_logout = input("\nPressione [S/N]: ");
      if(conf_logout == 'N'):
        self.act_option = 0;
      elif(conf_logout == 'S'):
        self.authacc.closeDB();
        print("Obrigado pela visita, volte sempre !");
        time.sleep(1); 
  
  def clearScreen(self):
    if os.name == 'nt':
      os.system('cls');
    else:
      os.system('clear');





    
  