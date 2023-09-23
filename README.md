# Podcast Generation 

This project generates a podcast episode using different APIs and technologies. The main topic of this podcast is birds so each episode will be about a specific bird. This also means that the prompts were written with this in mind.

## Text Generation

We use [Wikipedia](https://github.com/goldsmith/Wikipedia) library to get the text about a bird, and [Langchain](https://www.langchain.com/) with [Openai](https://openai.com/blog/openai-api) to generate a structured podcast dialogue.

## Audio Generation

We use [ElevenLabs API]() to generate the voices for the podcast. We also create an audio for the podcast intro using [Audiocraft](https://audiocraft.metademolab.com/). This audio is a song generated with [MusicGen](https://audiocraft.metademolab.com/musicgen.html) and some sound effects generated using [AudioGen](https://audiocraft.metademolab.com/audiogen.html). We put everything together using [pydub](https://github.com/jiaaro/pydub) library.

## Image Generation

We use the Stable Diffusion XL model ([stable-diffusion-xl-base-1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)) as a base model and Refiner XL ([stable-diffusion-xl-refiner-1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-refiner-1.0)) as a refiner model to generate a podcast cover.

---

This project was part of the [Uplimit](https://uplimit.com/) course ["Prompt Design & Building AI Products"](https://uplimit.com/course/prompt-design-building-ai-products). You can see the Colab notebooks here:
- [Week 1](https://colab.research.google.com/drive/1Gpms1I9IPV5CWQU0siOZpM19Plf1Xckb?usp=sharing): Geting the text about your podcast topic, generating the podcast dialogue using OpenAI, and generating the voices with Elevenlabs.
- [Week 2](https://colab.research.google.com/drive/1rAzONRFTv062LRN2UuZewT6rfKI-4AoK?usp=sharing): Generating a cover for our podcast using Stable Diffusion XL model with a refiner. In this notebook, I tried different prompts to generate a cover in different art styles.
- [Week 3](https://colab.research.google.com/drive/1Xp4CCsNq9bykQ5nN4knyhtgt_Upvzf1T?usp=sharing): Generating music for the intro using AudioCraft. I also used Langchain to create a sequential chain summarising and generating the podcast dialogue. And the same process using Langchain agents.

