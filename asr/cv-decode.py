import pandas as pd
import aiohttp
import asyncio
import time
import os

def rmdir(directory):
    directory=Path(directory)
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()
    directory.rmdir()
# Assuming the Flask API is running locally on port 5000
ASR_API_URL = 'http://localhost:8001/asr'

# Path to the directory where audio files are stored
AUDIO_FILES_DIRECTORY = ''

# Read the CSV file into a DataFrame
df = pd.read_csv('cv-valid-dev.csv')

# Semaphore to limit the number of concurrent connections
CONNECTION_SEMAPHORE = asyncio.Semaphore(15) # currently set at 15 concurrent jobs

# Asynchronous function to get transcription and duration
async def get_transcription_and_duration(session, audio_file_path):
    async with CONNECTION_SEMAPHORE, session.post(ASR_API_URL, data={'file': open(audio_file_path, 'rb')}) as response:
        if response.status == 200:
            json_response = await response.json()
            print(audio_file_path+"completed")
            return audio_file_path, json_response['duration'],json_response['transcription'].lower()
        else:
            response_text = await response.text()
            print(f"Error processing {audio_file_path}: {response_text}")
            return None, None

# Asynchronous function to process all files
async def process_files():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for filename in df['filename']:
            audio_file_path = filename
            task = asyncio.create_task(get_transcription_and_duration(session, audio_file_path))
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        df2 = pd.DataFrame(results, columns=['filename', 'duration', 'generated_text'])
        df3=pd.merge(df,df2, on='filename', how='left')
        df3.to_csv('output.csv', index=False)


# Run the asynchronous function

asyncio.run(process_files())

try:
    rmdir(Path("./cv-valid-dev"))
    os.remove("./cv-valid-dev.csv")
except:
    pass
print("completed")
