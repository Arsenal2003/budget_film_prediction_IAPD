import os
import csv

def generate_imdb_links_from_folder(folder_path="movie_info", output_file="imdb_links.csv"):
    all_links = []

    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"❌ Folder '{folder_path}' not found.")
        return

    csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

    if not csv_files:
        print(f"⚠️ No CSV files found in '{folder_path}'.")
        return

    print(f"📁 Found {len(csv_files)} CSV files in '{folder_path}'")

    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        print(f"🔍 Reading: {csv_file}")

        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            if "Const" not in reader.fieldnames:
                print(f"⚠️ Skipping '{csv_file}' (no 'Const' column).")
                continue

            for row in reader:
                const_value = row["Const"].strip()
                if const_value:
                    imdb_link = f"https://www.imdb.com/title/{const_value}/"
                    all_links.append([imdb_link])

    # Save combined results
    if all_links:
        with open(output_file, "w", newline="", encoding="utf-8") as out:
            writer = csv.writer(out)
            writer.writerow(["IMDb Link"])
            writer.writerows(all_links)
        print(f"\n✅ Saved {len(all_links)} total IMDb links to '{output_file}'")
    else:
        print("⚠️ No valid 'Const' values found in any CSV file.")


if __name__ == "__main__":
    generate_imdb_links_from_folder()
