from dotenv import load_dotenv
import os 

load_dotenv()

tappaytoken = {
    "TAPPAY_PARTNER_KEY": os.getenv("TAPPAY_PARTNER_KEY"),
    "TAPPAY_API_URL": os.getenv("TAPPAY_API_URL"),
}
