/**
 * Spectral Audio Engine for NecroCode.
 * Combines Web Audio API procedural soundscapes with ElevenLabs vocal playback
 * and browser SpeechSynthesis fallback.
 */

class SpectralAudioEngine {
  constructor() {
    this.audioCtx = null;
    this.ambientGain = null;
    this.isAmbientPlaying = false;
  }

  initContext() {
    if (!this.audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      this.audioCtx = new AudioContext();
    }
    if (this.audioCtx.state === 'suspended') {
      this.audioCtx.resume();
    }
  }

  toggleAmbientDrone() {
    this.initContext();
    if (this.isAmbientPlaying) {
      if (this.ambientGain) {
        this.ambientGain.gain.linearRampToValueAtTime(0.001, this.audioCtx.currentTime + 1.0);
        setTimeout(() => {
          this.ambientOsc1?.stop();
          this.ambientOsc2?.stop();
          this.isAmbientPlaying = false;
        }, 1000);
      }
      return false;
    } else {
      // Ethereal low-frequency drone (55Hz / 82.5Hz binaural harmonic)
      const t = this.audioCtx.currentTime;
      this.ambientGain = this.audioCtx.createGain();
      this.ambientGain.gain.setValueAtTime(0.001, t);
      this.ambientGain.gain.linearRampToValueAtTime(0.08, t + 2.0);

      this.ambientOsc1 = this.audioCtx.createOscillator();
      this.ambientOsc1.type = 'sawtooth';
      this.ambientOsc1.frequency.setValueAtTime(55, t); // A1

      this.ambientOsc2 = this.audioCtx.createOscillator();
      this.ambientOsc2.type = 'sine';
      this.ambientOsc2.frequency.setValueAtTime(82.41, t); // E2

      // Lowpass resonant filter for haunting underwater crypt feeling
      const filter = this.audioCtx.createBiquadFilter();
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(220, t);
      filter.Q.setValueAtTime(4.0, t);

      this.ambientOsc1.connect(filter);
      this.ambientOsc2.connect(filter);
      filter.connect(this.ambientGain);
      this.ambientGain.connect(this.audioCtx.destination);

      this.ambientOsc1.start();
      this.ambientOsc2.start();
      this.isAmbientPlaying = true;
      return true;
    }
  }

  playResurrectionChime() {
    this.initContext();
    const t = this.audioCtx.currentTime;
    const osc = this.audioCtx.createOscillator();
    const gain = this.audioCtx.createGain();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(528, t); // Solfeggio 528Hz transformation chime
    osc.frequency.exponentialRampToValueAtTime(880, t + 1.2);

    gain.gain.setValueAtTime(0.15, t);
    gain.gain.exponentialRampToValueAtTime(0.001, t + 1.5);

    osc.connect(gain);
    gain.connect(this.audioCtx.destination);

    osc.start(t);
    osc.stop(t + 1.5);
  }

  playSpectralVoice(text, base64Audio = null) {
    this.initContext();

    // Priority 1: High fidelity ElevenLabs audio stream if backend provided it
    if (base64Audio) {
      try {
        const audio = new Audio("data:audio/mpeg;base64," + base64Audio);
        audio.play();
        return;
      } catch (err) {
        console.warn("ElevenLabs audio play failed, falling back to Web Speech", err);
      }
    }

    // Priority 2: Offline Web Speech Synthesis with Spectral persona pitch
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.88;
      utterance.pitch = 0.65; // Eerie deep spectral voice
      utterance.volume = 0.9;
      
      const voices = window.speechSynthesis.getVoices();
      const preferred = voices.find(v => v.lang.startsWith("en") && (v.name.includes("Male") || v.name.includes("David") || v.name.includes("Google")));
      if (preferred) utterance.voice = preferred;

      window.speechSynthesis.speak(utterance);
    }
  }
}

window.spectralAudio = new SpectralAudioEngine();
