# Author: Nakasone
# Description: This Python code performs analysis and editing operations on MKV (Matroska Video) files. It prompts the user to enter the path to a directory containing MKV files.

import os
import subprocess
import sys
import json

TEMP_DIR = "temp"


def create_temp_directory():
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)


def get_mkv_files(directory):
    mkv_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".mkv"):
                mkv_files.append(os.path.join(root, file))
    return mkv_files


def create_mkvmerge_files(mkv_files):
    mkvmerge_files = []
    for mkv_file in mkv_files:
        json_file = os.path.join(TEMP_DIR, os.path.splitext(os.path.basename(mkv_file))[0] + ".json")
        command = ["mkvmerge", "-J", mkv_file]
        with open(json_file, "w", encoding="utf-8") as f:
            result = subprocess.run(command, stdout=f, text=True)

        if result.returncode == 0:
            mkvmerge_files.append(json_file)
            print(f"Created mkvmerge JSON file for {mkv_file}")
        else:
            print(f"Failed to generate mkvmerge JSON file for {mkv_file}")
    return mkvmerge_files


def identify_tracks(mkvmerge_files):
    track_info = {}

    for mkvmerge_file in mkvmerge_files:
        with open(mkvmerge_file, "r", encoding="utf-8") as f:
            content = json.load(f)

        tracks = content.get("tracks", [])

        audio_and_subtitle_info = [
            {
                "type": t["type"],
                "language": t["properties"]["language_ietf"],
                "forced": t["properties"].get("forced_track", False),
                "flag_hearing_impaired": t["properties"].get("flag_hearing_impaired", False)
            }
            for t in tracks if t["type"] in ["audio", "subtitles"]
        ]

        track_info[mkvmerge_file] = {
            "track_types": [t["type"] for t in audio_and_subtitle_info],
            "languages": [t["language"] for t in audio_and_subtitle_info],
            "forced": ["1" if t["forced"] else "0" for t in audio_and_subtitle_info],
            "flag_hearing_impaired": ["1" if t["flag_hearing_impaired"] else "0" for t in audio_and_subtitle_info]
        }

    track_info_file = os.path.join(TEMP_DIR, "track_info.json")
    with open(track_info_file, "w", encoding="utf-8") as f:
        json.dump(track_info, f, ensure_ascii=False, indent=4)

    return track_info


def edit_mkv_files(mkv_files):
    track_info_file = os.path.join(TEMP_DIR, "track_info.json")
    with open(track_info_file, "r", encoding="utf-8") as f:
        track_info = json.load(f)

    language_codes = {
        "ar-SA": "سعودية",
        "ar-AE": "العربية (الإمارات العربية المتحدة)",
        "en": "English",
        "en-US": "English (United States)",
        "en-GB": "English (United Kingdom)",
        "pt": "Português",
        "pt-BR": "Português (Brasil)",
        "pt-PT": "Português (Portugal)",
        "es": "Español",
        "es-419": "Español (Latinoamérica)",
        "es-ES": "Español (España)",
        "es-CO": "Español (Colombia)",
        "es-CL": "Español (Chile)",
        "es-MX": "Español (México)",
        "ar": "العربية",
        "ar-001": "العربية",
        "ar-EG": "العربية (مصر)",
        "cs": "Czech",
        "cs-CZ": "Czech (Czech Republic)",
        "da": "Dansk",
        "da-DK": "Dansk (Danmark)",
        "de": "Deutsch",
        "de-DE": "Deutsch (Deutschland)",
        "el": "Ελληνικά",
        "el-GR": "Ελληνικά (Ελλάδα)",
        "fi": "Suomi",
        "fi-FI": "Suomi (Suomi)",
        "fil": "Filipino",
        "fil-PH": "Filipino (Pilipinas)",
        "fr": "Français",
        "fr-CA": "Français (Canada)",
        "fr-FR": "Français (France)",
        "he": "עברית",
        "he-IL": "עברית (ישראל)",
        "hi-IN": "हिंदी (भारत)",
        "hr": "Hrvatski",
        "hu": "Magyar",
        "hu-HU": "Magyar (Magyarország)",
        "id": "Bahasa Indonesia",
        "id-ID": "Bahasa Indonesia (Indonesia)",
        "it": "Italiano",
        "it-IT": "Italiano (Italia)",
        "ja": "日本語",
        "ja-JP": "日本語 (日本)",
        "ko": "한국어",
        "ko-KR": "한국어(대한민국)",
        "ml": "മലയാളം",
        "ms": "Bahasa Melayu",
        "ms-MY": "Bahasa Melayu (Malaysia)",
        "no": "Norsk",
        "nb-NO": "Norsk (bokmål)",
        "nl": "Nederlands",
        "nl-NL": "Nederlands (Nederland)",
        "pl": "Polski",
        "pl-PL": "Polski (Polska)",
        "ro": "Română",
        "ro-RO": "Română (România)",
        "ru": "Pусский",
        "ru-RU": "Pусский (Россия)",
        "sv": "Svenska",
        "sv-SE": "Svenska (Sverige)",
        "sk": "Slovenčina",
        "sk-SK": "Slovenčina (Slovenská republika)",
        "ta-IN": "தமிழ் (இந்தியா)",
        "te-IN": "తెలుగు (భారత దేశం)",
        "th": "ไทย",
        "th-TH": "ไทย",
        "tr": "Türkçe",
        "tr-TR": "Türkçe (Türkiye)",
        "uk": "yкраїнська",
        "uk-UA": "yкраїнська (Україна)",
        "vi": "Tiếng Việt",
        "vi-VN": "Tiếng Việt (Việt Nam)",
        "zh": "中文",
        "zh-CN": "中文(中华人民共和国)",
        "zh-HK": "中文(香港特別行政區)",
        "zh-Hans": "中文(简体)",
        "zh-Hant": "中文(繁體)",
        # Add other language codes here
    }

    for mkv_file in mkv_files:
        mkvmerge_file = os.path.join(TEMP_DIR, os.path.splitext(os.path.basename(mkv_file))[0] + ".json")
        info = track_info.get(mkvmerge_file, {})

        languages = info.get("languages", [])
        forced = info.get("forced", [])
        flag_hearing_impaired = info.get("flag_hearing_impaired", [])

        for i, (language, is_forced, is_hearing_impaired) in enumerate(zip(languages, forced, flag_hearing_impaired), start=1):
            if language not in language_codes:
                continue

            language_title = language_codes.get(language, language)
            if is_forced == "1":
                language_title += " [FORCED]"
            if is_hearing_impaired == "1":
                language_title += " [SDH]"

            command = ["mkvpropedit", mkv_file, f"--edit", f"track:{i + 1}", f"--set", f"name={language_title}"]

            try:
                result = subprocess.run(command, check=True)
                print(f"Successfully updated {mkv_file}.")
            except subprocess.CalledProcessError:
                print(f"An error occurred while processing {mkv_file}.")

        # Remove the encoding date using mkvpropedit
        try:
            date_removal_command = ["mkvpropedit", mkv_file, "--delete", "date"]
            result = subprocess.run(date_removal_command, check=True)
            print(f"Encoding date removed from {mkv_file}")
        except subprocess.CalledProcessError:
            print(f"Failed to remove encoding date from {mkv_file}.")


def main():
    directory = input("Please enter the path to the directory that contains the MKV files to analyze: ")
    if not os.path.isdir(directory):
        print("The specified directory does not exist. Please check the path and try again.")
        sys.exit(1)

    create_temp_directory()
    mkv_files = get_mkv_files(directory)
    mkvmerge_files = create_mkvmerge_files(mkv_files)
    track_info = identify_tracks(mkvmerge_files)
    edit_mkv_files(mkv_files)


if __name__ == "__main__":
    main()
