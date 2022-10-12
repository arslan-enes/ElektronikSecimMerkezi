const knex = require('knex')(require('./knexfile'))

module.exports = {
    createUser({ data, hash, prevHash, security }) {
        console.log(`Added block with ${data} data.`)
        return knex('blockchain').insert({
            data,
            hash,
            prevHash,
            security
        })
    }
}