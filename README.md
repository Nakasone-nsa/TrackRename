## TrackRename

This Python script allows you to analyze and edit MKV (Matroska Video) files. It performs various operations on MKV files, such as extracting track information and modifying track names based on language, forced status, and hearing impairment flag. Additionally, it removes the encoding date from the MKV files.

https://github.com/Nakasone-nsa/TrackRename/assets/137841760/8509a9c4-4f78-4e88-baa4-e31d2ff3d093

## Prerequisites
Before using this script, make sure you have the following requirements:
- Python 3.x
- 'mkvmerge' and 'mkvpropedit' command-line tools installed on your system. These tools are part of the MKVToolNix package, which can be downloaded from https://mkvtoolnix.download/.

## Installation

1. Download the script directly
2. Install 'mkvmerge' and 'mkvpropedit' command-line tools by downloading and installing the MKVToolNix package from https://mkvtoolnix.download/.

##Usage

1. Open a terminal or command prompt.
2. Navigate to the directory where the script is located.
3. Run the script using the following command: "py trackrename.py"
4. You will be prompted to enter the path to the directory that contains the MKV files you want to analyze and edit. Provide the path and press Enter.
5. The script will create a temporary directory (if it doesn't already exist) to store intermediate files.
6. It will then analyze the MKV files, extract track information, and generate corresponding JSON files using the mkvmerge tool.
7. The extracted track information will be stored in a file named "track_info.json" in the temporary directory.
8. Next, the script will modify the track names of the MKV files based on the extracted information using the mkvpropedit tool.
9. Finally, the script will remove the encoding date from the MKV files using the mkvpropedit tool.
10. Progress and result messages will be displayed in the terminal throughout the process.
[b]Note:[/b] Make sure to backup your MKV files before running the script, as it modifies the files directly.

O progresso e os resultados das edições serão exibidos no console.

## Acknowledgements

- This script utilizes the mkvmerge and mkvpropedit tools from the MKVToolNix package.
- The language code mappings used in the script are based on the ISO 639-1 language codes.

