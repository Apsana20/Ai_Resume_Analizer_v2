import sqlite3
import bcrypt



def register_user(name, email, password):

    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    )

    try:
        cursor.execute(
            """
            INSERT INTO users(name,email,password)
            VALUES(?,?,?)
            """,
            (name, email, hashed_password)
        )

        conn.commit()
        conn.commit()
        print("User registered successfully")

    except Exception as e:
        return str(e)

    conn.close()

    return True
def login_user(email, password):
    
    import os
    print(os.path.abspath("database/users.db"))
    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT email FROM users")
   
    cursor.execute(
     "SELECT password FROM users WHERE email=?",
    (email,)
)

    user = cursor.fetchone()
   
    conn.close()

    if user:

      stored_password = user[0]
      
      

      if isinstance(stored_password, str):
         stored_password = stored_password.encode('utf-8')

      if bcrypt.checkpw(
         password.encode('utf-8'),
         stored_password
      ):
         return True

    return False