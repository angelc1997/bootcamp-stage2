from dotenv import load_dotenv
import os 

load_dotenv()

tokenconfig = {
    "SECRET_KEY": os.getenv("SECRET_KEY"),
    "ALGORITHM": os.getenv("ALGORITHM"),
    "ACCESS_TOKEN_EXPIRE_DAYS": 7
}
