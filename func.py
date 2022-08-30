import os
import sqlite3


con = sqlite3.connect("users.db")
cursor = con.cursor()


default_admin = [0, "Administrator", 99999999, 4, 1, "Default admin account"]

class Discord_User:


    def __init__(self, uid, user, gold, isMod):
        self.uid = uid
        self.user = user
        self.gold = gold
        self.isMod = isMod


    def modifyUID(self, newUID):
        self.uid = newUID



    def addPoints(self, ammount):
        self.gold += ammount
        
    
    def reducePoints(self, ammount):
        self.gold += ammount

    
    def newRole(self, roleNew):
        print("In work!")

    
    def addMod(self):
        self.isMod = True

    
    def __str__(self):
        return f'{self.uid} | {self.points} | {self.isMod}'




class ModUser(Discord_User):


    def __init__(self, uid, user, gold, isMod, isActive, additionalInfo):
        super().__init__(uid, user, gold, isMod)
        self.isMod = True
        self.isActive = isActive
        self.additionalInfo = additionalInfo

    
    def delMod(self):
        self.isMod = False
    

    def setInactive(self):
        self.isActive = False
    

    def setActive(self):
        self.isActive = True

    
    def __str__(self):
        return f'{self.uid} | {self.points} | {self.isMod} | {self.isActive} | {self.additionalInfo}'
    

def createTableinDB():
    cursor.execute("create table if not exists USERS (user_id, username, gold, modLevel, isActive, additionalInfo)")
    userEntryinDB(default_admin)

def userEntryinDB(x):
    cursor.execute("""insert into USERS values (?,?,?,?,?,?)""", x)
    con.commit()

def initializeUsers(x):
    y = Discord_User(int(x.id), str(x.name), int(50), 0)
    y_list = [y.uid, y.user, y.gold, y.isMod, 1, "-"]
    cursor.execute(f"""select exists(select user_id from USERS where user_id = {x.id})""")
    result = cursor.fetchone()
    print(result)
    if 1 in result:
        return f"User already in database: {x.id}"
    userEntryinDB(y_list)
    print(y_list)

def deleteMod(x):
    cursor.execute(f"""update USERS set modLevel = 0 where user_id = {x.id}""")
    con.commit()

def inititalizeMod(x):
    cursor.execute(f"""update USERS set modLevel = 1 where user_id = {x.id}""")
    con.commit()

def deleteSuperuser(x):
    cursor.execute(f"""update USERS set modLevel = 0 where user_id = {x.id}""")
    con.commit()

def initializeSuperuser(x):
    cursor.execute(f"""update USERS set modLevel = 3 where user_id = {x.id}""")
    con.commit()

def initializeOwner(x):
    cursor.execute(f"""update USERS set modLevel = 4 where user_id = {x.id}""")
    con.commit()

def autoInitialize(x):
    y = Discord_User(x.id, x, 0, x.roles, False)
    return f'{x} was initialized'

def resetUsers():
    cursor.execute("drop table USERS")
    createTableinDB()

def getModLevel(user):
    value = cursor.execute(f"""select modLevel from USERS where user_id = {user.id}""")
    result = value.fetchone()
    for value in result:
        return value

def addGoldtoUser(user, adress, ammount):
    if getModLevel(user) >= 3:
        if int(ammount) + getCurrentBalance(adress) <= 99999999:
            cursor.execute(f"""update USERS set gold = gold+{ammount} where user_id = {adress.id}""")
            con.commit()
            return 0
        else:
            cursor.execute(f"""update USERS set gold = 99999999 where user_id = {adress.id}""")
            con.commit()


def deductGoldfromUser(user, adress, ammount):
    if getModLevel(user) >= 3:
        if int(ammount) >= getCurrentBalance(adress):
            cursor.execute(f"""update USERS set gold = 0 where user_id = {adress.id}""")
            con.commit()
        else:
            cursor.execute(f"""update USERS set gold = gold-{ammount} where user_id = {adress.id}""")
            con.commit()
        return 0

def getCurrentBalance(x):
    value = cursor.execute(f"""select gold from USERS where user_id = {x.id}""")
    result = value.fetchone()
    for value in result:
        return value

def ownerCommandDeduceGold(adress, ammount):
    if int(ammount) >= getCurrentBalance(adress):
        cursor.execute(f"""update USERS set gold = 0 where user_id = {adress.id}""")
        con.commit()
    else:
        cursor.execute(f"""update USERS set gold = gold-{ammount} where user_id = {adress.id}""")
        con.commit()
    return 0

def ownerComandsetGold(x, y):
    if int(y) <= 99999999:
        cursor.execute(f"""update USERS set gold = {y} where user_id = {x.id}""")
        con.commit()
        return 0


def ownerComandaddGold(x, y):
    if int(y) <= 99999999:
        cursor.execute(f"""update USERS set gold = gold+{y} where user_id = {x.id}""")
        con.commit()
        return 0