import { Router } from 'express'
import { books } from './data.js'


const router = Router()

router.get( `/`, async ( req, res ) => {
   return res.status(200).json("Hello World!!")
} )

router.get( '/api/books/all', (req, res) => {
    return res.status(200).json(books)
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

    // Use the res.json function to convert our list in JSON format.
    // use res.status to return de code status of request
    return res.status(200).json(results)
})


router.post('/api/update/book', (req, res) => {
    // Check if an ID was provided as part of the body.
    // If no ID is provided, display an error in the browser.
    const body = req.body
    if (!body.id)
        return res.status(403).json("Error: No id field provided. Please specify an id.")
    const {id, title, author, published} = body

    // Use find function to array type to search unique value
    const found_book = books.find((book) => book.id === id)
    if(found_book){
        if(title)
            found_book.title = title
        if(author)
            found_book.author = author
        if(published)
            found_book.published = published
    } else 
        return res.status(404).json("Error: book not found")
    // Use the res.json function to convert our list in JSON format.
    // use res.status to return de code status of request
    return res.status(200).json(found_book)
})

export { router }
