from SimpleAudioIndexer import SimpleAudioIndexer as sai

SRC_DIR = "Audios\French pronunciation = ajouter\French pronunciation = ajouter.wav"

indexer = sai(mode="cmu", src_dir=SRC_DIR)

indexer.index_audio()
