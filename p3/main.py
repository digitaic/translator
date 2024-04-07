import torch
from TTS.api import TTS

device = "cuda" if torch.cuda.is_available() else "cpu"

print(TTS().list_models())

# Init TTS with the target model name
tts = TTS(model_name="tts_models/en/thorsten/tacotron2-DDC", progress_bar=False).to(device)

