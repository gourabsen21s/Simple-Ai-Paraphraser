const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const path = require('path'); // Import path module

const app = express();
const port = 3000;

app.use(bodyParser.json());

app.use(express.static(path.join(__dirname, 'frontend')));

app.post('/paraphrase', async (req, res) => {
    const inputText = req.body.text;
    
    try {
        const response = await axios.post('http://localhost:5000/paraphrase', {
            text: inputText
        });
        const paraphrasedText = response.data.paraphrasedText;
        res.json({ paraphrasedText });
    } catch (error) {
        console.error('Error communicating with Python API:', error);
        res.status(500).json({ error: 'Error communicating with Python API' });
    }
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'frontend', 'index.html'));
});

app.listen(port, () => {
    console.log(`Node.js server running on http://localhost:${port}`);
});
