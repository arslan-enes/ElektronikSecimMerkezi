const express = require('express')
const bodyParser = require('body-parser')
const usersRoutes = require('./routes/users')
const { spawn } = require('child_process')
const store = require('./store')
const { Console } = require('console')
const router = express.Router();
const http = require('http');
const fs = require('fs');
const PORT = 6000;


var server = http.createServer(function(req, res) {
    var dataToSend;
    const python = spawn('python', ['block_control.py']);

    python.stdout.on('data', (data) => {
        console.log('Pipe data from python script ...');
        dataToSend = data.toString();
        console.log(`${dataToSend}`);
    });
    python.stderr.on('data', (data) => {
        console.log(`child process close all stdio with code ${data}`);
    });
    res.writeHead(200, { 'Content-Type': 'text/html' });
    var myReadStream = fs.createReadStream(__dirname + "/test.html", 'utf-8');
    myReadStream.pipe(res);

});



module.exports = router;

server.listen(4545, '127.0.0.1');
console.log('Listening...')