from pipeline.data import DataFactory
from pipeline.batch_predict import Predictor
import asyncio
from params import *
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

async def main():

    predictor = Predictor(
        requests_filepath=REQUESTS_FILEPATH,
        save_tmp_filepath=SAVE_TMP_FILEPATH,
        request_url=REQUEST_URL,
        api_key=API_KEY,
        max_requests_per_minute=MAX_REQUESTS_PER_MINUTE,
        max_tokens_per_minute=MAX_TOKENS_PER_MINUTE,
        token_encoding_name=TOKEN_ENCODING_NAME,
        max_attempts=MAX_ATTEMPTS,
        logging_level=LOGGING_LEVEL
    )

    # fetch data and structure the conversation file to apply predictions on it
    df = DataFactory().get_bq_data()
    DataFactory().create_requests_file(df,REQUESTS_FILEPATH)

    # predict and save data locally or to GCP
    await predictor.process_api_requests_from_file(request_url=REQUEST_URL)

if __name__ == "__main__":
    # run the async main function
    asyncio.run(main())
