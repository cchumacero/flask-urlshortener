from database.db import get_connection
from .entities.Shorturl import Shorturl

class ShorturlModel():

    @classmethod
    def get_urls(self):
        try:
            connection=get_connection()
            urls=[]

            with connection.cursor() as cursor:
                cursor.execute("SELECT id, original_url, short_url FROM urls")
                resultset=cursor.fetchall()

                for row in resultset:
                    url=Shorturl(row[0], row[1], row[2])
                    urls.append(url.to_JSON())
            
            connection.close()
            return urls
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_shorturl(self, url):
        try:
            connection=get_connection()

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM urls WHERE original_url = %s", (url,))
    
                row=cursor.fetchone()

                url=None
                if row is not None:
                    url=Shorturl(row[0], row[1], row[2])

            
            connection.close()
            if url is not None:
                return url.to_JSON()
            else: 
                return url
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def create_shorturl(self, url):
        try:
            connection=get_connection()

            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO urls (original_url) VALUES (%s)", (url,))
                
                connection.commit()
            
            connection.close()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_shorturl(self, url):
        try:
            connection=get_connection()

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM urls WHERE original_url = %s", (url,))
    
                row=cursor.fetchone()

                url=None
                if row is not None:
                    url=Shorturl(row[0], row[1], row[2])

            
            connection.close()
            if url is not None:
                return url.to_JSON()
            else: 
                return url
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_originalUrl(self, index):
        print(index)
        try:
            connection=get_connection()

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM urls WHERE id = %s", (index,))
    
                row=cursor.fetchone()

                url=None
                if row is not None:
                    url=row[1]

            
            connection.close()
            if url is not None:
                return url
        except Exception as ex:
            raise Exception(ex)
        