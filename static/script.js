// Access webcam
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        const video = document.getElementById('webcam');
        video.srcObject = stream;
    })
    .catch(err => {
        console.error("Webcam access error: ", err);
        alert("Could not access webcam. Please upload an image instead.");
    });

// Capture frame and send to server
function capture() {
    const video = document.getElementById('webcam');
    const canvas = document.getElementById('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    
    canvas.toBlob(blob => {
        const formData = new FormData();
        formData.append('file', blob, 'webcam.jpg');
        
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(html => {
            document.body.innerHTML = html; // Load results page
        })
        .catch(err => {
            console.error("Upload error: ", err);
            alert("Error uploading webcam frame.");
        });
    }, 'image/jpeg');
}