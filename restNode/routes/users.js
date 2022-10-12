const express = require('express')
const router = express.Router();

module.exports = router;

const users = [{
        firstName: "John",
        lastName: "Doe",
        age: 25
    },
    {
        firstName: "Jane",
        lastName: "Doe",
        age: 24
    }
]

//all routes in here are starting with /users
router.get('/', (req, res) => {
    console.log(users);
    res.send(users);

})

router.post('/', (req, res) => {

    const user = req.body;
    const userId = uuidv4();
    const userWithID = {...user, id: userId }

    users.push(userWithID);

    res.send(`User with the name ${user.firstName} added to the database`);
})