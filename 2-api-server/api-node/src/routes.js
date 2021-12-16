import { Router } from 'express'
import { pool } from './db/connection'


const router = Router()

router.get( `/`, async ( req, res ) => {
   return res.status(200).json("Hello World!!")
} )

router.get( '/api/books/all', (req, res) => {
    pool.query('SELECT * FROM books', (err, result) => {
        if(err)
            res.status(403).json(err.message)
        res.status(200).json(result.rows)
    })
} )

router.get('/api/book', ( req, res ) => {
    // Check if an ID was provided as part of the URL.
    // If ID is provided, assign it to a variable.
    // If no ID is provided, display an error in the browser.
    const args = req.query
    let id = null
    if (args && args.id )
        id = parseInt(args.id)
    else
        return res.status(403).json("Error: No id field provided. Please specify an id.")
    
    // Empty list for our results
    const results = []

    // Loop through the data and match results that fit the requested ID.
    // IDs are unique, but other fields might return many results
    books.forEach( ( book ) => {
        if ( book.id === id )
            results.push(book)
    })
    pool.query('SELECT * FROM books WHERE id=$1', [id], (err, result) => {
        if(err)
            res.status(403).json(err.message)
        res.status(200).json(result.rows)
    })
})


router.post('/api/update/book', async (req, res) => {
    // Check if an ID was provided as part of the body.
    // If no ID is provided, display an error in the browser.
    const body = req.body
    if (!body.id)
        return res.status(403).json("Error: No id field provided. Please specify an id.")
    const {id, name, author, published} = body
    const found_book = await (await pool.query('SELECT * FROM books WHERE id=$1', [id])).rows[0]
  
    pool.query(
        'UPDATE books SET name=$2, author=$3, published=$4 where id=$1', 
        [id, name || found_book.name , author || found_book.author, published || found_book.published],
        (err, result) => {
            if (err)
                res.status(403).json(err.message)
            res.status(200).json({ 
                id, 
                name: name || found_book.name, 
                author: author || found_book.author, 
                published: published || found_book.published 
            })
        }
    )
})

router.post('/api/create/book', async (req, res) => {
    // Check if an ID was provided as part of the body.
    // If no ID is provided, display an error in the browser.
    const body = req.body
    const {name, author, published} = body
  
    pool.query(
        'INSERT INTO books (name, author, published) VALUES ($1,$2,$3)', 
        [name, author, published],
        (err, result) => {
            if (err)
                res.status(403).json(err.message)
            pool.query('SELECT * FROM books WHERE name=$1', [name], (err, result) => {
                res.status(200).json(result.rows[0])
            })
        }
    )
})


export { router }
