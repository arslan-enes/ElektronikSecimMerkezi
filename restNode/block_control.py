import mysql.connector
import hashlib
import sys

def encrypt_string(data):
    sha_signature = hashlib.sha256(data.encode()).hexdigest()
    return sha_signature


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="tutorial"
)

def hash_kontrol():
    imlec = mydb.cursor()
    sql = "SELECT data from blockchain"
    imlec.execute(sql)

    SONUC = True

    datalar = imlec.fetchall()
    datas = []

    for x in datalar:
        x = str(x)
        x = x[2:-3]
        datas.append(x)


    sql = "SELECT hash from blockchain"
    imlec.execute(sql)

    hashler = imlec.fetchall()
    hashes = []

    for x in hashler:
        x = str(x)
        x = x[2:-7]
        hashes.append(x)

    for x in range(len(hashes)):
        if encrypt_string(datas[x])!=hashes[x]:
            SONUC = False
            sql = "UPDATE blockchain SET hash = '"+encrypt_string(datas[x])+ "' , security = 0 where id = "+ str(x+1)
            imlec.execute(sql) 
        if not SONUC:
            sql = "UPDATE blockchain SET security = 0 where id >" + str(x+1)
            imlec.execute(sql)


    mydb.commit()
    if SONUC==False:
        print("Blockchain hatali.")
    else:
        print("Blockchain guvenli.")
    sys.stdout.flush()
    return

hash_kontrol()