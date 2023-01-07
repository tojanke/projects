from pydub import AudioSegment
from datetime import datetime, timedelta
import os

base_dir = "Konvertiert\\"
export_dir = base_dir + "Merged\\"

def export_audiofile(audio_file, date_start, suffix):
    print("Export " + str(date_start))
    date_base = date_start.replace(minute=0, second=0)
    base_audio = AudioSegment.silent(duration=(date_start-date_base).total_seconds()*1000)
    full_audio = base_audio + audio_file
    itr_sec = 0
    while itr_sec < full_audio.duration_seconds:
        end_sec = itr_sec + 60 * 60
        part_audio = full_audio[itr_sec*1000:end_sec*1000]
        part_date = date_base + timedelta(seconds=itr_sec)
        part_file = export_dir + part_date.strftime('%Y-%m-%d %H-%M') + suffix
        if not os.path.isfile(part_file):
            print("Write " + part_file)
            part_audio.export(part_file)
        itr_sec = end_sec


started = False

for file in os.listdir(base_dir):
     filename = os.fsdecode(file)
     if filename.endswith(".WAV"):        
        date_str = filename[:14]
        date_start = datetime.strptime(date_str, '%Y%m%d%H%M%S')
        song = AudioSegment.from_wav(base_dir + filename)
        dur_s = song.duration_seconds
        date_end = date_start + timedelta(seconds=dur_s)        
        
        if not started:            
            audio_file = song
            track_start = date_start
            track_suffix = filename[14:]
            started = True
        else:
            diff_to_prev = (date_start - prev_end).total_seconds()
            
            if diff_to_prev < 3600:
                between = AudioSegment.silent(duration=diff_to_prev*1000)
                audio_file = audio_file + between + song                
            else:
                export_audiofile(audio_file, track_start, track_suffix)
                audio_file = song
                track_start = date_start
                track_suffix = filename[14:]
        prev_end = date_end
export_audiofile(audio_file, track_start, track_suffix)


