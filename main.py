from this import s
from Database import insert
from Database import select
from Database import delete
from Database import update
from Database import TableModel
from Database import table_creator
from Database import table_loader
from Database import error_message


table_models = []
table_names = []

class Transaction:
    def __init__(self, sender_username, receiver_username, price):
        self.sender_username = sender_username
        self.receiver_username = receiver_username
        self.price = price

class Debt:
    def __init__(self, owner_account_alias, remaining_debt, total_debt):
        self.owner_account_alias = owner_account_alias
        self.remaining_debt = remaining_debt
        self.total_debt = total_debt

class Ticket:
    def __init__(self,pay_id, ticket_id, price):
        self.pay_id = pay_id
        self.ticket_id = ticket_id
        self.price = price

class Account:
    def __init__(self, alias, password, balance, email, favorite, owner_username, debt = 0):
        self.alias = alias
        self.password = password
        self.balance = balance
        self.debt = debt
        self.owner_username = owner_username
        self.email = email
        self.favorite = favorite



class User:
    def __init__(self, name, username, password, email, phone, balance):
        self.name = name
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.balance = balance
        self.accounts = []
        self.fav_accounts = []
        self.transactions = []
        

    def user_check(self, id):
        for table_name in table_names:

            if table_name == 'accounts':
                open_table = open(table_name+'.txt', 'r')
                accounts_info = open_table.readlines()
                each_account_info = []
                for i in range(0, len(accounts_info)):
                    each_account_info.append(accounts_info[i].split())

                open_table.close()

                for i in range(0, len(each_account_info)):
                    if each_account_info[i][5] == self.username:
                        self.accounts.append(Account(each_account_info[i][0], each_account_info[i][1], each_account_info[i][2], each_account_info[i][3], each_account_info[i][4], each_account_info[i][5]))

            elif table_name == 'transactions':
                open_table = open(table_name+'.txt', 'r')
                transactions_info = open_table.readlines()
                each_transaction_info = []
                
                for i in range(0, len(transactions_info)):
                    each_transaction_info.append(transactions_info[i].split())
            
                open_table.close()

                for i in range(0, len(each_transaction_info)):
                    if each_transaction_info[i][0] == self.username or each_transaction_info[i][0] == self.username :
                        self.transactions.append(Transaction(each_transaction_info[i][0], each_transaction_info[i][1], each_transaction_info[i][2]))

            else:
                pass
                


def sign_up(info):

    insert('users', table_models, table_names, info)
    print("Sign Up Successfull.")

def log_in(username, password):
    expressions = 'username == '+ str(username)+ ' AND '+ 'password == '+ str(password)
    expressions = expressions.split()
    selected_ids = select('users',table_models, table_names, expressions)
    if (len(selected_ids) == 1 and selected_ids[0] != 'Not Found.'):
        return selected_ids[0]
    else:
        raise ValueError("Error!")

def accounts_info():
    pass

def create_account():
    pass

def send_money():
    pass

def pay_ticket():
    pass

def close_account():
    pass

def get_loan():
    pass

def control_panel(id):
    print("login Successfull.")
    print("-----------------------------------------------------------------")
    users_info = open('users.txt','r')
    users_info = users_info.readlines()
    each_user_info = []
    for i in range(0, len(users_info)):
        each_user_info.append(users_info[i].split())
    users_info.close()
    id = int(id)
    user = User(each_user_info[id+1][0], each_user_info[id+1][1], each_user_info[id+1][2], each_user_info[id+1][3], each_user_info[id+1][4], each_user_info[id+1][5])
    user.user_check(id)
    while(True):
        print("hi %s. how can i help you?(options: create_account, accounts_info, get_loan, pay_ticket, close account, send_money",user.name)
        command = input()
        if command == "create_account":
            create_account()
        if command == "account_info":
            accounts_info()
        if command == "get_loan":
            get_loan()
        if command == "account_info":
            accounts_info()  
        if command == 'pay_ticket':
            pay_ticket()
        if command == 'send_money':
            send_money()
        if command == 'close_account':
            close_account()



if __name__ == '__main__':
    table_loader(table_models, table_names)
    print("-----------------------------------------------------------------")
    print("                     WELCOME TO OUR BANK!                        ")
    print("-----------------------------------------------------------------")
    print("log in or sign Up to continue.")
    print("-----------------------------------------------------------------")
    
    while(True):

        command = input()

        if command == 'log in':
            print("Please enter your username and password seperated by a space.")
            command = input()
            command = command.split()            id = log_in(command[0], command[1])
            if id != "Error!":
                control_panel(id)
            else:
                print("login failed.")
                
        elif command == 'sign up':
            print("Please enter your name, username, password, email, phone, and balance seperated by spaces.")
            command = input()
            command = command.split()
            sign_up(command)

        elif command == 'end':
            break

        else:
            error_message()


