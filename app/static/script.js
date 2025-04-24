function uploadImage() {
    const input = document.getElementById('imageUpload');
    if (input.files && input.files[0]) {
        const file = input.files[0];

        // Preview the image
        const reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById('previewImage').src = e.target.result;
            document.getElementById('previewSection').style.display = 'block';
        };
        reader.readAsDataURL(file);

        // Upload the image via POST
        const formData = new FormData();
        formData.append('file', file);

        fetch('/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('resultSection').style.display = 'block';
            document.getElementById('predictedClass').innerText = data.prediction;
            document.getElementById('confidenceScore').innerText = data.confidence;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}
