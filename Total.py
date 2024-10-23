
class TableModel:
    def __init__(self, table_name):
        self.tale_name = table_name
        self.variable_names = []
        self.uniqueness = [] #0 means NOT unique and 1 means unique
        self.types = []
        self.limits = []

    def add_variable(self, variable_name, unique, variable_type, limit):
        self.variable_names.append(variable_name)
        self.uniqueness.append(unique)
        self.types.append(variable_type)
        self.limits.append(limit)


table_models = []
table_names = []

def table_creator(table_models,table_names):

    file = open('schema.txt', 'r')
    tables_info = open('tables_info.txt', 'x')
    id_numbers_file = open('id_numbers.txt', 'x')
    tables_info.write('-----\n')

    for line in file:
        line = line.split()

        if len(line) == 1 :
            table = open(line[0]+'.txt', 'x')
            table_models.append(TableModel(line[0]))
            id_numbers_file.write(str(0) + ' ')
            tables_info.write(line[0]+'\n') #table_name into info.txt
            table_names.append(line[0])

        elif len(line) == 0:
            tables_info.write('-----\n')
            table.close()
        
        else:
 
            variable_name = line[0]

            if line[1] == 'UNIQUE':
                unique = 1
                
                if variable_type[0:4] == 'CHAR':

                    line[len(line)-1] = line[len(line)-1].replace('(',' ')
                    line[len(line)-1] = line[len(line)-1].replace(')','')
                    temp = line[len(line)-1].split()
                    del line[len(line)-1]
                    line.append(temp[0])
                    line.append(temp[1])
                    variable_type = line[2]

                    limit = line[3]

                else:
                    limit = None
            
            else:
                unique = 0
                variable_type = line[1]

                if variable_type[0:4] == 'CHAR':
                    line[len(line)-1] = line[len(line)-1].replace('(',' ')
                    line[len(line)-1] = line[len(line)-1].replace(')','')
                    temp = line[len(line)-1].split()
                    del line[len(line)-1]
                    line.append(temp[0])
                    line.append(temp[1])
                    variable_type = line[1]

                    limit = line[2]

                else:
                    limit = None

            table.write(variable_name+' ')
            tables_info.write(variable_name+' '+ str(unique)+' ' + variable_type+' '+str(limit)+'\n')
            table_models[-1].add_variable(variable_name, unique, variable_type, limit)
            

    table.close()
    file.close()
    tables_info.close()
    id_numbers_file.close()



def table_loader(table_models, table_names):
    info = open('tables_info.txt', 'r')
    info_list = list(info.readlines())
    for i in range(0,len(info_list)):
        info_list[i] = info_list[i].replace('\n', '')

    for i in range (0,len(info_list)-1):

        if info_list[i] == '-----':
            table_models.append(TableModel(info_list[i+1]))
            table_names.append(info_list[i+1])

        elif info_list[i+1] == '-----':
            pass

        else:
            variable_info = info_list[i+1].split()
            variable_name = variable_info[0]
            unique = variable_info[1]
            variable_type = variable_info[2]
            limit = variable_info[3]
            table_models[-1].add_variable(variable_name, unique, variable_type, limit)

    info.close()


def error_message():
    print("Error! The command is not in the right format.")


def insert(table_name,table_models , table_names, values, id = None):

    selected_table = None
    
    if id == None:
        ids = open('id_numbers.txt','r')
        all_of_ids = ids.readline()
        all_of_ids = all_of_ids.split()

    for i in range (0, len(table_names)):
        if table_name == table_names[i]:
            selected_table = table_models[i]
            id_index = i
            break
    
    table_file = open(table_name+'.txt', 'a')
    if id == None:
        table_file.write('\n')

    for i in range (0, len(values)):
        if selected_table.types[i] == 'CHAR':
            if len(values[i]) <= int(selected_table.limits[i]):
                table_file.write(values[i]+' ')
            else:
                error_message()

        elif selected_table.types[i] == 'INTEGER':
            if values[i].isdigit():
                table_file.write(values[i]+' ')
            else:
                error_message()

        elif selected_table.types[i] == 'BOOLEAN':
            if type(values[i]) == type(True):
                table_file.write(values[i]+' ')
            else:
                error_message()

    if id == None:
        table_file.write(all_of_ids[id_index])
        all_of_ids[id_index] = int(all_of_ids[id_index])
        all_of_ids[id_index] += 1
        ids.close()
        ids = open('id_numbers.txt','w')
        for i in range (0,len(all_of_ids)):
            ids.write(str(all_of_ids[i]) + ' ')
        ids.close()
    else:
        table_file.write(id)


    table_file.close()


def select(table_name, table_models, table_names, expressions):

    selected_ids = []

    flag = 0
    for i in range (0, len(table_names)):
        if table_name == table_names[i]:
            selected_table = table_models[i]
            flag = 1
            break
    if flag == 0:
        raise ValueError('Not Found.') 

    table_file = open(table_name+'.txt', 'r')
    table_lines = table_file.readlines()
    table_variables = []
    for i in range(0,len(table_lines)):
        table_variables.append(table_lines[i].split())
    
    columns = []
    operation = ''
    for i in range (0,len(expressions)):
        if expressions[i] == 'OR':
            operation = 'or'
        elif expressions[i] == 'AND':
            operation = 'and'
        else:
            for j in range(0, len(table_variables[0])):
                if expressions[i] == table_variables[0][j]:
                    columns.append(j)
                    break
                
    if operation == 'or':
        for i in range(0,len(table_variables)):
            if (expressions[-1] == table_variables[i][columns[0]]) or (expressions[-1] == table_variables[i][columns[1]])or (expressions[2] == table_variables[i][columns[0]])or (expressions[2] == table_variables[i][columns[1]]):
                selected_ids.append(table_variables[i][-1])

    elif operation == 'and':
        for i in range(0,len(table_variables)):
            if ((expressions[-1] == table_variables[i][columns[0]]) and (expressions[2] == table_variables[i][columns[1]])) or ((expressions[2] == table_variables[i][columns[0]]) and (expressions[-1] == table_variables[i][columns[1]])):
                selected_ids.append(table_variables[i][-1])

    table_file.close()
    return selected_ids
 

def delete(table_name, table_models, table_names, expressions):

    selected_ids = select(table_name,expressions)
    table_file = open(table_name+'.txt', 'r')
    table_lines = table_file.readlines()
    table_file.close()

    table_variables = []
    for i in range(0,len(table_lines)):
        table_variables.append(table_lines[i].split())

    count = len(selected_ids)
    for i in range(0, len(table_variables)):
        for id in selected_ids:
            if count == 0:
                break
            if id == table_variables[i][-1]:
                del table_variables[i]
                count -= 1


        if len(table_variables) == 1:
            break


    table_file = open(table_name+'.txt', 'w')
    for j in range(0, len(table_variables[0])):
        table_file.write(table_variables[0][j]+' ')
    table_file.write('\n')

    for i in range(1,len(table_variables)):
        for j in range(0, len(table_variables[0])+1):
            table_file.write(table_variables[i][j]+' ')
        table_file.write('\n')


    table_file.close()

def update(table_name, table_models, table_names, expressions, updated_values):

    selected_ids = select(table_name,expressions)
    table_file = open(table_name+'.txt', 'r')
    table_lines = table_file.readlines()

    table_variables = []
    for i in range(0,len(table_lines)):
        table_variables.append(table_lines[i].split())
    
    for i in range(0, len(table_variables)):
        for id in selected_ids:
            if len(table_variables) == 1:
                break
            if id == table_variables[i][-1]:
                temp_id = table_variables[i][-1]
                delete(table_name, expressions)
                insert(table_name, updated_values, temp_id)

        if len(table_variables) == 1:
            break
        
    table_file.close()



if __name__ == '__main__':
    
    print("-----------------------------------------------------------------")
    print("Do you want to be build tables from scratch based on schema?(y/n)")
    print("-----------------------------------------------------------------")
    ans = input()
    if ans == 'y':   
        table_creator(table_models,table_names)
    elif ans == 'n':
        table_loader(table_models,table_names)    
    else:
        print("Pleas answer with 'y' or 'n'.")

    while (True):


        print("----------------------------------------------------------------")
        print("Use INSERT, SELECT, UPDATE, or DELETE commands. Or you can exit the programd with END command:")
        try:
            command = list(input().split())
        except:
            error_message()

        if (command[0] != '$') or (command[-1][-1] != ';'):
            print("The command format is incorrect. It must start with a '$' and end with a ';'.")
        
        else:

            if command [1] == 'INSERT':
                if command[2] == 'INTO' and command[4] == 'VALUES' :
                    table_name = command[3]
                    start_index = (command[5].find('(') + 1)
                    end_index = command[5].find(')')
                    values = command[5][start_index: end_index]
                    values = values.split(',')
                    insert(table_name, table_models, table_names, values)
                else:
                    error_message()


            elif command [1] == 'SELECT':
                if command[2] == 'FROM' and command[4] == 'WHERE' :
                    table_name = command[3]
                    command[-1] = command[-1].strip(';')
                    expressions = command[5:]
                    select(table_name, table_models, table_names, expressions)
                else:
                    error_message()

            elif command [1] == 'UPDATE':
                if command [-2] == 'VALUES' and command[3] == 'WHERE' :
                    table_name = command[2]
                    expressions = command[4:-2]
                    command[-1] = command[-1].strip(';')
                    command[-1] = command[-1].replace(')','')
                    command[-1] = command[-1].replace('(','')
                    updated_values = command[-1].split(',')
                    update(table_name, table_models, table_names, expressions, updated_values)

                else:
                    error_message()

            elif command [1] == 'DELETE':
                if  command[2] == 'FROM' and command[4] == 'WHERE' :
                    table_name = command[3]
                    command[-1] = command[-1].strip(';')
                    expressions = command[5:]
                    delete(table_name, table_models, table_names, expressions)
                else:
                    error_message()

            elif command [1] == 'END;':
                break

            


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
            command = command.split()
            id = log_in(command[0], command[1])
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


