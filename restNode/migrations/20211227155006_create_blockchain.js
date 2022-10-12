exports.up = function(knex) {
    return knex.schema.createTable('blockchain', function(t) {
        t.increments('id').primary()
        t.string('Data').notNullable()
        t.string('Hash').notNullable()
        t.string('PrevHash').notNullable()
        t.bit('Security').notNullable()
        t.timestamps(false, true)
    })
};

exports.down = function(knex) {
    return knex.schema.dropTableIfExists('blockchain')
};