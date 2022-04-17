const express = require('express');
const fileUpload = require('express-fileupload');
const fs = require('fs');
const {PythonShell} = require('python-shell');
const cors = require('cors');

const app = express();

app.use(fileUpload());
app.use(cors());

const runWrapper = (req, res, funcList, funcDict, output) => {
    let next = funcList.shift();
    funcDict[next](req, res, funcList, funcDict, output);
}

const sendResWrapper = (req, res, output) => {
    fs.unlink(`${__dirname}/${req.query.path}`, (err) => {
        if (err) {
            console.error(err)
            return
        }
    });
    insertInd = req.query.path.lastIndexOf('/');
    let vocabPath = req.query.path.slice(0, insertInd+1) + "vocab" + req.query.path.slice(insertInd+1)
    checkVocabPath = `${__dirname}/${vocabPath}` 
    fs.access(checkVocabPath, fs.R_OK, (err) => {
        if (!err) { 
            fs.unlink(`${__dirname}/${vocabPath}`, (err) => {
                if (err) {
                    console.error(err)
                    return
                }
            });
        } 
    });
    res.json(output);
}

const runSyntAnalysis = (req, res, funcList, funcDict, output) => {
    let parsedFilePath = '';

    // Run UDPipe first to get parsed file for processing
    const options = {
        mode: 'text',
        pythonPath: '/Library/Frameworks/Python.framework/Versions/3.8/bin/python3',
        pythonOptions: ['-u'], // get print results in real-time
        scriptPath: '/Users/alexgoberna/Desktop/senal/api'
    };

    options['args'] = [`${__dirname}/` + req.query.path, req.query.name];

    PythonShell.run('SENAL-SYNT/UDPipe.py', options, function (err, results) {
        if (err){
            console.log(err);
            console.log('There was an error in processing');
        }

        // Results are read as text, path is output by UDPipe in print statement
        parsedFilePath = results[0];

        // Process parsed file from UDPipe using LingComplexityFinalPlt
        options['args'] = [`${__dirname}/${parsedFilePath}`];
        options['mode'] = 'json';
        PythonShell.run('SENAL-SYNT/LingComplexityFinalPlt.py', options, function (err, results) {
            if (err){
                console.log(err);
                console.log('There was an error in processing');
            }

            // Results are read as JSON, data is output by LingComplexityFinal in print statement
            var outputData = results[0];

            // Delete parsed file from server
            fs.unlink(`${__dirname}/${parsedFilePath}`, (err) => {
                if (err) {
                    console.error(err)
                    return
                }
            });

            // Add output to previously computed output data
            output = {...(output), 'synt': outputData};

            // Run remaining functions requested
            if(funcList.length > 0){
                runWrapper(req, res, funcList, funcDict, output);
            }
            // Send response if no functions left
            else{
                sendResWrapper(req, res, output);
            }
        });
    });
}

const defaultFunc = (req, res, funcList, funcDict, output) => {
    // Run remaining functions requested
    if(funcList.length > 0){
        runWrapper(req, res, funcList, funcDict, output);
    }
    // Send response if no functions left
    else{
        sendResWrapper(req, res, output);
    } 
}

const runGrammarAssistant = (req, res, funcList, funcDict, output) => {
    let outputData = {};

    const options = {
        mode: 'json',
        pythonPath: '/Library/Frameworks/Python.framework/Versions/3.8/bin/python3',
        pythonOptions: ['-u'],
        scriptPath: '/Users/alexgoberna/Desktop/senal/api'
    };

    options['args'] = [`${__dirname}/` + req.query.path, req.query.name];

    PythonShell.run('Stats/stats.py', options, function (err, results) {
        if (err){
            console.log(err);
            console.log('There was an error in processing');
        }

        // Results are read as json, path is output by stats.py in object
        outputData = {...(results[0]['output'])};

        // Add output to previously computed output data
        output = {...(output), 'grammar': outputData};

        // Run remaining functions requested
        if(funcList.length > 0){
            runWrapper(req, res, funcList, funcDict, output);
        }
        // Send response if no functions left
        else{
            sendResWrapper(req, res, output);
        }
    });
}

const runClassifier = (req, res, funcList, funcDict, output) => {
    let outputData = {};


    const options = {
        mode: 'json',
        pythonPath: '/Library/Frameworks/Python.framework/Versions/3.8/bin/python3',
        pythonOptions: ['-u'],
        scriptPath: '/Users/alexgoberna/Desktop/senal/api'
    };

    options['args'] = [`${__dirname}/` + req.query.path];

    PythonShell.run('MLClassifier/Model/classifyFile.py', options, function (err, results) {
        if (err){
            console.log(err);
            console.log('There was an error in processing');
        }

        // Results are read as json, path is output by stats.py in object
        outputData = {...(results[0]['output'])};

        // Add output to previously computed output data
        output = {...(output), 'classifier': outputData};

        // Run remaining functions requested
        if(funcList.length > 0){
            runWrapper(req, res, funcList, funcDict, output);
        }
        // Send response if no functions left
        else{
            sendResWrapper(req, res, output);
        }
    });
}

const runLexAnalysis = (req, res, funcList, funcDict, output) => {
    let parsedFilePath = '';
    let outputData = {};

    // Run UDPipe first to get parsed file for processing
    const options = {
        mode: 'json',
        pythonPath: '/Library/Frameworks/Python.framework/Versions/3.8/bin/python3',
        pythonOptions: ['-u'], // get print results in real-time
        scriptPath: '/Users/alexgoberna/Desktop/senal/api'
    };

    options['args'] = [`${__dirname}/` + req.query.path, req.query.name];

    PythonShell.run('SENAL-LEX/WFreq.py', options, function (err, results) {
        if (err){
            console.log(err);
            console.log('There was an error in processing');
        }

        // Results are read as json, path is output by WFreq in object
        parsedFilePath = results[0]['parsedPath'];
        outputData = {...(results[0]['output'])};

        // Process parsed file from WFreq using SubtitleToStimuliFinal3
        options['args'] = [`${__dirname}/${parsedFilePath}`];
        options['mode'] = 'json';
        PythonShell.run('SENAL-LEX/SubtitleToStimuliFinal3.py', options, function (err, results) {
            if (err){
                console.log(err);
                console.log('There was an error in processing');
            }

            // Results are read as JSON, data is output by LingComplexityFinal in print statement
            outputData = {...(outputData), ...(results[0])};

            // Delete parsed file from server
            fs.unlink(`${__dirname}/${parsedFilePath}`, (err) => {
                if (err) {
                    console.error(err)
                    return
                }
            });

            // Add output to previously computed output data
            output = {...(output), 'lex': outputData};

            // Run remaining functions requested
            if(funcList.length > 0){
                runWrapper(req, res, funcList, funcDict, output);
            }
            // Send response if no functions left
            else{
                sendResWrapper(req, res, output);
            }
        });
    });
}

// Upload Endpoint
app.post('/api/upload', (req, res) => {
    if(req.files === null) {
        return res.status(400).json({ msg: 'No file was uploaded' });
    }

    // Set file to be uploaded
    const file = req.files.file;
    const vocab = req.files.vocab;

    // Upload File
    file.mv(`${__dirname}/uploads/${file.name}`, err => {
        if(err) {
            console.error(err);
            return res.status(500).send(err);  
        }
        if(vocab !== undefined){
            // Upload vocab
            vocab.mv(`${__dirname}/uploads/vocab${file.name}`, err => {
                if(err) {
                    console.error(err);
                    return res.status(500).send(err);  
                }
            }); 
        }
        res.json({ fileName: file.name, filePath: `/uploads/${file.name}`});
     });
});

app.get('/api/output', (req, res) => {
    // Programs to be run in req.query.program
    let funcList = req.query.program;
    let funcDict = {'Synt Analysis': runSyntAnalysis, 'Lex Analysis': runLexAnalysis, 'Grammar Assistant': runGrammarAssistant, 'L2 Classifier': runClassifier};
    if(funcList.length === 0){
        return res.status(400).json({ msg: 'No program was requested' });
    }
    runWrapper(req, res, funcList, funcDict, {});
});

app.get('/api/textOutput', (req, res) => {
    const text = req.query.text;
    const program = req.query.program;
    let programPath = '';
    let outputData = {};
    let output = {};

    const options = {
        mode: 'json',
        pythonPath: '/Library/Frameworks/Python.framework/Versions/3.8/bin/python3',
        pythonOptions: ['-u'],
        scriptPath: '/Users/alexgoberna/Desktop/senal'
    };

    if(program === "Text L2 Classifier"){
        programPath = 'MLClassifier/Model/classifyText.py';
    } else if(program === "CAPTURA"){
        programPath = 'SENAL-CAPTURA/captura3.py';
    } else{
        return res.status(400).json({ msg: 'Unknown program was requested' }); 
    }
    options['args'] = [text];

    PythonShell.run(programPath, options, function (err, results) {
        if (err){
            console.log(err);
            console.log('There was an error in processing');
        }
        // Results are read as json, path is output by stats.py in object
        outputData = {...(results[0]['output'])};

        output = {program : {...(outputData)}};
        res.json(output); 
    });
});

app.listen(process.env.PORT, () => console.log('Server Started...'));
