import sqlite3 as sqlite;
# declare account class
class ATMAccount:
  agency = None;
  number = None;
  user_id = -1;
  user_fullname = None;
  balance = None;
  dbcon = None;

  def __init__(self):
    self.initDB();

  def getAccountNumber(self):
    return self.number;
  
  def getAgency(self):
    return self.agency;
  
  def getBalance(self):
    return self.balance;

  def getUserFullname(self):
    return self.user_fullname;
  
  def getUserID(self):
    return self.user_id;

  def getMovimentHistory(self):
    cursor = self.dbcon.cursor();
    cursor.execute("""
      SELECT moviment_date, moviment_type, moviment_value FROM atm_moviment 
      WHERE account_ag = '"""+self.getAgency()+"""'
      AND account_number = '"""+self.getAccountNumber()+"""'
      ORDER BY moviment_date DESC
    """);
    hists = cursor.fetchall();
    return hists;
   
  def deposit(self, amount, ag=None, account=None):
    cur = self.dbcon.cursor();
    agen = self.getAgency() if ag is None else ag;
    acc = self.getAccountNumber() if account is None else account;
    #if(self.getBalance() < amount)
      #raise Exception("Você não possui saldo para este depósio.");
    
    cur.execute("""
          UPDATE atm_account SET current_balance = current_balance + """+str(amount)+"""
          WHERE account_ag = '"""+str(agen)+"""'
          AND account_number = '"""+str(acc)+"""'
      """);
    if(ag is None and account is None):
      type_id = 'D';
      self.balance = self.balance + amount;
    else:
      type_id = 'DO';
      cur.execute("""
        INSERT INTO atm_moviment(account_ag, account_number, user_id, moviment_type, moviment_date, moviment_value)
        VALUES('"""+str(self.getAgency())+"""', '"""+str(self.getAccountNumber())+"""','"""+str(self.getUserID())+"""', '"""+type_id+"""', datetime('now'), """+str(amount*-1)+""")
     """);

    cur.execute("""
        INSERT INTO atm_moviment(account_ag, account_number, user_id, moviment_type, moviment_date, moviment_value)
        VALUES('"""+str(agen)+"""', '"""+str(acc)+"""','"""+str(self.getUserID())+"""', '"""+type_id+"""', datetime('now'), """+str(amount)+""")
    """);

    self.dbcon.commit();
    return True;
  

  def transfer(self, agen=None, account=None, amount=0):
    cur = self.dbcon.cursor();
    if(self.getBalance() < amount):
      raise Exception("Você não possui saldo para este depósio.");
    elif(str(self.getAgency()) == agen and str(self.getAccountNumber()) == account):
      raise Exception("Você não pode realizar uma transferência para você mesmo.");
    cur.execute("""
          UPDATE atm_account SET current_balance = current_balance + """+str(amount)+"""
          WHERE account_ag = '"""+str(agen)+"""'
          AND account_number = '"""+str(account)+"""'
     """);

    self.balance = self.balance - amount;
    cur.execute("""
        INSERT INTO atm_moviment(account_ag, account_number, user_id, moviment_type, moviment_date, moviment_value)
        VALUES('"""+str(self.getAgency())+"""', '"""+str(self.getAccountNumber())+"""','"""+str(self.getUserID())+"""', 'TO', datetime('now'), """+str(amount*-1)+""")
    """);

    cur.execute("""
        INSERT INTO atm_moviment(account_ag, account_number, user_id, moviment_type, moviment_date, moviment_value)
        VALUES('"""+str(agen)+"""', '"""+str(account)+"""','"""+str(self.getUserID())+"""', 'T', datetime('now'), """+str(amount)+""")
    """);

    self.dbcon.commit();
    return True;
   

  def db(self):
    return self.dbcon;

  def initDB(self):
    self.dbcon = sqlite.connect("atmdb.db");
  
  def closeDB(self):
    self.dbcon.close();
  
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
      self.agency = str(auth_rows[0]);
      self.number = str(auth_rows[1]);
      self.user_id = auth_rows[2];
      self.user_fullname = auth_rows[3];
      self.balance = float(auth_rows[4]);
      return True;
