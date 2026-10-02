document.getElementById('spamForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const emailText = document.getElementById('emailText').value;
    const resultCard = document.getElementById('resultCard');
    const resultLabel = document.getElementById('resultLabel');
    const spamProb = document.getElementById('spamProb');
    const notSpamProb = document.getElementById('notSpamProb');

    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email_text: emailText })
        });

        const data = await response.json();

        resultCard.classList.remove('hidden', 'is-spam', 'not-spam');

        if (data.is_spam) {
            resultCard.classList.add('is-spam');
            resultLabel.textContent = '🚨 Result: Spam';
        } else {
            resultCard.classList.add('not-spam');
            resultLabel.textContent = '✅ Result: Not Spam';
        }

        spamProb.textContent = `${data.spam_probability}%`;
        notSpamProb.textContent = `${data.not_spam_probability}%`;

    } catch (error) {
        alert('Failed to connect to backend server. Make sure backend/app.py is running on port 5000.');
    }
});