import dotenv
import os

dotenv.load_dotenv()


MYSQL_URL = os.getenv(
    "MYSQL_URL", "mysql+mysqlconnector://root:aslon2001@localhost:3306/employer"
)
SQLITE_URL = os.getenv("SQLITE_URL", "sqlite:///./employer.db")
DATABASE_NAME = os.getenv("DATABASE_NAME", "employer")
SECRET_KEY = os.getenv("SECRET", "your-256-bit-secret")
