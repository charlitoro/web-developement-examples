import { Pool } from 'pg'

export const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'books',
  password: 'pastgres',
  port: 5432,
})