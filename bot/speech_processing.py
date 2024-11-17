import speech_recognition as sr
from gtts import gTTS
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
from pydub import AudioSegment
model_name = "facebook/blenderbot-400M-distill"  
tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
model = BlenderbotForConditionalGeneration.from_pretrained(model_name)
def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(file_path)
    wav_path = file_path.replace('.wav', '_converted.wav')
    audio.export(wav_path, format='wav')

    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    return text
def generate_response(user_input, conversation_history=None):
    inputs = tokenizer(user_input, return_tensors="pt")
    reply_ids = model.generate(**inputs)
    response = tokenizer.decode(reply_ids[0], skip_special_tokens=True)
    return response


def text_to_speech(text, output_file):
    tts = gTTS(text=text, lang='en')
    tts.save(output_file)
