const express = require('express')
const bodyParser = require('body-parser')
const usersRoutes = require('./routes/users')
const { spawn } = require('child_process')
const store = require('./store')
const { Console } = require('console')
const router = express.Router();
const soap = require('soap');


const app = express();
const PORT = 5000;

module.exports = router;


app.use(bodyParser.json());


app.get('/prevHashEkleme', (req, res) => {

    const python = spawn('python', ['prevHashEkleme.py']);
    python.on('close', (code) => {

        console.log(`child process close all stdio with code ${code}`);
    });

    res.send(200);
});

app.post('/createBlock', (req, res) => {

    var dataToSend;
    // spawn new child process to call the python script
    const python = spawn('python', ['script.py', req.body.data]);

    // collect data from script
    python.stdout.on('data', function(data) {
        console.log('Pipe data from python script ...');
        dataToSend = data.toString();
    });
    python.stderr.on('error', function(error) {
            console.log(error);
        })
        // in close event we are sure that stream from child process is closed
    python.on('close', (code) => {
        // send data to browser
        store
            .createUser({
                data: req.body.data,
                hash: dataToSend,
                prevHash: "temp",
                security: 1
            })
            .then(() => res.redirect('/prevHashEkleme'))

        console.log(`child process close all stdio with code ${code}`);
    });

});

app.listen(PORT, () => {
    console.log(`Server running on: http://localhost:${PORT}`);

});