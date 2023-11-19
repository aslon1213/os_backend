import dotenv
import os

dotenv.load_dotenv()


MYSQL_URL = os.getenv(
    "MYSQL_URL", "mysql+mysqlconnector://root:aslon2001@localhost:3306/employer"
)
DATABASE_NAME = os.getenv("DATABASE_NAME", "employer")
SECRET = os.getenv("SECRET", "blablabalbalabla")
