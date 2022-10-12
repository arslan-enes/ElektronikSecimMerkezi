from hashlib import blake2b,sha256,sha512,blake2s,sha1
import base64
from Crypto import Random
from Crypto.Cipher import AES,DES
import sys
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="tutorial"
)

def encrypt_string():
    sha_signature = sha256(sys.argv[1].encode()).hexdigest()
    print(sha_signature)


def prevHashEkleme():
    imlec = mydb.cursor()
    hash = ''

    sql3 = "SELECT id from blockchain"
    imlec.execute(sql3)

    idler = imlec.fetchall()
    ids = []

    for x in idler:
        x = str(x)
        ids.append(x)

    sonID = ids[-1][1:-2]

    sql = "SELECT hash from blockchain"
    imlec.execute(sql)

    hashs = []

    sonuc = imlec.fetchall()

    for x in sonuc:
        x = str(x)
        hash = x[2:-7]
        hashs.append(hash)
    
    hash = hashs[-2]

    sql2 = "UPDATE blockchain SET prevHash = ' " + hash + " 'where id= " + sonID
    imlec.execute(sql2)
    mydb.commit()
    
    return

class sifrelemeYontemleri:
    def __init__(self):
        self.key = ""
        self.bs = ""
        pass
    def blake2b_sifreleme(self,string):
        """def blake2b_sifreleme() : 1 ile 64 bit arasinda herhangi bir boyutta sifreler uretir.\n .blake2b_sifreleme(str) seklinde yazilir"""
        return blake2b(string.encode()).hexdigest()

    def sha256_sifreleme(self,string):
        """def sha256_sifreleme() : Girilen verileri 32 byte boyutunda sifrelemektedir..\n .sha256_sifreleme(str) seklinde yazilir"""
        return sha256(string.encode()).hexdigest()

    def sha512_sifreleme(self,string):
        """def sha512_sifreleme() : Girilen verileri 512 bit boyutunda sifrelemektedir..\n .sha512_sifreleme(str) seklinde yazilir"""
        return sha512(string.encode()).hexdigest()
        
    def blake2s_sifreleme(self,string):
        """def blake2s_sifreleme() : 1 ile 32 bayt arasinda herhangi bir boyutta sifreler uretir.\n .blake2s_sifreleme(str) seklinde yazilir"""
        return blake2s(string.encode()).hexdigest()

    def sha1_sifreleme(self,string):
        """def sha1_sifreleme() : 20 byte boyutta sifreler uretir.\n .sha1_sifreleme(str) seklinde yazilir"""
        return sha1(string.encode()).hexdigest()

    def AES_pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
    
    def AES_sifreleme(self,key,string):
        """def AES_sifreleme() : Verilen anahtar ile verilen ifadeyi sifreler.\n .AES_sifreleme(key,str) seklinde yazilir"""
        self.bs = AES.block_size
        self.key = sha256(key.encode()).digest()
        try:
            raw = self.AES_pad(string)
        except:
            print("Exception meydana geldi.")
        finally:
            iv = Random.new().read(AES.block_size)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def DES_sifreleme(self,key,string):
        """def DES_sifreleme() : Verilen anahtar ile verilen ifadeyi sifreler.\n .DES_sifreleme(key,str) seklinde yazilir"""
        des = DES.new(key, DES.MODE_ECB)
        padded_text = self.DES_pad(string)
        encrypted_text = des.encrypt(padded_text)
        return encrypted_text
    
    def DES_pad(self,text):
        n = len(text) % 8
        return text + (b' ' * n)

def kelimedondur(string):
        return string.split()

class DilKontrolSinifi:
    def __init__(self,string):
        self.string = string
        self.CUMLE = self.cumleSayisi()
        self.KELIME = self.kelimeSayisi()
        self.SESLIHARF = self.sesliHarfSayisi()
        self.BUYUKUNLU = self.buyukUnluUyumu()
        print("Cumle Sayisi: "+str(self.CUMLE))
        print("Kelime Sayisi: "+str(self.KELIME))
        print("Sesli Harf Sayisi: "+str(self.SESLIHARF))
        print("Buyuk Unlu Uyumuna Uyan ve Uymayan Kelime Sayisi: "+str(self.BUYUKUNLU))
        pass

    def cumleSayisi(self):
        """def cumleSayisi() : Verilen string ifadenin cumle sayisini donduren fonksiyon.\n .cumleSayisi(str) seklinde yazilir"""
        myList = [x for x in self.string]
        cumleSonu = ['.','?','!']
        cumle = 0
        for x,y in enumerate(myList):
            if y in cumleSonu and x<len(myList)-2 and myList[x+2].isupper():
                cumle+=1
        if myList[-1] in cumleSonu:
            cumle+=1
        return cumle

    def kelimeSayisi(self):
        """def kelimeSayisi() : Verilen string ifadenin kelime sayisini donduren fonksiyon.\n .kelimeSayisi(str) seklinde yazilir"""
        string = self.string.split()
        self.KELIME = len(string)
        return len(string)

    def sesliHarfSayisi(self):
        """def sesliHarfSayisi() : Verilen string ifadenin sesli harf sayisini donduren fonksiyon.\n .sesliHarfSayisi(str) seklinde yazilir"""
        sesliler = ['a','e','ı','i','u','ü','o','ö','i̇']
        myList = [x for x in self.string]
        sesliHarf = 0
        for x,y in enumerate(myList):
            if myList[x].lower() in sesliler:
                sesliHarf += 1
        return sesliHarf

    def buyukUnluUyumu(self):
        """def buyukUnluUyumu() : Verilen string ifadenin buyuk unlu uyumuna uyan ve uymayan kelimelerin sayisini donduren fonksiyon.\n .buyukUnluUyumu(str) seklinde yazilir"""
        uyumlular=0
        uyumsuzlar=0
        try:
            kelimeler = kelimedondur(self.string)
        except:
            print("Exception meydana geldi.")
        finally:
            kalin_unluler = list("aıouAIOU") # veya ['a', 'ı', 'o', 'u'] 
            ince_unluler = list("eiöüEİOU") # veya ['e', 'i', 'ö', 'ü']
            for kelime in kelimeler:
                if (sum(kelime.count(kalin) for kalin in kalin_unluler)) != 0 and (sum(kelime.count(ince) for ince in ince_unluler)) != 0:
                    uyumsuzlar+=1
                else:
                    uyumlular+=1
            self.BUYUKUNLU = (uyumlular,uyumsuzlar)
            return(uyumlular,uyumsuzlar)

class Help(DilKontrolSinifi,sifrelemeYontemleri):
    def __init__(self):
        print('''        Modulumuzun iceriginde dil bilgisi islemler yapan DilKontrolSinifi ve
        sifreleme islemeri yapan sifrelemeYontemleri sinifi bulunmaktadır.
        Detaylı bilgi helper.(fonksiyonAd)_Help() seklinde elde edilebilir''')
        pass
    def cumleSayisi_Help(self):
        print(help(self.cumleSayisi))

    def kelimeSayisi_Help(self):
        print(help(self.kelimeSayisi))

    def sesliHarfSayisi_Help(self):
        print(help(self.sesliHarfSayisi))

    def buyukUnluUyumu_Help(self):
        print(help(self.buyukUnluUyumu))

    def sha1_Help(self):
        print(help(self.sha1_sifreleme))

    def sha256_Help(self):
        print(help(self.sha256_sifreleme))

    def sha512_Help(self):
        print(help(self.sha512_sifreleme))

    def blake2b_Help(self):
        print(help(self.blake2b_sifreleme))

    def blake2s_Help(self):
        print(help(self.blake2s_sifreleme))

    def AES_Help(self):
        print(help(self.AES_sifreleme))

    def DES_Help(self):
        print(help(self.DES_sifreleme))

if __name__ == "__main__":
    helper = Help()
    helper.sha256_Help()
else:
    prevHashEkleme()

