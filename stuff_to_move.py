    recording = check_recording()
    while not recording:
        recording = check_recording()

recording_confirmation_file = 'Record_condition.txt'
recording = False


def check_recording():
    with open(recording_confirmation_file, 'r') as file:
        if file.read() == 'True': return True
    return False


def record_wav():
    # Open a file to write the stream data
    with open(wav_output_file, 'wb') as f:
        # Send a request to get the stream
        with requests.get(wav_url, stream=True) as r:
            start_time = time.time()
            # Read chunks of the stream and write to the file
            for chunk in r.iter_content(chunk_size=1024):
                recording = check_recording()
                # Check if the duration has been reached
                if not recording:
                    break
                f.write(chunk)