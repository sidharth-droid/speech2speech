from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .speech_processing import transcribe_audio, generate_response, text_to_speech
import os
from django.conf import settings
from django.shortcuts import render
import logging
import speech_recognition as sr
def index(request):
    return render(request, 'index.html')
@csrf_exempt
def process_audio(request):
    if request.method == 'POST':
        audio_file = request.FILES['audio']
        audio_path = os.path.join(settings.MEDIA_ROOT, 'input_audio.wav')
        with open(audio_path, 'wb') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)
        logging.info(f"Audio file saved to {audio_path}")

        try:
            transcribed_text = transcribe_audio(audio_path)
            logging.info(f"Transcribed text: {transcribed_text}")
            
            response_text = generate_response(transcribed_text)
            audio_output_path = os.path.join(settings.MEDIA_ROOT, 'response.mp3')
            
            text_to_speech(response_text, audio_output_path)
            
            return JsonResponse({'audio_url': f'/media/response.mp3'})

        except:
            # logging.error("Speech recognition could not understand audio.")
            # return JsonResponse({'error': 'Could not understand audio, please try again.'}, status=400)
            error_response_text = "Sorry, I could not hear. Please say again."
            error_audio_output_path = os.path.join(settings.MEDIA_ROOT, 'error_response.mp3')
            
            text_to_speech(error_response_text, error_audio_output_path)
            
            return JsonResponse({'audio_url': f'/media/error_response.mp3'}, status=400)
            
        

    return JsonResponse({'error': 'Invalid request'}, status=400)
def cleanup_audio_files():
    media_root = settings.MEDIA_ROOT
    for filename in os.listdir(media_root):
        if filename.endswith('.wav') or filename.endswith('.mp3'):
            os.remove(os.path.join(media_root, filename))