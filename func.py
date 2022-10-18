import os
import sqlite3
from numba import jit, cuda
import numba
from multiprocessing import Pool


con = sqlite3.connect("users.db")
cursor = con.cursor()

con2 = sqlite3.connect("resources.db")
cursor2 = con2.cursor()

con3 = sqlite3.connect("moderatedServers.db")
cursor3 = con3.cursor()

default_account = [0, "Default", 0, 0, 0]
default_account_res = [0, "Default", 0]
default_account_modservers = [0, 0]


def createTableinDB():
    cursor.execute("create table if not exists USERS (user_id, username, isSuperuser, isActive, isVIP)")
    #newEntry(default_account)

def createTableinDB2():
    cursor2.execute("create table if not exists RESOURCES (user_id, username, gold)")
    #newEntry2(default_account_res)

def createTableinDB3():
    cursor3.execute("create table if not exists MODSERVERS (user_id, modServer)")


def newEntry(x):
    cursor.execute("""insert into USERS values (?,?,?,?,?)""", x)
    con.commit()

def newEntry2(x):
    cursor2.execute("""insert into RESOURCES values (?,?,?)""", x)
    con2.commit()

def newEntry3(x):
    cursor3.execute("""insert into MODSERVERS values (?,?)""", x)
    con3.commit()

def massNewEntry(x):
    cursor.executemany("""insert into USERS values (?,?,?,?,?)""", (x))
    con.commit()

def massNewEntry2(x):
    cursor2.executemany("""insert into RESOURCES values (?,?,?)""", (x))
    con2.commit()

def newMassEntry3(x):
    cursor3.executemany("""insert into MODSERVERS values (?,?)""", (x))
    con3.commit()

def getCurrentBalance(target):
    value =  cursor2.execute(f"""select gold from RESOURCES where user_id = {target.id}""")
    result = value.fetchone()
    for i in result:
        return i

def goldTransacting(user, adress, ammount):
    usersBalance = getCurrentBalance(user)
    adressBalance = getCurrentBalance(adress)
    if int(ammount) <= usersBalance and int(ammount) + adressBalance <= 99999999:    
        cursor2.execute(f"""update RESOURCES set gold = gold-{ammount} where user_id = {user.id}""")
        cursor2.execute(f"""update RESOURCES set gold = gold+{ammount} where user_id = {adress.id}""")
    elif int(ammount) + adressBalance >= 99999999 and int(ammount) <= usersBalance:
        cursor2.execute(f"""update RESOURCES set gold = gold-{ammount} where user_id = {user.id}""")
        cursor2.execute(f"""update RESOURCES set gold = 99999999 where user_id = {adress.id}""")    
    elif int(ammount) + adressBalance <= 99999999 and int(ammount) >= usersBalance:
        cursor2.execute(f"""update RESOURCES set gold = 0 where user_id = {user.id}""")
        cursor2.execute(f"""update RESOURCES set gold = gold+{ammount} where user_id = {adress.id}""")
    elif int(ammount) + adressBalance >= 99999999 and int(ammount) >= usersBalance:
        cursor2.execute(f"""update RESOURCES set gold = 0 where user_id = {user.id}""")
        if usersBalance + adressBalance > 99999999:
            cursor2.execute(f"""update RESOURCES set gold = 99999999 where user_id = {adress.id}""")
        else:
            cursor2.execute(f"""update RESOURCES set gold = gold+{usersBalance} where user_id = {adress.id}""")
    con2.commit()
    return 0

class Common_User:
    
    def __init__(self, user_id, username, gold, isSuperuser, isActive, isVIP):
        self.user_id = user_id
        self.username = username
        self.gold = gold
        self.isSuperuser = isSuperuser
        self.isActive = isActive
        self.isVIP = isVIP
    
    
    def initializeUsersDB(self):

        # Users DB
        cursor.execute(f"""select exists(select user_id from USERS where user_id = {self.user_id})""")
        result = cursor.fetchone()
        #print(result)
        if 1 in result:
            return f"User already in users database: {self.user_id}"
        else:
            newEntry([self.user_id, self.username, self.isSuperuser, self.isActive, self.isVIP])
            con.commit()

        # Resources DB

        cursor2.execute(f"""select exists(select user_id from RESOURCES where user_id = {self.user_id})""")
        result = cursor2.fetchone()
        #print(result)
        if 1 in result:
            return f"User already in resources database: {self.user_id}"
        else:
            newEntry2([self.user_id, self.username, self.gold])
            print(self.user_id, self.username, self.isSuperuser, self.isActive, self.isVIP)
            con2.commit()
        return 0
    

    #def massInitialization(x):
    #
    #    for i in x:
    #        cursor.execute(f"""select exists(select user_id from USERS where user_id = {i[0]})""")
    #        result = cursor.fetchone()
    #        if 1 in result:
    #            return f"User already in users database: {i[0]}"
    #        else:
    #            newEntry([i[0], i[1], i[2], i[3], i[4], i[5]])
    #        cursor2.execute(f"""select exists(select user_id from RESOURCES where user_id = {i[0]})""")
    #        result = cursor2.fetchone()
    #        if 1 in result:
    #            return f"User already in resources database: {i[0]}"
    #        else:
    #            newEntry2([i[0], i[1], i[2]])
    #            print(i)
    #    con.commit()
    #    con2.commit()
    #    return 0

    def massInitializationOLD(x):
        print(x)
        USER_list = []
        RES_list = []
        n = 0
        for i in x:
            p1 = i[:3]
            p2 = p1[:] + i[4:7]
            RES_list.append(p1)
            USER_list.append(p2)
            #print(i[0][0])
            print(p2)
            cursor.execute(f"""select exists(select user_id from USERS where user_id = {i[0]})""")
            result = cursor.fetchone()
            if 1 in result:
                print(f"User already in users/resources database: {i[0]}")
                print(USER_list[n])
                #print(USER_list[n][0])
                del USER_list[n]
                del RES_list[n]
                #del(USER_list[n][0])
                #del(RES_list[n][0])
            n += 1
        print(x)
        massNewEntry(USER_list)
        massNewEntry2(RES_list)
        con.commit()
        con2.commit()
        return 0


    def massInitializationNEW(x):
        print(x)
        deletions = 0
        USER_list = []
        RES_list = []
        for i in range(len(x)):
            p1 = x[:][i][:3]
            p2 = p1[:] + x[i][4:6]
            RES_list.append(p1)
            USER_list.append(p2)
            #print(i[0][0])
            print(x[i][0])
            cursor.execute(f"""select exists(select user_id from USERS where user_id = {x[i][0]})""")
            result = cursor.fetchone()
            if 1 in result:
                deletions += 1
                print(f"User already in users/resources database: {x[i][0]}")
                #print(USER_list[i-deletions])
                #print(USER_list[n][0])
                del USER_list[i-deletions]
                del RES_list[i-deletions]
                #del(USER_list[n][0])
                #del(RES_list[n][0])
        #print(x)
        massNewEntry(USER_list)
        massNewEntry2(RES_list)
        con.commit()
        con2.commit()
        return 0


class Bot_Moderator(Common_User):

    def __init__(self, user_id, username, gold, isSuperuser, isActive, isVIP):
        super(Common_User).__init__(self, user_id, username, gold,  isSuperuser, isActive, isVIP)
    
    def deleteMod(user, guild):
        cursor3.execute(f"""select exists(select user_id from MODSERVERS where user_id= {user.id} and modServer = {guild.id})""")
        result = cursor3.fetchone()
        if 1 in result:
            return 1
        else:
            cursor3.execute(f"DELETE FROM MODSERVERS where user_id = {user.id} and modServer = {guild.id}")
            con.commit()
            return 0

    def addMod(user, guild):
        cursor3.execute(f"""select exists(select * from MODSERVERS where modServer = {guild.id} and user_id = {user.id})""")
        con3.commit()
        result = cursor3.fetchone()
        if 1 in result:
            return 1
        else:
            newEntry3([user.id, guild.id])
            con.commit()
            return 0
    
    def modList(guild):
        list = []
        modlist = cursor3.execute(f"""select user_id from MODSERVERS where modServer = {guild.id}""")
        result = modlist.fetchall()
        return result
        for i in result:
            list.append(i)
        return list

    def isMod(guild, user):
        exists = cursor3.execute(f"""select exists(select * from MODSERVERS where modServer = {guild.id} and user_id = {user.id})""")
        #server = cursor3.execute(f"""select modServer from MODSERVERS where user_id = {user.id}""")
        result = exists.fetchone()
        for i in result:
            if 1 in result:
                return True
        return False


class Bot_SU(Common_User):
    def __init__(self, user_id, username, gold, isActive, isVIP):
        super(Common_User).__init__(self, user_id, username, gold, isActive, isVIP)
        self.isSuperuser = 1

    def setInactive(user):
        cursor.execute(f"""update USERS set isActive = 0 where user_id = {user.id}""")
        con.commit()
        return 0
    
    def reactivate(user):
        cursor.execute(f"""update USERS set isActive = 1 where user_id = {user.id}""")
        con.commit()
        return 0
    
    def checkSu(user):
        su =  cursor.execute(f"""select isSuperuser from USERS where user_id = {user.id}""")
        result = su.fetchone()
        for i in result:
            return i
    
    def getActivity(user):
        cursor.execute(f"""select exists(select user_id from USERS where user_id = {user.id})""")
        value = cursor.fetchone()
        for i in value:
            if i == 1:
                act =  cursor.execute(f"""select isActive from USERS where user_id = {user.id}""")
                result = act.fetchone()
                for i in result:
                    return i

    def addGoldToUser(address, ammount):
        if int(ammount) + getCurrentBalance(address) <= 99999999:
                cursor2.execute(f"""update RESOURCES set gold = gold+{ammount} where user_id = {address.id}""")
                return 0
        else:
            cursor2.execute(f"""update RESOURCES set gold = 99999999 where user_id = {address.id}""")
        con2.commit()
        return 0

    def deductGoldFromUser(address, ammount):
        if int(ammount) >= getCurrentBalance(address):
                cursor2.execute(f"""update RESOURCES set gold = 0 where user_id = {address.id}""")
        else:
            cursor2.execute(f"""update RESOURCES set gold = gold-{ammount} where user_id = {address.id}""")
        con2.commit()
        return 0
    
    
class Bot_Owner(Common_User):
    def __init__(self):
        pass

    def deleteSuperuser(user):
        cursor.execute(f"""update USERS set isSuperuser = 0 where user_id = {user.id}""")
        con.commit()
        return 0

    def addSuperuser(user):
        cursor.execute(f"""update USERS set isSuperuser = 1 where user_id = {user.id}""")
        con.commit()
        return 0

    def resetUsers():
        cursor.execute("drop table USERS")
        createTableinDB()
        con.commit()
        return 0
    
    def resetRes():
        cursor2.execute("drop table RESOURCES")
        createTableinDB()
        con2.commit()
        return 0
    
    def resetMod():
        cursor3.execute("drop table MODSERVERS")
        createTableinDB3
        con3.commit()
        return 0
    
    def setGold(address, ammount):
        if int(ammount) + getCurrentBalance(address) <= 99999999:
                cursor2.execute(f"""update RESOURCES set gold = {ammount} where user_id = {address.id}""")
                return 0
        else:
             cursor2.execute(f"""update RESOURCES set gold = 99999999 where user_id = {address.id}""")
        con.commit()
        return 0

