from gtts import gTTS
from pydub import AudioSegment
import os 

def split_text(podcast_text):
    splitted_text = podcast_text.strip().split("\n")

    parsed_lines = []

    for line in splitted_text:
        if line.startswith("Speaker 1:"):
            parsed_lines.append(("Speaker 1", line.replace("Speaker 1:", "").strip()))
        elif line.startswith("Speaker 2:"):
            parsed_lines.append(("Speaker 2", line.replace("Speaker 2:", "").strip()))
        else:
            print(f"Skipping malformed line {line}")
    return parsed_lines
            

def turn_to_voice(podcast_text, output_file="final_podcast.mp3"):
    

    speaker_langs = {
        "Speaker 1": "en",
        "Speaker 2": "en-uk"
    }

    lines = split_text(podcast_text=podcast_text)
    audio_segments = []

    for i, (speaker, text) in enumerate(lines):
        lang = speaker_langs.get(speaker, "en")

        tts = gTTS(text=text, lang=lang)
        filename = f"segment_{i}.mp3"
        tts.save(filename)

        segment = AudioSegment.from_mp3(filename)
        audio_segments.append(segment)

    # Merge all audio
    final_audio = sum(audio_segments)
    final_audio.export(output_file, format="mp3")

    for i in range(len(lines)):
        os.remove(f"segment_{i}.mp3")

    print(f"Podcast generated at {output_file}!")