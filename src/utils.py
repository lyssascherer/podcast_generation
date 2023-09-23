import generate_text as gt
import generate_audio as ga
import generate_images as gi
import os
import argparse


 
argParser = argparse.ArgumentParser(description="Just an example",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
argParser.add_argument("-p", "--pagename", action="store_true", help="name of the wikipedia page about the bird")
argParser.add_argument("-s", "--episodeslug", help="unique identifier to identify the episode")

args = argParser.parse_args()
config = vars(args)
print(config)





def main(page_name:str="Common Blackbird", episode_slug="common_blackbird"):
  podcast_name = "Birds are awsome!"
  
  # get text
  input_text = gt.get_page_content_from_wikipedia(page_name)
  texts = gt.split_text_into_documents(input_text)

  # create dialogue
  output_dialogue = gt.create_podcast_dialogue_from_text(input_text, podcast_name, verbose=False)
  podcast_dialogues = output_dialogue["podcast_dialogues"][:3] # TODO: remove this

  # generate episode with voices
  ga.generate_voices(podcast_dialogues, f"audios/episodes/ep_{episode_slug}.mp3")

  # create music for intro if none existent
  if not os.path.isfile("audios/intro_main_song.wav"):
    description = "earthy tones, environmentally conscious, ukulele-infused, harmonic, breezy, easygoing, organic instrumentation, gentle grooves"
    audio = ga.create_audio_sample(description, save_filename="audios/intro_main_song")

  # create sound effect for intro if none existent
  if not os.path.isfile("audios/intro_bird_effect.wav"):
    description = "sounds of birds"
    effects = ga.create_effects_sample(description, save_filename="audios/intro_bird_effect")

  # put intro to episode
  full_episode_audio = ga.add_into_ontro_podcast_audio(f"audios/episodes/ep_{episode_slug}.mp3")
  full_episode_audio.export(f"audios/full_episodes/full_ep_{episode_slug}.mp3", format="mp3")

  # generate podcast cover
  prompt_pop_art = f"Pop art illustration of a {page_name}, comic book-inspired, vivid and contrasting colors, layered composition, retro flair, lively and expressive"
  negative_prompt = "multiple birds, out of frame, lowres, text, error, cropped, worst quality, low quality, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, username, watermark, signature"

  image = gi.generate_cover(prompt_pop_art, negative_prompt) 
  # image save(f"covers/episode_slug.jpg") # TODO: implement


if __name__ == "__main__":

  args = argParser.parse_args()
  print(args.pagename)
  print(args.episodeslug)
  # main()