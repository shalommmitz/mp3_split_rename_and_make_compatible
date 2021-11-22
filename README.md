# mp3 split, rename and make compatible

I often hear long mp3 files in my wife's car, which is a Peugeot. The car's multimedia system is really sensitive about the format of the audio. So, I have written the utilities in this repository to 'shape' the audio files "just right".

## The utilities are:

  - rename_files_of_current_folder:

    Renames all the .mp3 files in the current directory to 01.mp3...xx.mp3.

  - convert_files_to_compatible:

    Transcode all .mp3 files in the specified directory to format compatible with old or limited MP3 players.  Like any transcoding operation, there is a loss of quality, so use only if your players does not play the original files.

  - split_files

    Will split all the files in the current folder, or in the specified folder, to 15-minutes shorter files.

## Installation

This software was developed and tested on Xubuntu 18.04. It will probably work on any Linux, or other POSIX, operating system. It might, or might not, work on Windows.
Beside Python, this software uses lame and FFMPEG for all the heavy lifting:

`sudo apt install FFmpeg lame`

## Author

**Shalom Mitz** - [shalommmitz](https://github.com/shalommmitz)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE ) file for details.


