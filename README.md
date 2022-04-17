# Mora Music Metadata Grabber
The program grabs the song metadata from mora.jp artist page and save that artist's single/album metadata into some flac files.

## Implementation Notes
1. The program runs with python, so make sure you have installed python on your computer.
2. Copy the repo.
3. Install dependencies using `pip install -r requirements.txt`.
4. You are good to go.

## Usage
`Nippon_Mora_GrabFromAlbum.py` grabs the metadata from single/album, e.g., [Aimer Zankyosanka / Asa ga kuru](https://mora.jp/package/43000100/VVCL01955B00Z_96/).
`Nippon_Mora_GrabFromArtist.py` grabs all the metadata of singles/albums from an artist, e.g., [YOASOBI](https://mora.jp/artist/1223123/).

The program grabs metadata of:
```
"artist"
"album"
"title"
"track"
"date"
```

and requires dependencies of:
```
mutagen==1.45.1
requests==2.27.1
selenium==4.1.3
```

For dependencies, you may install via `pip install -r requirements.txt`.

## Notes
It's better for you to study the code before you run it.
