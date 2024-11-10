// static/js/audio-processor.js
class AudioProcessor extends AudioWorkletProcessor {
    constructor() {
        super();
        this.port.onmessage = (event) => {
            // Handle messages from the main thread if needed
        };
    }

    process(inputs, outputs, parameters) {
        const input = inputs[0];
        if (input.length > 0) {
            const audioChunk = input[0];
            this.port.postMessage({ audio: Array.from(audioChunk) });
        }
        return true; // Keep the processor alive
    }
}

registerProcessor('audio-processor', AudioProcessor);
