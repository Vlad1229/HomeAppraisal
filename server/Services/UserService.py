import psycopg2
import jwt
import hashlib
from Services.Service import Service


class UserService(Service):
    def user_is_admin(self, token):
        decoded = jwt.decode(token, "Secret", algorithms=['HS256'])
        query = "select * from users where \"Id\" = %s"

        cursor = self.conn.cursor()
        try:
            cursor.execute(query, (decoded["id"],))
            rows = cursor.fetchall()
            if cursor.rowcount == 1:
                for row in rows:
                    return row[4]

            return False
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            cursor.execute("rollback")
            return False
        finally:
            cursor.close()

    @staticmethod
    def get_user_id(token):
        return jwt.decode(token, "Secret", algorithms=['HS256'])["id"]

    def auth_user(self, nickname, password):
        query = "select * from users where \"Nickname\" = %s"

        cursor = self.conn.cursor()
        try:
            cursor.execute(query, (nickname,))
            rows = cursor.fetchall()
            token = None
            is_admin = False
            if cursor.rowcount == 1:
                for row in rows:
                    hash_object = hashlib.sha1(bytes(password, 'utf-8'))
                    hashed_password = hash_object.hexdigest()
                    if hashed_password == row[3]:
                        token = jwt.encode({"id": row[0]}, "Secret", algorithm='HS256')
                        is_admin = row[4]

            return {"token": token, "isAdmin": is_admin}
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            cursor.execute("rollback")
            return None
        finally:
            cursor.close()

    def add_user(self, user_id, email, password, is_admin):
        query = "insert into users (\"Nickname\", \"Email\", \"Password\", \"IsAdmin\") values(%s,%s,%s,%s)"

        cursor = self.conn.cursor()
        try:
            hash_object = hashlib.sha1(bytes(password, 'utf-8'))
            hashed_password = hash_object.hexdigest()

            cursor.execute(query, (user_id, email, hashed_password, is_admin))
            self.conn.commit()
            cursor.close()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            cursor.execute("rollback")
            cursor.close()
            return False
