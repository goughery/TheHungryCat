import sys
sys.path.insert(0, sys.path[0]+'/Modules')
import pymysql
import datetime

def makeConnection():
    try:
        conn = pymysql.connect('jeffdb.c8gaccabupfm.us-east-1.rds.amazonaws.com', user='lambdauser', passwd='dRt4#98Uknd', db='CatFed', connect_timeout=5, cursorclass=pymysql.cursors.DictCursor)
        return conn
   
    except:
        return "Connection Fail"
        #print("connection fail")

def add_increment_userDB(session):
    increment = 1
    #add or increment user
    #if the user doesn't exist, add the user to the database with a session count of 1
    #if the user already exists, add 1 to the session count of the user
    #should be added to the beginning of every session
    conn = makeConnection()

    userID = session['user']['userId']
    getUserSQL = "SELECT UserID, SessionCount FROM CatFed.Users WHERE UserID = '" + userID + "'"
    nowtime = datetime.datetime.now()# - datetime.timedelta(hours=4)
    newUserSQL = "INSERT INTO CatFed.Users(UserID, SessionCount, LastDate) VALUES('%s',1,'%s')" %(userID, nowtime)
    
    #userID = 'testuser123'
    
    with conn.cursor() as cur:
        cur.execute(getUserSQL)
        result = cur.fetchall()  #returns ['{UserIDKey':18, 'SessionCount': 3}]
        conn.commit()
        if len(result) == 0:
            cur.execute(newUserSQL)
            conn.commit()
            userAdded = 1
        else:
            currentSessionCount = result[0]["SessionCount"]
            #existingUserSQL = "UPDATE spelling.Users SET SessionCount = "+ str(currentSessionCount + 1) + " WHERE UserID = '" + userID + "'"
            existingUserSQL = """Update CatFed.Users
                                 SET SessionCount = %s, LastDate = '%s'
                                 WHERE UserID = '%s'""" %(currentSessionCount+increment, nowtime, userID)
            cur.execute(existingUserSQL)
            conn.commit()
            userAdded = 0
        #cur.close()
    cur.close()
    conn.commit()
    conn.close()
    #del cur
#userAdded

def make_Catdb(session, catname):
    userID = session['user']['userId']
    conn = makeConnection()
    
    makeCatSQL = """INSERT INTO CatFed.Cats (UserID, CatName)
                    VALUES ('%s', '%s')""" %(userID, catname)
    
    try:
        with conn.cursor() as cur:
            cur.execute(makeCatSQL)
            conn.commit()
        success = 1
    except pymysql.IntegrityError as e:
        success = 0

        
    cur.close()
    conn.commit()
    conn.close()
    return success

def check_lastDateTime(session, catname):
    #checks when the cat was last fed
    userID = session['user']['userId']
    conn = makeConnection()
    
    getLastDateSQL = """SELECT FedDateTime
                         FROM CatFed.Cats WHERE UserID = '%s' and CatName = '%s'""" %(userID, catname)
    with conn.cursor() as cur:
        cur.execute(getLastDateSQL)
        lastDate = cur.fetchall()[0]['FedDateTime']
        conn.commit()
        
    cur.close()
    conn.commit()
    conn.close()
    
    return lastDate

def feed_catdb(session, catname):
    userID = session['user']['userId']
    conn = makeConnection()
    nowtime = datetime.datetime.now()
    updateCatSQL = """UPDATE CatFed.Cats SET FedDateTime = '%s'
                      WHERE UserID = '%s' and CatName = '%s'""" %(nowtime, userID, catname)
    
    with conn.cursor() as cur:
        cur.execute(updateCatSQL)
        conn.commit()
        
    cur.close()
    conn.commit()
    conn.close()
     
    
def check_catsdb(session):
    userID = session['user']['userId']
    conn = makeConnection()
    checkCatsSQL = """SELECT CatName from CatFed.Cats WHERE UserID = '%s'""" %(userID)
    
    with conn.cursor() as cur:
        cur.execute(checkCatsSQL)
        cats = cur.fetchall()
        conn.commit()
        
    cur.close()
    conn.commit()
    conn.close()
    return cats
    
def check_onecatdb(session, catname):
    userID = session['user']['userId']
    conn = makeConnection()
    checkCatsSQL = """SELECT CatName from CatFed.Cats WHERE UserID = '%s' and CatName = '%s'""" %(userID, catname)
    
    with conn.cursor() as cur:
        cur.execute(checkCatsSQL)
        cats = cur.fetchall()
        conn.commit()
        
    cur.close()
    conn.commit()
    conn.close()
    return cats
    
    
def set_paidDB(session, paid):
    userID = session['user']['userId']
    conn = makeConnection()
    setPaidSQL = """UPDATE CatFed.Users SET Purchased = %s WHERE UserID = '%s'""" %(paid, userID)
    with conn.cursor() as cur:
        cur.execute(setPaidSQL)
        conn.commit()
        
    cur.close()
    conn.commit()
    conn.close()

def get_paidDB(session):
    #find out if the user is paid
    #returns 1 or 0
    userID = session['user']['userId']
    conn = makeConnection()
    getPaidSQL = """SELECT COALESCE(Purchased, 0) as Purchased
                         FROM CatFed.Users WHERE UserID = '%s'""" %(userID)
    with conn.cursor() as cur:
        cur.execute(getPaidSQL)
        paid = cur.fetchall()[0]['Purchased']
        
        conn.commit()
        
    cur.close()
    conn.commit()
    conn.close()
    
    return paid

def remove_Catdb(session, catname):
    userID = session['user']['userId']
    conn = makeConnection()
    removeSQL = """DELETE FROM CatFed.Cats WHERE UserID = '%s' AND CatName = '%s'""" %(userID, catname)
    with conn.cursor() as cur:
        cur.execute(removeSQL)
        conn.commit()
        
    cur.close()
    conn.commit()
    conn.close()