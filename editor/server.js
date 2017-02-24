const express = require("express");
const path = require("path");
const fs = require("fs");
const bodyParser = require('body-parser');

const app = express();

app.use("/build", express.static("build"));
app.use("/monaco", express.static("monaco"));
app.use(bodyParser.json());

app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname + "/index.html"));
});

app.get("/api/graph.json", (req, res) => {
    res.type("json");
    fs.readFile("../bot/graph.json", (err, data) => {
        if (err) {
            res.status("500");
            res.send(JSON.stringify({
                "error": "Couldn't read file"
            }));
        } else {
            res.send(data);
        }
    });
});

app.put("/api/graph.json", (req, res) => {
    res.type("json");
    json = JSON.stringify(req.body, undefined, 4);
    fs.writeFile("../bot/graph.json", json, (err) => {
        if (err) {
            res.status("500");
            res.send(JSON.stringify({
                "error": "Couldn't write file"
            }));
        } else {
            res.send(JSON.stringify({
                "status": "ok"
            }));
        }
    });
});

app.listen(8080, () =>  {
    console.log("Listening on port 8080")
});
