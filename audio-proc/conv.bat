cd C:\Users\Tobias Janke\Documents\2022\Recorder
for %%i in (*.WAV) do (
    ffmpeg -i "%%i" "Konvertiert/%%i"
)