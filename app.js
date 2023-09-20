function convertSpeechToText() {
    const fileInput = document.getElementById('audioFile');
    const textResult = document.getElementById('textResult');

    const formData = new FormData();
    formData.append('audio', fileInput.files[0]);

    fetch('/speech-to-text', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Error:', data.error);
            textResult.innerHTML = 'Error occurred during speech recognition.';
        } else {
            textResult.innerHTML = data.text;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        textResult.innerHTML = 'An error occurred. Please try again.';
    });
}

// ... (previous code) ...

// Text to Speech
$('#convertTTS').click(function() {
    const text = $('#ttsText').val();
    const targetLanguage = $('#targetLanguage').val(); // Add a select element for language selection

    $.ajax({
        type: 'POST',
        url: '/tts',
        data: { text: text, target_language: targetLanguage }, // Send the target language
        success: function(data) {
            const ttsAudio = new Audio(data.tts_filename); // Create an Audio element
            ttsAudio.play(); // Play the audio
        },
        error: function(error) {
            console.error(error);
            alert('Error converting text to speech.');
        }
    });
});
