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
        "en-US": "English (United States)",
        "pt": "Português",
        "pt-BR": "Português (Brasil)",
        "pt-PT": "Português (Portugal)",
        "es": "Español",
        "es-419": "Español (Latinoamérica)",
        "es-ES": "Español (España)",
        "es-CO": "Español (Colombia)",
        "ar": "العربية",
        "ar-001": "العربية",
        "ar-EG": "العربية (مصر)",
        "cs": "Čeština",
        "cs-CZ": "Čeština (Česká republika)",
        "da": "Dansk",
        "da-DK": "Dansk (Danmark)",
        "de": "Deutsch",
        "de-DE": "Deutsch (Deutschland)",
        "el": "Ελληνικά",
        "el-GR": "Ελληνικά (Ελλάδα)",
        "fi": "Suomi",
        "fi-FI": "Suomi",
        "fil": "Filipino",
        "fil-PH": "Filipino",
        "fr": "Français",
        "fr-CA": "Français (Canada)",
        "fr-FR": "Français (France)",
        "he": "עברית",
        "he-IL": "עברית",
        "hi-IN": "हिंदी (भारत)",
        "hr": "Hrvatski",
        "hu": "Magyar",
        "hu-HU": "Magyar",
        "id": "Bahasa Indonesia",
        "id-ID": "Bahasa Indonesia",
        "it": "Italiano",
        "it-IT": "Italiano (Italia)",
        "ja": "日本語",
        "ja-JP": "日本語 (日本)",
        "ko": "한국어",
        "ko-KR": "한국어",
        "ml": "മലയാളം",
        "ms": "Bahasa Melayu",
        "ms-MY": "Bahasa Melayu",
        "nb": "Norsk",
        "nb-NO": "Norsk (bokmål)",
        "nl": "Nederlands",
        "nl-NL": "Nederlands",
        "pl": "Polski",
        "pl-PL": "Polski (Polska)",
        "ro": "Română",
        "ro-RO": "Română (România)",
        "ru": "русский",
        "ru-RU": "русский (Россия)",
        "sv": "Svenska",
        "sv-SE": "Svenska",
        "ta-IN": "தமிழ் (இந்தியா)",
        "te-IN": "తెలుగు (భారత దేశం)",
        "th": "ไทย",
        "th-TH": "ไทย",
        "tr": "Türkçe",
        "tr-TR": "Türkçe (Türkiye)",
        "uk": "yкраїнська",
        "uk-UA": "yкраїнська",
        "vi": "Tiếng Việt",
        "vi-VN": "Tiếng Việt",
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
        flag_hearing_impaired = info.get("flag_hearing_impaired", [])  # Novo campo adicionado

        # Comece a iterar a partir da segunda faixa (índice 1)
        for i, (language, is_forced, is_hearing_impaired) in enumerate(zip(languages, forced, flag_hearing_impaired), start=1):
            if language not in language_codes:
                continue

            language_title = language_codes.get(language, language)  # Obter o título do idioma com base no language_codes
            if is_forced == "1":
                language_title += " [FORCED]"
            if is_hearing_impaired == "1":  # Verifica se é uma faixa "hearing impaired"
                language_title += " [SDH]"  # Adiciona o termo " [SDH]" ao título do idioma

            command = ["mkvpropedit", mkv_file, f"--edit", f"track:{i+1}", f"--set", f"name={language_title}"]
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
