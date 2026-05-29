import os
import json
import math

n = 5

for file_name in os.listdir("jsons"):

    if file_name.endswith(".json"):

        file_path = os.path.join("jsons", file_name)

        with open(file_path, "r", encoding="utf-8") as f:

            data = json.load(f)

            new_chunks = []

            num_chunks = len(data["chunks"])

            num_groups = math.ceil(num_chunks / n)

            for i in range(num_groups):

                start_idx = i * n

                end_idx = min((i + 1) * n, num_chunks)

                chunks_group = data["chunks"][start_idx:end_idx]

                new_chunks.append({

                    "number": chunks_group[0]["number"],

                    "title": chunks_group[0]["title"],

                    "start": chunks_group[0]["start"],

                    "end": chunks_group[-1]["end"],

                    "text": " ".join(c["text"] for c in chunks_group)

                })

        # Create folder
        os.makedirs("newjsons", exist_ok=True)

        # Save merged file
        output_path = os.path.join("newjsons", file_name)

        with open(output_path, "w", encoding="utf-8") as json_file:

            json.dump(
                {
                    "chunks": new_chunks,
                    "text": data["text"]
                },
                json_file,
                indent=4,
                ensure_ascii=False
            )