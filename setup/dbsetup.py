# import sqlite 3 api 
import sqlite3 as sqlite;
# initialize connection to ATM database
dbcon = sqlite.connect("../atmdb.db");
#try to execute db creation
try:
  # execute table creations 
    # create table for users
  dbcon.execute("""
      CREATE TABLE atm_user(
        user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        user_fullname varchar(60) NOT NULL,
        user_birthdate date NOT NULL,
        user_createdate datetime NOT NULL
      );
  """);
  # create table for accounts
  dbcon.execute("""
    CREATE TABLE atm_account(
      account_ag INTEGER NOT NULL,
      account_number INTEGER NOT NULL,
      user_id INTEGER NOT NULL,
      account_pwd text NOT NULL,
      current_balance decimal(10,2) NOT NULL DEFAULT 0,
      PRIMARY KEY(account_ag, account_number),
      FOREIGN KEY (user_id) REFERENCES atm_user(user_id) 
    );
  """);
  # create table for moviments
  dbcon.execute("""
    CREATE TABLE atm_moviment(
      moviment_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
      account_ag int(4) NOT NULL,
      account_number int(6) NOT NULL,
      user_id INTEGER NOT NULL,
      moviment_type varchar(2) NOT NULL,
      moviment_date datetime NOT NULL,
      moviment_value decimal(10,2) NOT NULL DEFAULT 0,
      FOREIGN KEY(account_ag, account_number, user_id) REFERENCES atm_account(account_ag, account_number, user_id)
    );
  """);
  print("-----------------------------------------------------------------");
  print(" Success: Database initialized correctly!");
  print("-----------------------------------------------------------------");
except Exception as e:
   print("----------------------------------------------------------------");
   print(" Failed to create and initialize database");
   print(" Error: "+str(e));
   print("----------------------------------------------------------------");

# close database connection
dbcon.close();


