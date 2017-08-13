


const express = require('express')
const bodyParser = require('body-parser')
const app = express()


// Extract data from the form and add to body property of request object.
app.use(bodyParser.urlencoded({extended: true}))
// app.use("/client", express.static(__dirname + '/client'));



// // DB CITY
// const AWS = require('aws-sdk')
// AWS.config.update({
//   region: "us-east-1"
// });
// var db = new AWS.DynamoDB.DocumentClient()

const database = require('./routes/database.js')

const axios = require('axios')


console.log("Node server up!")


app.listen(3000, ()=> {
    console.log('Now listening on 3000')
})


app.get('/', (req, res)=> {
    res.sendFile(__dirname + '/index.html')
})



app.post('/api/database', (req, res)=> {
    console.log("req + body")
    console.log(req.body)
    database.getSubjectById(req.body.code, function(subject, err) {

        if (err) {
            console.log(err)
        } else {
            console.log(subject)
            res.json(subject)

        }

    })

    res.redirect('/')

})




app.get('/axios', (req, res)=> {
    res.send("Axios response")
})

app.get('/app.js', (req, res)=> {
    res.sendFile(__dirname + '/app.js')
})

app.get('/node_modules/bulma/css/bulma.css', (req, res)=> {
    res.sendFile(__dirname + '/node_modules/bulma/css/bulma.css')
})

app.get('/node_modules/vue/dist/vue.js', (req, res)=> {
    res.sendFile(__dirname + '/node_modules/vue/dist/vue.js')
})

// app.post('/test', (req, res)=> {
//
//     console.log(req.body.code)
//
//     params = {
//         TableName: 'Subjects',
//         Key: { 'code' : req.body.code }
//     }
//
//     db.get(params, (err, data) => {
//         if (err) {
//             console.error("Unable to read item. Error: ", JSON.stringify(err, null, 2))
//         } else {
//             console.log("GetItem succeeded: ", JSON.stringify(data, null, 2))
//         }
//         res.redirect('/')
//     })
//
// })


// app.get('/test_db', (req, res)=> {
//
//     // console.log(req.body)
//
//     params = {
//         TableName: 'Subjects',
//         Key: { 'code' : 'WRIT6001' }
//     }
//
//     db.get(params, (err, data) => {
//         if (err) {
//             console.error("Unable to read item. Error: ", JSON.stringify(err, null, 2))
//         } else {
//             console.log("GetItem succeeded: ", JSON.stringify(data, null, 2))
//         }
//         res.redirect('/')
//     })
// })
