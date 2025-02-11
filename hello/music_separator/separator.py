from pathlib import Path
from demucs.apply import apply_model
from demucs.pretrained import get_model
import soundfile as sf
import librosa
import numpy as np
import torch

class MusicSeparator:
    def __init__(self):
        self.model = get_model(name='htdemucs_ft')
        self.model.cpu()

    def separate_vocals(self, input_file, output_dir):
        """Separate vocals using Demucs with proper tensor conversion"""
        y, sr = sf.read(input_file)

        # Ensure stereo input
        if y.ndim == 1:
            y = np.stack([y, y], axis=0)
        else:
            y = y.T

        if sr != self.model.samplerate:
            y = librosa.resample(y, orig_sr=sr, target_sr=self.model.samplerate)

        y = torch.tensor(y, dtype=torch.float32).unsqueeze(0)  # Shape: [1, 2, samples]
        device = next(self.model.parameters()).device
        y = y.to(device)

        with torch.no_grad():
            sources = apply_model(self.model, y, device=device)[0]

        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        vocal_index = self.model.sources.index("vocals")
        stem = sources[vocal_index].cpu().numpy().T
        sf.write(output_path / f"{Path(input_file).stem}.wav", stem, sr)

        return output_path