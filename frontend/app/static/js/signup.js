// signup.js
document.getElementById('signupForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    // Get form data
    const formData = new FormData(this);

    // Convert form data to JSON object
    const userData = {};
    formData.forEach((value, key) => {
        userData[key] = value;
    });

    // Send POST request to backend
    fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })
    .then(response => {
        // Handle response from server
        if (response.ok) {
            // Redirect user or show success message
            window.location.href = '/login';
        } else {
            // Handle error
            console.error('Signup failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
