"""
Static version will be coming for testing purposes
Uses postgresql
"""


import psycopg2
from psycopg2.extras import DictCursor


# Creating database
class Database:
    # Constructor
    def __init__(self):
        # Connection parameters
        self.host = "localhost"
        self.database = "postgres"
        self.user = "postgres"
        self.password = "postgres"
        # self.options = "-c search_path=dbo,main"

        # Cursor and connection
        self.conn = None
        self.cursor = None

        # Connecting to the database
        try:
            # Connecting to the database
            self.conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                # options=self.options
            )

            # Setting the cursor
            self.cursor = self.conn.cursor(cursor_factory=DictCursor)

            # Printing version
            print("PostgreSQL version: ")
            self.cursor.execute("SELECT version()")
            print(self.cursor.fetchone())

        # Any connection errors
        except Exception as e:
            print(f"[DB ERROR] {e}")

    # Check if user exists
    def checkIfUserExists(self, email) -> bool:
        """
        :param email:
        :return bool:
        """

        # Using connection
        with self.conn:
            # Query and params
            query = "SELECT 1 FROM users WHERE email = %s"
            params = (email,)

            # Execution
            self.cursor.execute(query, params)

            # Checking
            if self.cursor.fetchone() is None:
                return False
            return True

    # Creating Id for the user
    def checkIfIdExists(self, ID) -> bool:
        """
        :param ID:
        :return bool:
        """

        # Connection
        with self.conn:
            # Query and params
            query = "SELECT 1 FROM USERS WHERE id = %s"
            params = (ID,)

            # Execution
            self.cursor.execute(query, params)

            if self.cursor.fetchone() is None:
                return False
            return True

    # Gets password from users table
    def getPassword(self, email) -> str or None:
        """
        :param email:
        :return self.cursor.fetchone():
        """

        # Checking is email exists
        exists = self.checkIfUserExists(email=email)
        if exists:
            # Using connection
            with self.conn:
                # Query and params
                query = "SELECT * FROM users WHERE email = %s"
                params = (email,)

                # Execution
                self.cursor.execute(query, params)
                return self.cursor.fetchone()['password']

        else:
            return None

    # Gets all of users content
    def getAllFromUser(self, email) -> str:
        """
        :param email:
        :return self.cursor.fetchone: str
        """

        with self.conn:
            # Query and params
            query = "SELECT * FROM users WHERE email = %s"
            params = (email,)

            # Execution
            self.cursor.execute(query, params)
            return self.cursor.fetchone()

    # Adds user to the users table
    def addUser(self, email, password, userType, ID, salt) -> None:
        """
        :param email:
        :param password:
        :param userType:
        :param ID:
        :return None:
        """

        # Using connection
        with self.conn:
            # Query and params
            query = "INSERT INTO users (email, password, user_type, id, salt) VALUES (%s, %s, %s, %s, %s)"
            params = (email, password, userType, ID, salt)

            # Execution
            self.cursor.execute(query, params)

    # Deletes a user from the users table
    def deleteUser(self, email) -> bool:
        """
        :param email:
        :return exists:
        """

        try:
            # Using connection
            with self.conn:
                # Query an params
                query = "DELETE FROM users WHERE email = %s"
                params = (email,)

                # Execution
                self.cursor.execute(query, params)
                return True

        # Any errors
        except Exception as e:
            print(f"[DB ERROR] {e}")
            return False

    def getIDFromEmail(self, email) -> str:
        """
        :param email:
        :return self.cursor.fetchone(): str:
        """

        # Connection
        with self.conn:
            # Query and parameters
            query = "SELECT id FROM users WHERE email = %s"
            params = (email,)

            # Execution
            self.cursor.execute(query, params)

            return self.cursor.fetchone()

    # Update email from the users table
    def updateEmail(self, ID, newEmail) -> bool:
        """
        :param ID:
        :param newEmail:
        :return bool:
        """

        try:
            # Using connection
            with self.conn:
                # Query and params
                query = "UPDATE users SET email = %s WHERE ID = %s"
                params = (newEmail, ID)

                # Execution
                self.cursor.execute(query, params)
                return True

        # Any errors
        except Exception as e:
            print(f"[DB ERROR] {e}")
            return False

    # Update password
    def updatePassword(self, email, newPassword) -> bool:
        """
        :param email:
        :param newPassword:
        :return bool:
        """

        try:
            # Using connection
            with self.conn:
                # Query and params
                query = "UPDATE users SET password = %s WHERE email = %s"
                params = (email, newPassword)

                # Execution
                self.cursor.execute(query, params)

        # Any errors
        except Exception as e:
            print(f"[DB ERROR] {e}")
            return False

    # Update user type (i.e Admin, user, etc.)
    def updateUserType(self, email, userType) -> bool:
        """
        :param email:
        :param userType:
        :return bool:
        """

        try:
            # Using the connection
            with self.conn:
                # Query and params
                query = "UPDATE users SET user_type = %s WHERE email = %s"
                params = (userType, email)

                # Execution
                self.cursor.execute(query, params)
                return True

        # Any errors
        except Exception as e:
            print(f"[DB ERROR] {e}")
            return False

    # Closes the connection between the server
    def closeConnection(self) -> None:
        # Closes the connection
        self.conn.close()

    # Reconnect to the server
    def reconnect(self, reconnectAmount) -> bool:
        # Loop until the reconnect amount
        for reconnect in range(reconnectAmount):
            # Connecting to the database
            try:
                # Connecting to the database
                self.conn = psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                    # options=self.options
                )

                # Setting the cursor
                self.cursor = self.conn.cursor(cursor_factory=DictCursor)
                return True

            # Any errors
            except Exception as e:
                print(f"[DB RECONNECT ERROR] {e}")

                # If has reached connection attempt
                if reconnect == reconnectAmount:
                    raise Exception("[FATAL DB ERROR] Reached max reconnect attempts and failed to connect")

        return False