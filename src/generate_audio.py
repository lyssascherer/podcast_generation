
import requests

from pydub import AudioSegment
from audiocraft.models import MusicGen
from audiocraft.utils.notebook import display_audio
from audiocraft.data.audio import audio_write
from audiocraft.models import AudioGen

from dotenv import load_dotenv, find_dotenv
import os
_ = load_dotenv(find_dotenv())  # read local .env file
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")


def generateVoiceFrom11(input_text:str, speakerChoice:str):
  """Generate voices for a speaker given a text using elevenlabs API."""
  api_endpoint = "https://api.elevenlabs.io/v1/text-to-speech/" + speakerChoice
  headers = { "xi-api-key": ELEVENLABS_API_KEY}
  body = {"text": input_text, "voice_settings": {"stability": 0, "similarity_boost": 0 } }
  response = requests.post(api_endpoint, headers=headers, json=body)
  return response


def generate_voices(podcast_dialogues:dict, filename:str):
  """Text-to-speech: generate the voices for the whole dialogue and concatenate them in one audio file."""
  speakers_voices = {"Mark": {"name":"Jeremy", "voice_id":"bVMeCyTHy58xNoL34h3p"}, "Anna": {"name":"Glinda", "voice_id":"z9fAnlkpzviPz146aGWa"}}
  generated_voices = []
  for dialogue_line in podcast_dialogues:
    generated_voice = generateVoiceFrom11(input_text=dialogue_line["speaker_text"], speakerChoice=speakers_voices[dialogue_line["speaker_name"]]["voice_id"])
    generated_voices.append(generated_voice.content)

    with open(filename, "wb") as f:
        for voice_dialogue in generated_voices:
            f.write(voice_dialogue)


def generate_musics_sample_from_descriptions(descriptions:list[str], duration=30):
  """Generate different sounds for the intro of the podcast using a list of prompts. 
  We use te MusicGen from AudioCraft to generate the sound."""
  model_music_gen = MusicGen.get_pretrained('facebook/musicgen-small')
  model_music_gen.set_generation_params(
      use_sampling=True,
      top_k=250,
      duration=duration
  )
  output_music = model_music_gen.generate(
    descriptions=descriptions,
    progress=True,
    return_tokens=True
  )
  for i, description in enumerate(descriptions):
    print(f"\nPrompt audio {i}: {description}")
    display_audio(output_music[0][i], sample_rate=32000)
  return output_music[0]


def generate_audio_effects(descriptions:list[str]):
  """Generate different effects for the intro of the podcast using a list of prompts. 
  We use te AudioGen from AudioCraft to generate the sound effects."""
  model_effects = AudioGen.get_pretrained('facebook/audiogen-medium')
  model_effects.set_generation_params(
    use_sampling=True,
    top_k=250,
    duration=5
  )

  output_effects = model_effects.generate(
    descriptions=descriptions,
    progress=True
  )
  for i, description in enumerate(descriptions):
    print(f"\nPrompt audio {i}: {description}")
    display_audio(output_effects[i], sample_rate=16000)
  return output_effects


def create_audio_sample(description:str, save_filename:str=None):
    """Generate a music for intro using a text prompt and MusicGen model."""
    audio = generate_musics_sample_from_descriptions([description], duration=15)[0]
    if save_filename:
        audio_write(save_filename, audio.cpu(), sample_rate=32000)
    return audio


def create_effects_sample(description:str, save_filename:str=None):
    """Generate a sound effect for intro using a text prompt and AudioGen model."""
    effect = generate_audio_effects([description])[0]
    if save_filename:
        audio_write(save_filename, effect.cpu(), sample_rate=16000)
    return effect


def add_into_ontro_podcast_audio(podcast_audio_file:str):
  """Generate a unique audio with the intro song + podcast episode. 
  The intro song is the sound generated with the audio effects on the backkground.
  We also add some smooth transition."""
  intro_music_file = "audios/intro_main_song.wav"
  audio_effect_file = "audios/intro_bird_effect.wav"

  # Import your respective saved MP3 files
  music_intro = AudioSegment.from_wav(intro_music_file)[:15 * 1000]
  effects_intro = AudioSegment.from_wav(audio_effect_file)
  podcast_episode = AudioSegment.from_mp3(podcast_audio_file).apply_gain(+4.5)

  music_intro_with_bird_effect = music_intro.overlay(effects_intro, loop=True, times=5, gain_during_overlay=3)
  final_music_intro = music_intro_with_bird_effect.append(effects_intro, crossfade=1500)
  final_music_intro = final_music_intro.fade_in(duration=1000)
  full_episode = final_music_intro + podcast_episode + music_intro_with_bird_effect.fade_in(duration=1000)
  return full_episode