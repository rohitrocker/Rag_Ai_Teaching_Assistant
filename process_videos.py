import os
import subprocess

# Create audios folder if not exists
os.makedirs("audios", exist_ok=True)

files = os.listdir("videos")

for file in files:

    tutorial_number = file.split(" [")[0].split(" #")[1]
    file_name = file.split(" ｜ ")[0]

    print(tutorial_number, file_name)

    input_path = f"videos/{file}"
    output_path = f"audios/{tutorial_number}_{file_name}.mp3"

    subprocess.run([
        "ffmpeg",
        "-i",
        input_path,
        output_path
    ])