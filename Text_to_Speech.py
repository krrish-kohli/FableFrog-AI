import os
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment

# Ensure the API key is set
ELEVENLABS_API_KEY = "sk_f295af66b75bdacfdcda54f33759fcf804bed01b0abd7847"
if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

voice_id_male = "pqHfZKP75CvOlQylNhV4"
voice_id_female = "AZnzlk1XvdvUeBnXmlldc"
voice_id = voice_id_male

def text_to_speech_file(text: str) -> str:
    # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        voice_id=voice_id, # Adam pre-made voice
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2", # use the turbo model for low latency, for other languages use the ⁠ eleven_multilingual_v2 ⁠
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    # Generating a unique file name for the output MP3 file
    # save_file_path = "speech.mp3"
    save_file_path = "speech2.mp3"

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:


        for chunk in response:
            if chunk:
                f.write(chunk)

    print(save_file_path)

    print(f"{save_file_path}: A new audio file was saved successfully!")

    # Verify the file can be opened with pydub
    try:
        AudioSegment.from_mp3(save_file_path)
        print("MP3 file verified successfully!")
    except Exception as e:
        print(f"Error verifying MP3 file: {e}")

    # Return the path of the saved audio file
    return save_file_path

# Test the text_to_speech_file function with a sample text
sample_text = "Hello there, nice seeing you, I am so happy to see you, how have you been doing today?"
mp3_file_path = text_to_speech_file(sample_text)

# Verify that the MP3 file was created correctly
if os.path.exists(mp3_file_path):
    print(f"The file {mp3_file_path} exists and was created successfully.")
else:
    print(f"Failed to create the file {mp3_file_path}.")