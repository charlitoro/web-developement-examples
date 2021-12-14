import { json, urlencoded } from 'body-parser'
import cors from 'cors'
import express from 'express'

import { router } from './routes'

const application = express()
const serverPort = 8080

application.use( cors( {
    credentials: true,
    origin: true
} ) )

application.use( json() )
application.use( urlencoded( { extended: true } ) )
application.use( router )


const server = application.listen( serverPort, () => {
    console.info( `🚀 Server listen at http://localhost:${ serverPort }` )
} )

server.setTimeout( 1800000 ) // 10 minutes
