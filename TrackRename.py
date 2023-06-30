# Author: Paul M. Nakasone
# Descrição: Este script permite editar as faixas de arquivos MKV, alterando os títulos das faixas com base nas informações de idioma fornecidas. Ele utiliza as ferramentas mkvmerge e mkvpropedit para realizar as alterações nos arquivos MKV.

import os
import subprocess
import sys
import re
import json

# Crie a pasta "temp" se ela não existir
temp_dir = "temp"
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)
    
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
        json_file = os.path.join(temp_dir, os.path.splitext(os.path.basename(mkv_file))[0] + ".json")
        command = ["mkvmerge", "-J", mkv_file]
        with open(json_file, "w", encoding="utf-8") as f:
            result = subprocess.run(command, stdout=f, text=True)

        if result.returncode == 0:
            mkvmerge_files.append(json_file)
            print(f"Arquivo mkvmerge JSON criado para {mkv_file}")
        else:
            print(f"Erro ao gerar o arquivo mkvmerge JSON para {mkv_file}")
    return mkvmerge_files

def identify_tracks(mkvmerge_files):
    track_info = {}

    for mkvmerge_file in mkvmerge_files:
        with open(mkvmerge_file, "r", encoding="utf-8") as f:
            content = json.load(f)

        tracks = content.get("tracks", [])

        audio_and_subtitle_info = [
            (t["type"], t["properties"]["language_ietf"], t["properties"].get("forced_track", False))
            for t in tracks if t["type"] in ["audio", "subtitles"]
        ]

        track_info[mkvmerge_file] = {
            "track_types": [t for t, _, _ in audio_and_subtitle_info],
            "languages": [l for _, l, _ in audio_and_subtitle_info],
            "forced": ["1" if f else "0" for _, _, f in audio_and_subtitle_info]
        }

    # Salva as informações extraídas em um arquivo JSON na pasta "temp"
    track_info_file = os.path.join(temp_dir, "track_info.json")
    with open(track_info_file, "w", encoding="utf-8") as f:
        json.dump(track_info, f, ensure_ascii=False, indent=4)

    return track_info

def edit_mkv_files(mkv_files):
    # Carrega as informações do arquivo JSON na pasta "temp"
    track_info_file = os.path.join(temp_dir, "track_info.json")
    with open(track_info_file, "r", encoding="utf-8") as f:
        track_info = json.load(f)

    language_codes = {
        "en": "English",
        "en-US": "English (US)",
        "pt": "Português",
        "pt-BR": "Português (Brasil)",
        "pt-PT": "Português (Portugal)",
        "es": "Español",
        "es-419": "Español (Latinoamérica)",
        "es-ES": "Español (España)",
        "ar": "العربية",
        "cs": "Čeština",
        "da": "Dansk",
        "de": "Deutsch",
        "el": "Ελληνικά",
        "fi": "Suomi",
        "fil": "Filipino",
        "fr": "Français",
        "fr-CA": "Français (Canada)",
        "he": "עברית",
        "hr": "Hrvatski",
        "hu": "Magyar",
        "id": "Bahasa Indonesia",
        "it": "Italiano",
        "it-IT": "Italiano (Italia)",
        "ja": "日本語",
        "ja-JP": "日本語 (日本)",
        "ko": "한국어",
        "ml": "മലയാളം",
        "ms": "Bahasa Melayu",
        "nb": "Norsk (bokmål)",
        "nb-NO": "Norsk (bokmål)",
        "nl": "Nederlands",
        "pl": "Polski",
        "pl-PL": "Polski (Polska)",
        "ro": "Română",
        "ro-RO": "Română (România)",
        "sv": "Svenska",
        "th": "ไทย",
        "th-TH": "ไทย",
        "tr": "Türkçe",
        "tr-TR": "Türkçe (Türkiye)",
        "uk": "yкраїнська",
        "vi": "Tiếng Việt",
        "zh": "中文",
        "zh-CN": "中文(中华人民共和国)",
        "zh-HK": "中文(香港特別行政區)",
        "zh-Hans": "中文(简体)",
        "zh-Hant": "中文(繁體)",
        # Adicione outros códigos de idioma aqui
    }

    for mkv_file in mkv_files:
        mkvmerge_file = os.path.join(temp_dir, os.path.splitext(os.path.basename(mkv_file))[0] + ".json")
        info = track_info.get(mkvmerge_file, {})

        languages = info.get("languages", [])
        forced = info.get("forced", [])

        # Comece a iterar a partir da segunda faixa (índice 1)
        for i, (language, is_forced) in enumerate(zip(languages, forced), start=1):
            if language not in language_codes:
                continue

            new_title = language_codes[language]
            if is_forced == "1":
                new_title = "Forced"

            command = ["mkvpropedit", mkv_file, f"--edit", f"track:{i+1}", f"--set", f"name={new_title}"]
            result = subprocess.run(command)

            if result.returncode == 0:
                print(f"Alterações em {mkv_file} com sucesso.")
            else:
                print(f"Ocorreu um erro ao processar o {mkv_file}.")

if __name__ == "__main__":
    directory = input("Por favor, insira o caminho do diretório que contém os arquivos MKV para serem analisados: ")
    if not os.path.isdir(directory):
        print("O diretório informado não existe. Por favor, verifique o caminho e tente novamente.")
        sys.exit(1)

    mkv_files = get_mkv_files(directory)
    mkvmerge_files = create_mkvmerge_files(mkv_files)
    track_info = identify_tracks(mkvmerge_files)
    edit_mkv_files(mkv_files)
