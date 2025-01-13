from helper import execute_sql_file, scrape_reddit, scrape_twitter
import logging
from dotenv import load_dotenv
import schedule
import time

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_tasks():
    try:
        # Create Database Tables if it does not exist
        logging.info("Starting: Create Database Tables")
        execute_sql_file(file_path="sql/CreateTables.sql")
        logging.info("Completed: Create Database Tables")

        # Scrape Reddit
        logging.info("Starting: Scrape Reddit")
        subreddits = ["wallstreetbets", "CryptoMoonShots"]
        scrape_reddit(subreddits=subreddits)
        logging.info("Completed: Scrape Reddit")

        # Scrape Twitter
        logging.info("Starting: Scrape Twitter")
        twitter_keyword = "bitcoin"
        scrape_twitter(twitter_keyword=twitter_keyword)
        logging.info("Completed: Scrape Twitter")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Schedule tasks every 10 minutes
schedule.every(10).seconds.do(run_tasks)

if __name__ == "__main__":
    logging.info("Scheduler started.")
    while True:
        schedule.run_pending()
        time.sleep(1)  # Wait a second before checking the schedule again











