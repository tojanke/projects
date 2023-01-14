for %%i in (*.WAV) do (
    ffmpeg -i "%%i" "Konvertiert/%%i"
)